"""
Authentication endpoints for frontend
Supports password-based registration/login with JWT tokens
"""
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime, timedelta
from typing import Optional

from app.database.db import SessionLocal
from app.database.models import Account, APIKey, RefreshToken
from app.auth.password import hash_password, verify_password, validate_password_strength
from app.auth.jwt import create_access_token, create_refresh_token, verify_token
from app.auth.dependencies import get_db, get_current_user_jwt, get_current_user_flexible
from app.config import settings

router = APIRouter(prefix="/auth")


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    initial_balance: float = 0.0

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        is_valid, error_msg = validate_password_strength(v)
        if not is_valid:
            raise ValueError(error_msg)
        return v


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Register a new user account with password.
    Password is hashed and stored securely.
    Does NOT issue JWT tokens - user must login after registration.
    """
    # Check if account already exists
    existing = db.query(Account).filter(Account.email == request.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password
    password_hash = hash_password(request.password)
    
    # Create account
    account = Account(
        id=Account.generate_id(),
        email=request.email,
        password_hash=password_hash,
        email_verified=False,
        balance=request.initial_balance
    )
    db.add(account)
    db.flush()  # Get account ID
    
    # Create default API key
    api_key = APIKey(
        id=str(uuid.uuid4()),
        key=APIKey.generate_key(),
        name="Default Key",
        account_id=account.id
    )
    db.add(api_key)
    db.commit()
    db.refresh(account)
    db.refresh(api_key)
    
    return {
        "account": {
            "id": account.id,
            "email": account.email,
            "balance": account.balance,
            "email_verified": account.email_verified
        },
        "api_key": api_key.key,
        "api_key_id": api_key.id,
        "message": "Account created successfully. Please login to get JWT tokens."
    }


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login with email and password.
    Returns JWT access token and refresh token on success.
    """
    # Find account
    account = db.query(Account).filter(Account.email == request.email).first()
    
    if not account:
        # Use generic error message to prevent email enumeration
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Check if account has password (backward compatibility)
    if not account.password_hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account not set up for password authentication. Please register with a password."
        )
    
    # Verify password
    if not verify_password(request.password, account.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Create tokens
    token_data = {
        "sub": account.id,  # Standard JWT claim for subject (user ID)
        "email": account.email
    }
    
    access_token = create_access_token(token_data)
    refresh_token_str = create_refresh_token(token_data)
    
    # Store refresh token in database for revocation
    expires_at = datetime.utcnow() + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = RefreshToken(
        id=RefreshToken.generate_id(),
        token=refresh_token_str,
        account_id=account.id,
        expires_at=expires_at,
        is_revoked=False
    )
    db.add(refresh_token)
    db.commit()
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token_str,
        token_type="bearer",
        expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token.
    """
    try:
        # Verify refresh token
        payload = verify_token(request.refresh_token, token_type="refresh")
        account_id = payload.get("sub")
        
        if not account_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        # Check if refresh token is revoked
        refresh_token_record = db.query(RefreshToken).filter(
            RefreshToken.token == request.refresh_token,
            RefreshToken.account_id == account_id,
            RefreshToken.is_revoked == False
        ).first()
        
        if not refresh_token_record:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token not found or revoked"
            )
        
        # Check if token is expired (database check)
        if refresh_token_record.expires_at < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has expired"
            )
        
        # Get account
        account = db.query(Account).filter(Account.id == account_id).first()
        if not account:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        # Create new tokens
        token_data = {
            "sub": account.id,
            "email": account.email
        }
        
        access_token = create_access_token(token_data)
        refresh_token_str = create_refresh_token(token_data)
        
        # Revoke old refresh token
        refresh_token_record.is_revoked = True
        
        # Store new refresh token
        expires_at = datetime.utcnow() + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
        new_refresh_token = RefreshToken(
            id=RefreshToken.generate_id(),
            token=refresh_token_str,
            account_id=account.id,
            expires_at=expires_at,
            is_revoked=False
        )
        db.add(new_refresh_token)
        db.commit()
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token_str,
            token_type="bearer",
            expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )


@router.post("/logout")
async def logout(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Logout by revoking refresh token.
    """
    try:
        # Verify token to get account_id
        payload = verify_token(request.refresh_token, token_type="refresh")
        account_id = payload.get("sub")
        
        if account_id:
            # Revoke refresh token
            refresh_token = db.query(RefreshToken).filter(
                RefreshToken.token == request.refresh_token,
                RefreshToken.account_id == account_id
            ).first()
            
            if refresh_token:
                refresh_token.is_revoked = True
                db.commit()
        
        return {"message": "Logged out successfully"}
        
    except HTTPException:
        # Token invalid, but still return success (idempotent)
        return {"message": "Logged out successfully"}
    except Exception:
        return {"message": "Logged out successfully"}


@router.get("/me")
async def get_current_user(
    account: Account = Depends(get_current_user_flexible),
    db: Session = Depends(get_db)
):
    """
    Get current user info from JWT token or API key.
    Supports both authentication methods for backward compatibility.
    """
    # Get all API keys for this account
    api_keys = db.query(APIKey).filter(
        APIKey.account_id == account.id
    ).all()
    
    return {
        "id": account.id,
        "email": account.email,
        "balance": account.balance,
        "email_verified": account.email_verified,
        "api_keys": [
            {
                "id": key.id,
                "name": key.name,
                "is_active": key.is_active,
                "created_at": key.created_at.isoformat(),
                "key_preview": key.key[:20] + "..." if len(key.key) > 20 else key.key
            }
            for key in api_keys
        ],
        "created_at": account.created_at.isoformat()
    }
