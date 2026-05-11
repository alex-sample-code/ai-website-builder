"""
FastAPI application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import sys

from app.config import settings
from app.database import init_db, close_db
from app.api.v1 import api_router

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    """
    # Startup
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")

    # Initialize database (create tables if needed - for development)
    if settings.ENVIRONMENT == "development" and settings.DEBUG:
        try:
            logger.info("Initializing database...")
            # await init_db()  # Uncomment to auto-create tables
            logger.info("Database initialized")
        except Exception as e:
            logger.error(f"Database initialization error: {e}")

    yield

    # Shutdown
    logger.info("Shutting down application...")
    try:
        await close_db()
        logger.info("Database connections closed")
    except Exception as e:
        logger.error(f"Error closing database: {e}")


# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for AI-powered website building platform",
    version=settings.VERSION,
    docs_url="/api/docs" if settings.DEBUG else None,
    redoc_url="/api/redoc" if settings.DEBUG else None,
    openapi_url="/api/openapi.json" if settings.DEBUG else None,
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Trusted host middleware (for production)
# Note: disabled to allow ALB health checks which use IP as Host header
# if settings.ENVIRONMENT == "production":
#     app.add_middleware(
#         TrustedHostMiddleware,
#         allowed_hosts=["api.chinabjalex.com", "*.chinabjalex.com", "localhost"]
#     )


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": f"{settings.PROJECT_NAME} API",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "docs": "/api/docs" if settings.DEBUG else None
    }


@app.get("/health")
async def health_check():
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handle uncaught exceptions"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error" if settings.ENVIRONMENT == "production" else str(exc)
        }
    )


# Include API v1 router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)

logger.info("Application initialized successfully")
