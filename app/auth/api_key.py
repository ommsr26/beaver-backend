from fastapi import Header, HTTPException, status, Depends, Request
from sqlalchemy.orm import Session, joinedload

from app.database.db import SessionLocal
from app.database.models import APIKey, Account


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def verify_api_key(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Verify API key from request.
    First checks if middleware already validated it, otherwise validates it here.
    """
    # If API key is already validated by middleware, use it
    if hasattr(request.state, "api_key"):
        return request.state.api_key
    
    # Fallback: validate API key if not set by middleware
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

    api_key_value = authorization.replace("Bearer ", "").strip()

    api_key = db.query(APIKey).options(
        joinedload(APIKey.account)
    ).filter(
        APIKey.key == api_key_value,
        APIKey.is_active == True
    ).first()

    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or disabled API key"
        )

    # Check if account has sufficient balance
    if api_key.account.balance < 0:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Insufficient account balance. Please top up your account."
        )

    return api_key
