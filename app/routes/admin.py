from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
import uuid

from app.database.db import SessionLocal
from app.database.models import APIKey, Account, Transaction

router = APIRouter(prefix="/admin")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class CreateAccountRequest(BaseModel):
    email: EmailStr
    initial_balance: float = 0.0


class CreateAPIKeyRequest(BaseModel):
    account_id: str
    name: str


class TopUpRequest(BaseModel):
    account_id: str
    amount: float


@router.post("/accounts")
async def create_account(
    request: CreateAccountRequest,
    db: Session = Depends(get_db)
):
    """Create a new account"""
    # Check if account already exists
    existing = db.query(Account).filter(Account.email == request.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Account with this email already exists")
    
    account = Account(
        id=Account.generate_id(),
        email=request.email,
        balance=request.initial_balance
    )
    
    db.add(account)
    
    # Create initial transaction if balance > 0
    if request.initial_balance > 0:
        transaction = Transaction(
            id=f"txn_{Account.generate_id()}",
            account_id=account.id,
            amount=request.initial_balance,
            transaction_type="topup",
            description="Initial account balance"
        )
        db.add(transaction)
    
    db.commit()
    db.refresh(account)
    
    return {
        "account_id": account.id,
        "email": account.email,
        "balance": account.balance,
        "created_at": account.created_at.isoformat()
    }


@router.post("/api-keys")
async def create_api_key(
    request: CreateAPIKeyRequest,
    db: Session = Depends(get_db)
):
    """Create a new API key for an account"""
    # Verify account exists
    account = db.query(Account).filter(Account.id == request.account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    try:
        new_key = APIKey(
            id=str(uuid.uuid4()),
            key=APIKey.generate_key(),
            name=request.name,
            account_id=request.account_id
        )
        
        db.add(new_key)
        db.commit()
        db.refresh(new_key)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create API key: {str(e)}")
    
    return {
        "id": new_key.id,
        "name": new_key.name,
        "api_key": new_key.key,
        "account_id": new_key.account_id,
        "created_at": new_key.created_at.isoformat()
    }


@router.post("/top-up")
async def top_up_account(
    request: TopUpRequest,
    db: Session = Depends(get_db)
):
    """Top up an account balance"""
    if request.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than 0")
    
    account = db.query(Account).filter(Account.id == request.account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # Update balance
    account.balance += request.amount
    
    # Create transaction record
    transaction = Transaction(
        id=f"txn_{Account.generate_id()}",
        account_id=account.id,
        amount=request.amount,
        transaction_type="topup",
        description=f"Account top-up: ${request.amount:.2f}"
    )
    
    db.add(transaction)
    db.commit()
    db.refresh(account)
    
    return {
        "account_id": account.id,
        "new_balance": account.balance,
        "amount_added": request.amount,
        "transaction_id": transaction.id
    }


@router.get("/accounts/{account_id}")
async def get_account(
    account_id: str,
    db: Session = Depends(get_db)
):
    """Get account details"""
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # Get API keys for this account
    api_keys = db.query(APIKey).filter(APIKey.account_id == account_id).all()
    
    return {
        "account_id": account.id,
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
