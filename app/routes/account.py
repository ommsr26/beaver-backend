from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from pydantic import BaseModel

from app.database.db import SessionLocal
from app.database.models import Account, Transaction, UsageLog
from app.auth.dependencies import get_current_user_flexible
from app.database.models import Account

router = APIRouter(prefix="/account")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/balance")
async def get_balance(
    account: Account = Depends(get_current_user_flexible),
    db: Session = Depends(get_db)
):
    """Get current account balance
    Supports both JWT and API key authentication"""
    return {
        "account_id": account.id,
        "email": account.email,
        "balance": account.balance,
        "currency": "USD"
    }


@router.get("/transactions")
async def get_transactions(
    account: Account = Depends(get_current_user_flexible),
    db: Session = Depends(get_db),
    limit: int = 50
):
    """Get transaction history
    Supports both JWT and API key authentication"""
    
    transactions = db.query(Transaction).filter(
        Transaction.account_id == account.id
    ).order_by(
        Transaction.created_at.desc()
    ).limit(limit).all()
    
    return {
        "account_id": account.id,
        "transactions": [
            {
                "id": txn.id,
                "amount": txn.amount,
                "type": txn.transaction_type,
                "description": txn.description,
                "created_at": txn.created_at.isoformat()
            }
            for txn in transactions
        ]
    }


@router.get("/usage")
async def get_usage(
    account: Account = Depends(get_current_user_flexible),
    db: Session = Depends(get_db),
    days: int = 30
):
    """
    Get usage analytics
    Returns usage stats for the specified number of days
    Supports both JWT and API key authentication
    """
    
    # Calculate date range
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Get usage logs
    usage_logs = db.query(UsageLog).filter(
        UsageLog.account_id == account.id,
        UsageLog.created_at >= start_date,
        UsageLog.created_at <= end_date
    ).all()
    
    # Calculate statistics
    total_requests = len(usage_logs)
    total_input_tokens = sum(log.input_tokens for log in usage_logs)
    total_output_tokens = sum(log.output_tokens for log in usage_logs)
    total_cost = sum(log.total_cost for log in usage_logs)
    
    # Group by model
    model_stats = {}
    for log in usage_logs:
        if log.model_id not in model_stats:
            model_stats[log.model_id] = {
                "model_id": log.model_id,
                "requests": 0,
                "input_tokens": 0,
                "output_tokens": 0,
                "cost": 0.0
            }
        model_stats[log.model_id]["requests"] += 1
        model_stats[log.model_id]["input_tokens"] += log.input_tokens
        model_stats[log.model_id]["output_tokens"] += log.output_tokens
        model_stats[log.model_id]["cost"] += log.total_cost
    
    return {
        "account_id": account.id,
        "period_days": days,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "summary": {
            "total_requests": total_requests,
            "total_input_tokens": total_input_tokens,
            "total_output_tokens": total_output_tokens,
            "total_tokens": total_input_tokens + total_output_tokens,
            "total_cost": round(total_cost, 6)
        },
        "by_model": list(model_stats.values())
    }


@router.get("/billing")
async def get_billing(
    account: Account = Depends(get_current_user_flexible),
    db: Session = Depends(get_db),
    limit: int = 100
):
    """
    Get billing history (alias for /account/transactions)
    Frontend compatibility endpoint
    Supports both JWT and API key authentication
    """
    
    transactions = db.query(Transaction).filter(
        Transaction.account_id == account.id
    ).order_by(
        Transaction.created_at.desc()
    ).limit(limit).all()
    
    return {
        "account_id": account.id,
        "transactions": [
            {
                "id": txn.id,
                "amount": txn.amount,
                "type": txn.transaction_type,
                "description": txn.description,
                "created_at": txn.created_at.isoformat()
            }
            for txn in transactions
        ],
        "total": len(transactions)
    }

