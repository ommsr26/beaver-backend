from fastapi import APIRouter, Depends
from app.auth.api_key import verify_api_key

router = APIRouter()

@router.get("/protected")
async def protected_route(
    api_key = Depends(verify_api_key)
):
    return {
        "message": "You have access to Beaver!",
        "api_key_id": api_key.id,
        "api_key_name": api_key.name,
        "account_id": api_key.account.id,
        "account_balance": api_key.account.balance
    }
