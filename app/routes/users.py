"""
User management endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database.db import SessionLocal
from app.database.models import APIKey, Account
from app.auth.dependencies import get_current_user_flexible
from app.database.models import Account

router = APIRouter(prefix="/users")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class UpdateUserRequest(BaseModel):
    email: str = None
    # Add more fields as needed


@router.get("/me")
async def get_current_user(
    account: Account = Depends(get_current_user_flexible),
    db: Session = Depends(get_db)
):
    """
    Get current user info
    Same as GET /auth/me for frontend compatibility
    Supports both JWT and API key authentication
    """
    
    # Get all API keys for this account
    api_keys = db.query(APIKey).filter(
        APIKey.account_id == account.id
    ).all()
    
    return {
        "id": account.id,
        "email": account.email,
        "balance": account.balance,
        "api_keys": [
            {
                "id": key.id,
                "name": key.name,
                "is_active": key.is_active,
                "created_at": key.created_at.isoformat()
            }
            for key in api_keys
        ],
        "created_at": account.created_at.isoformat()
    }


@router.patch("/me")
async def update_current_user(
    request: UpdateUserRequest,
    account: Account = Depends(get_current_user_flexible),
    db: Session = Depends(get_db)
):
    """
    Update current user settings
    Supports both JWT and API key authentication
    """
    
    # Update email if provided
    if request.email and request.email != account.email:
        # Check if email is already taken
        existing = db.query(Account).filter(
            Account.email == request.email,
            Account.id != account.id
        ).first()
        
        if existing:
            raise HTTPException(status_code=400, detail="Email already in use")
        
        account.email = request.email
    
    db.commit()
    db.refresh(account)
    
    return {
        "id": account.id,
        "email": account.email,
        "balance": account.balance,
        "message": "User updated successfully"
    }

