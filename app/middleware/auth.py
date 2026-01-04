from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session, joinedload

from app.database.db import SessionLocal
from app.database.models import APIKey


class AuthMiddleware(BaseHTTPMiddleware):
    """Extract and validate API key from Authorization header"""
    
    async def dispatch(self, request: Request, call_next):
        # Allow OPTIONS requests for CORS preflight
        if request.method == "OPTIONS":
            return await call_next(request)
        
        # Skip auth for health check and public endpoints
        if request.url.path in ["/health", "/docs", "/openapi.json", "/redoc"]:
            return await call_next(request)
        
        # Allow admin endpoints (account creation, etc.) without auth
        if request.url.path.startswith("/admin"):
            return await call_next(request)
        
        # Allow auth endpoints (register, login) without auth
        if request.url.path.startswith("/auth"):
            return await call_next(request)
        
        authorization = request.headers.get("Authorization")
        
        if not authorization:
            # Only require auth for protected routes
            if "/v1/" in request.url.path or "/account" in request.url.path:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Missing Authorization header"
                )
            return await call_next(request)
        
        if not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Authorization format"
            )
        
        api_key_value = authorization.replace("Bearer ", "").strip()
        
        # Validate API key
        db: Session = SessionLocal()
        try:
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
            
            # Check account balance
            if api_key.account.balance < 0:
                raise HTTPException(
                    status_code=status.HTTP_402_PAYMENT_REQUIRED,
                    detail="Insufficient account balance. Please top up your account."
                )
            
            # Set API key in request state for use by other middleware and routes
            request.state.api_key = api_key
            
        finally:
            db.close()
        
        response = await call_next(request)
        return response

