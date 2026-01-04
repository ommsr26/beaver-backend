from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.lifespan import lifespan
from app.routes.health import router as health_router
from app.routes.protected_test import router as protected_router
from app.routes.chat import router as chat_router
from app.routes.admin import router as admin_router
from app.routes.account import router as account_router
from app.routes.models import router as models_router
from app.routes.auth import router as auth_router
from app.routes.api_keys import router as api_keys_router
from app.routes.status import router as status_router
from app.routes.users import router as users_router
from app.middleware.auth import AuthMiddleware
from app.middleware.rate_limit import RateLimitMiddleware
from app.middleware.usage_limit import UsageLimitMiddleware

app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan
)

# CORS Middleware - Must be added first to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS + ["https://lovable.dev"],
    allow_origin_regex=r"https://.*\.lovable\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create sub-application for /v1 routes
v1_app = FastAPI()

# Apply CORS middleware to /v1 sub-application
v1_app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS + ["https://lovable.dev"],
    allow_origin_regex=r"https://.*\.lovable\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include v1 routes in sub-application
# Note: The routers have /v1 prefix, but when included in a sub-app mounted at /v1,
# FastAPI will handle the routing. The sub-app's CORS middleware will apply to /v1/* requests.
# We include the routers here so CORS applies, and also in main app for original paths.
v1_app.include_router(chat_router)
v1_app.include_router(models_router)

# Mount v1 sub-application at /v1
app.mount("/v1", v1_app)

# Include v1 routes in main app to maintain original paths
app.include_router(chat_router)
app.include_router(models_router)

# Include non-v1 routes in main app
app.include_router(health_router)
app.include_router(protected_router)
app.include_router(admin_router)
app.include_router(account_router)
app.include_router(auth_router)
app.include_router(api_keys_router)
app.include_router(status_router)
app.include_router(users_router)

# Middleware order matters - AuthMiddleware must run first
app.add_middleware(AuthMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(UsageLimitMiddleware)