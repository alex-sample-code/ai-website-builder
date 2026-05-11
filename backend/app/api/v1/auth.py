"""
Authentication endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.user import User
from app.models.tenant import Tenant, TenantPlan
from app.schemas.user import UserRegister, UserLogin, TokenResponse, CurrentUser
from app.auth.cognito import cognito_client
from app.auth.deps import get_current_user
import uuid
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user and create a new tenant.
    This creates both a Cognito user and database records.
    """
    try:
        # Check if user already exists
        result = await db.execute(
            select(User).where(User.email == user_data.email)
        )
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Create tenant first
        tenant = Tenant(
            name=user_data.company_name,
            plan=TenantPlan.FREE.value,
            status="active",
            ai_quota_limit=3
        )
        db.add(tenant)
        await db.flush()

        # Register user in Cognito
        cognito_response = await cognito_client.sign_up(
            email=user_data.email,
            password=user_data.password,
            tenant_id=str(tenant.id),
            name=user_data.name
        )

        # Create user in database
        user = User(
            email=user_data.email,
            name=user_data.name,
            cognito_sub=cognito_response["UserSub"],
            tenant_id=tenant.id,
            role="owner"
        )
        db.add(user)
        await db.commit()

        # Authenticate and get tokens
        auth_response = await cognito_client.initiate_auth(
            email=user_data.email,
            password=user_data.password
        )

        return TokenResponse(
            access_token=auth_response["AuthenticationResult"]["AccessToken"],
            refresh_token=auth_response["AuthenticationResult"].get("RefreshToken"),
            token_type="bearer",
            expires_in=auth_response["AuthenticationResult"]["ExpiresIn"]
        )

    except HTTPException:
        await db.rollback()
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )


@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """
    Authenticate user with email and password.
    Returns JWT tokens from Cognito.
    """
    try:
        # Authenticate with Cognito
        auth_response = await cognito_client.initiate_auth(
            email=credentials.email,
            password=credentials.password
        )

        # Update last login time
        result = await db.execute(
            select(User).where(User.email == credentials.email)
        )
        user = result.scalar_one_or_none()
        if user:
            from datetime import datetime, timezone
            user.last_login_at = datetime.now(timezone.utc)
            await db.commit()

        return TokenResponse(
            access_token=auth_response["AuthenticationResult"]["AccessToken"],
            refresh_token=auth_response["AuthenticationResult"].get("RefreshToken"),
            token_type="bearer",
            expires_in=auth_response["AuthenticationResult"]["ExpiresIn"]
        )

    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_token: str):
    """
    Refresh access token using refresh token.
    """
    try:
        auth_response = await cognito_client.refresh_token(refresh_token)

        return TokenResponse(
            access_token=auth_response["AuthenticationResult"]["AccessToken"],
            token_type="bearer",
            expires_in=auth_response["AuthenticationResult"]["ExpiresIn"]
        )

    except Exception as e:
        logger.error(f"Token refresh error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )


@router.get("/me", response_model=CurrentUser)
async def get_current_user_info(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get current authenticated user information.
    """
    # Fetch tenant info
    result = await db.execute(
        select(Tenant).where(Tenant.id == user.tenant_id)
    )
    tenant = result.scalar_one_or_none()

    return CurrentUser(
        id=user.id,
        email=user.email,
        name=user.name,
        tenant_id=user.tenant_id,
        cognito_sub=user.cognito_sub,
        role=user.role,
        avatar_url=user.avatar_url,
        last_login_at=user.last_login_at,
        created_at=user.created_at,
        updated_at=user.updated_at,
        tenant_name=tenant.name if tenant else None,
        tenant_plan=tenant.plan if tenant else None
    )


@router.post("/forgot-password")
async def forgot_password(email: str):
    """
    Initiate forgot password flow.
    Sends a verification code to the user's email.
    """
    try:
        await cognito_client.forgot_password(email)
        return {"message": "Password reset code sent to email"}

    except Exception as e:
        logger.error(f"Forgot password error: {e}")
        # Don't reveal if email exists or not
        return {"message": "If the email exists, a reset code will be sent"}
