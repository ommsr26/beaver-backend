"""
API Key management endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database.db import SessionLocal
from app.database.models import APIKey
from app.auth.dependencies import get_current_user_flexible
from app.database.models import Account

router = APIRouter(prefix="/keys")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class CreateAPIKeyRequest(BaseModel):
    name: str


@router.get("")
async def list_api_keys(
    account: Account = Depends(get_current_user_flexible),
    db: Session = Depends(get_db)
):
    """List all API keys for current account
    Supports both JWT and API key authentication"""
    
    api_keys = db.query(APIKey).filter(
        APIKey.account_id == account.id
    ).order_by(APIKey.created_at.desc()).all()
    
    return {
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
        "total": len(api_keys)
    }


@router.post("")
async def create_api_key(
    request: CreateAPIKeyRequest,
    account: Account = Depends(get_current_user_flexible),
    db: Session = Depends(get_db)
):
    """Create a new API key for current account
    Supports both JWT and API key authentication"""
    
    new_key = APIKey(
        id=APIKey.generate_key(),
        key=APIKey.generate_key(),
        name=request.name,
        account_id=account.id
    )
    
    db.add(new_key)
    db.commit()
    db.refresh(new_key)
    
    return {
        "id": new_key.id,
        "name": new_key.name,
        "api_key": new_key.key,  # Only returned on creation
        "account_id": new_key.account_id,
        "created_at": new_key.created_at.isoformat()
    }


@router.delete("/{key_id}")
async def delete_api_key(
    key_id: str,
    account: Account = Depends(get_current_user_flexible),
    db: Session = Depends(get_db)
):
    """Delete an API key (must belong to current account)
    Supports both JWT and API key authentication"""
    
    # Find the key
    key_to_delete = db.query(APIKey).filter(
        APIKey.id == key_id,
        APIKey.account_id == account.id
    ).first()
    
    if not key_to_delete:
        raise HTTPException(status_code=404, detail="API key not found")
    
    # Revoke the key instead of deleting (set is_active=False)
    # This preserves history while making the key unusable
    key_to_delete.is_active = False
    db.commit()
    
    return {"message": "API key revoked successfully"}


@router.post("/generate")
async def generate_api_key(
    account: Account = Depends(get_current_user_flexible),
    db: Session = Depends(get_db)
):
    """
    Generate a new API key (alias for POST /api-keys)
    Frontend compatibility endpoint
    Supports both JWT and API key authentication
    """
    
    new_key = APIKey(
        id=APIKey.generate_key(),
        key=APIKey.generate_key(),
        name="Generated Key",
        account_id=account.id
    )
    
    db.add(new_key)
    db.commit()
    db.refresh(new_key)
    
    return {
        "api_key": new_key.key,
        "id": new_key.id,
        "name": new_key.name,
        "created_at": new_key.created_at.isoformat()
    }

