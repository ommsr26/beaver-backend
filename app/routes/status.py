"""
Status and health endpoints
"""
from fastapi import APIRouter
from datetime import datetime, timedelta
import time

router = APIRouter(prefix="/status")

# Track server start time for uptime calculation
SERVER_START_TIME = datetime.utcnow()


@router.get("/uptime")
async def get_uptime():
    """Get server uptime"""
    uptime = datetime.utcnow() - SERVER_START_TIME
    uptime_seconds = int(uptime.total_seconds())
    
    days = uptime_seconds // 86400
    hours = (uptime_seconds % 86400) // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60
    
    return {
        "uptime_seconds": uptime_seconds,
        "uptime_formatted": f"{days}d {hours}h {minutes}m {seconds}s",
        "uptime_percentage": 99.9,  # Can be calculated from actual downtime logs
        "started_at": SERVER_START_TIME.isoformat()
    }


@router.get("/latency")
async def get_latency():
    """Get average API latency"""
    # This is a placeholder - in production, you'd track actual request latencies
    return {
        "average_latency_ms": 50,
        "p50_latency_ms": 45,
        "p95_latency_ms": 120,
        "p99_latency_ms": 200,
        "note": "Placeholder values - implement actual latency tracking"
    }

