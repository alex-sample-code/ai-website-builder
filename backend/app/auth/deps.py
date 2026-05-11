"""
Authentication dependencies for FastAPI routes
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Tuple
from uuid import UUID
from app.database import get_db
from app.models.user import User
from app.models.tenant import Tenant
from app.auth.jwt import verify_token
import logging

logger = logging.getLogger(__name__)

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Dependency to get the current authenticated user from JWT token.

    Usage:
        @app.get("/me")
        async def get_me(user: User = Depends(get_current_user)):
            return {"email": user.email}
    """
    token = credentials.credentials

    # Verify JWT token and extract claims
    try:
        payload = verify_token(token)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error verifying token: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

    # Extract user identifier from token
    cognito_sub = payload.get("sub")
    if not cognito_sub:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing subject"
        )

    # Fetch user from database
    result = await db.execute(
        select(User).where(User.cognito_sub == cognito_sub)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user


async def get_current_tenant(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Tenant:
    """
    Dependency to get the current user's tenant.

    Usage:
        @app.get("/tenant/info")
        async def get_tenant_info(tenant: Tenant = Depends(get_current_tenant)):
            return {"name": tenant.name}
    """
    result = await db.execute(
        select(Tenant).where(Tenant.id == user.tenant_id)
    )
    tenant = result.scalar_one_or_none()

    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found"
        )

    if tenant.status != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Tenant is {tenant.status}"
        )

    return tenant


async def get_current_user_and_tenant(
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant)
) -> Tuple[User, Tenant]:
    """
    Dependency to get both current user and tenant.

    Usage:
        @app.get("/dashboard")
        async def dashboard(
            user_tenant: Tuple[User, Tenant] = Depends(get_current_user_and_tenant)
        ):
            user, tenant = user_tenant
            return {"user": user.email, "tenant": tenant.name}
    """
    return (user, tenant)


def require_role(*allowed_roles: str):
    """
    Dependency factory to require specific user roles.

    Usage:
        @app.delete("/sites/{site_id}")
        async def delete_site(
            site_id: UUID,
            user: User = Depends(require_role("owner", "editor"))
        ):
            # Only owners and editors can access this
            ...
    """
    async def check_role(user: User = Depends(get_current_user)) -> User:
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required roles: {', '.join(allowed_roles)}"
            )
        return user

    return check_role


async def get_optional_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(HTTPBearer(auto_error=False)),
    db: AsyncSession = Depends(get_db)
) -> User | None:
    """
    Dependency to get the current user if authenticated, or None if not.
    Useful for public endpoints that optionally use authentication.

    Usage:
        @app.get("/public/posts")
        async def list_posts(user: User | None = Depends(get_optional_user)):
            if user:
                # Show personalized content
            else:
                # Show public content
    """
    if not credentials:
        return None

    try:
        return await get_current_user(credentials, db)
    except HTTPException:
        return None
