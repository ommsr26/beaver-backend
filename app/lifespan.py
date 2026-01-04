from contextlib import asynccontextmanager
import httpx
import redis.asyncio as redis
from app.config import settings

@asynccontextmanager
async def lifespan(app):
    """
    Runs once when server starts and once when it stops
    """

    # 🔥 Startup (runs once)
    app.state.http_client = httpx.AsyncClient(
        timeout=60.0,
        limits=httpx.Limits(
            max_connections=200,
            max_keepalive_connections=50
        )
    )

    app.state.redis = redis.from_url(
        settings.REDIS_URL,
        decode_responses=True
    )

    yield

    # 🧹 Shutdown (runs once)
    await app.state.http_client.aclose()
    await app.state.redis.close()
