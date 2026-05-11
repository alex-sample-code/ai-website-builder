"""
Database connection and session management
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from app.config import settings

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_pre_ping=True,
    # Use NullPool for local development if needed
    poolclass=NullPool if settings.ENVIRONMENT == "test" else None,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency function to get database session.
    Usage in FastAPI routes:
        async def my_route(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """Initialize database - create all tables if they don't exist"""
    from app.models.base import Base

    # Import all models to register them with Base
    from app.models import (  # noqa: F401
        tenant,
        user,
        site,
        page,
        site_version,
        site_settings,
        nav_menu,
        asset,
        ai_session,
        blog,
        form,
        integration,
        audit_log,
        team_invitation,
    )

    async with engine.begin() as conn:
        # Drop all tables (for development only!)
        if settings.ENVIRONMENT == "development" and settings.DEBUG:
            await conn.run_sync(Base.metadata.drop_all)

        # Create all tables
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """Close database connections"""
    await engine.dispose()
