from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.usage_tracker import usage_tracker


class UsageLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip middleware if api_key not in state (e.g., health check endpoints)
        if not hasattr(request.state, "api_key"):
            return await call_next(request)
        
        api_key_data = request.state.api_key
        # Use default plan for all accounts (can be enhanced later)
        plan = "pro"

        allowed = usage_tracker.increment(
            api_key=api_key_data.key,
            plan=plan
        )

        if not allowed:
            raise HTTPException(
                status_code=402,
                detail="Monthly usage limit exceeded"
            )

        return await call_next(request)
