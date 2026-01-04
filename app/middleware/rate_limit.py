from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.rate_limiter import rate_limiter


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip middleware if api_key not in state (e.g., health check endpoints)
        if not hasattr(request.state, "api_key"):
            return await call_next(request)
        
        api_key_data = request.state.api_key
        api_key = api_key_data.key
        
        # Use default plan for all accounts (can be enhanced later)
        plan = "pro"

        allowed = rate_limiter.is_allowed(
            api_key=api_key,
            plan=plan
        )

        if not allowed:
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded"
            )

        response = await call_next(request)
        return response
