"""
Authentication dependencies for FastAPI routes
Supports both JWT and API key authentication
"""
from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import Optional

from app.database.db import SessionLocal
from app.database.models import Account
from app.auth.jwt import verify_token
from app.auth.api_key import verify_api_key


def get_db():
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user_jwt(
    request: Request,
    db: Session = Depends(get_db)
) -> Account:
    """
    Get current user from JWT token.
    Expects Authorization header with Bearer token (JWT).
    
    Returns:
        Account object
        
    Raises:
        HTTPException if token is invalid or user not found
    """
    authorization = request.headers.get("Authorization")
    
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header"
        )
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization format"
        )
    
    token = authorization.replace("Bearer ", "").strip()
    
    # Verify JWT token
    payload = verify_token(token, token_type="access")
    
    # Extract user info from payload
    account_id = payload.get("sub")  # Standard JWT claim for subject (user ID)
    if not account_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    
    # Get account from database
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return account


async def get_current_user_optional(
    request: Request,
    db: Session = Depends(get_db)
) -> Optional[Account]:
    """
    Get current user from JWT token (optional).
    Returns None if no valid token is provided.
    Useful for endpoints that work with or without auth.
    """
    try:
        return await get_current_user_jwt(request, db)
    except HTTPException:
        return None


async def get_current_user_flexible(
    request: Request,
    db: Session = Depends(get_db)
) -> Account:
    """
    Get current user from either JWT or API key.
    Tries JWT first, falls back to API key.
    
    This allows endpoints to accept both authentication methods.
    """
    # Try JWT first
    try:
        return await get_current_user_jwt(request, db)
    except HTTPException:
        pass
    
    # Fall back to API key
    # verify_api_key uses Depends(get_db) internally, so we validate manually
    authorization = request.headers.get("Authorization")
    
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required (JWT token or API key)"
        )
    
    api_key_value = authorization.replace("Bearer ", "").strip()
    
    # Check if it's an API key (starts with "beaver_")
    if api_key_value.startswith("beaver_"):
        from app.database.models import APIKey
        from sqlalchemy.orm import joinedload
        
        api_key = db.query(APIKey).options(
            joinedload(APIKey.account)
        ).filter(
            APIKey.key == api_key_value,
            APIKey.is_active == True
        ).first()
        
        if not api_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required (JWT token or API key)"
            )
        
        # Check balance
        if api_key.account.balance < 0:
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail="Insufficient account balance. Please top up your account."
            )
        
        return api_key.account
    
    # Not a JWT token and not an API key
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication required (JWT token or API key)"
    )

