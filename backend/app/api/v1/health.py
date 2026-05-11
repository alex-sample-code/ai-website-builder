"""
Health check endpoints
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.database import get_db
from app.config import settings
import redis.asyncio as redis

router = APIRouter()


@router.get("/health")
async def health_check():
    """Basic health check"""
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }


@router.get("/health/db")
async def health_check_db(db: AsyncSession = Depends(get_db)):
    """Health check with database connectivity"""
    try:
        await db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "database": db_status,
        "version": settings.VERSION
    }


@router.get("/health/full")
async def health_check_full(db: AsyncSession = Depends(get_db)):
    """Full health check including all services"""
    checks = {}

    # Database check
    try:
        await db.execute(text("SELECT 1"))
        checks["database"] = "healthy"
    except Exception as e:
        checks["database"] = f"unhealthy: {str(e)}"

    # Redis check
    try:
        redis_client = redis.from_url(settings.REDIS_URL)
        await redis_client.ping()
        await redis_client.close()
        checks["redis"] = "healthy"
    except Exception as e:
        checks["redis"] = f"unhealthy: {str(e)}"

    # Overall status
    all_healthy = all(status == "healthy" for status in checks.values())
    overall_status = "healthy" if all_healthy else "degraded"

    return {
        "status": overall_status,
        "checks": checks,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }
