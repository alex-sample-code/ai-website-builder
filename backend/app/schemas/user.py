"""
User schemas
"""

from pydantic import EmailStr, Field
from datetime import datetime
from uuid import UUID
from app.schemas.common import BaseSchema, TimestampSchema, IDSchema


class UserBase(BaseSchema):
    """Base user schema"""

    email: EmailStr
    name: str = Field(..., min_length=1, max_length=255)


class UserCreate(UserBase):
    """Schema for creating a user"""

    password: str = Field(..., min_length=8)
    tenant_id: UUID | None = None
    role: str = Field(default="owner", pattern="^(owner|editor|viewer)$")


class UserUpdate(BaseSchema):
    """Schema for updating a user"""

    name: str | None = Field(None, min_length=1, max_length=255)
    avatar_url: str | None = None
    role: str | None = Field(None, pattern="^(owner|editor|viewer)$")


class UserResponse(UserBase, IDSchema, TimestampSchema):
    """Schema for user response"""

    tenant_id: UUID
    cognito_sub: str
    role: str
    avatar_url: str | None = None
    last_login_at: datetime | None = None


class UserLogin(BaseSchema):
    """Schema for user login"""

    email: EmailStr
    password: str


class UserRegister(UserBase):
    """Schema for user registration"""

    password: str = Field(..., min_length=8)
    company_name: str = Field(..., min_length=1, max_length=255)


class TokenResponse(BaseSchema):
    """Schema for token response"""

    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"
    expires_in: int


class CurrentUser(UserResponse):
    """Schema for current authenticated user"""

    tenant_name: str | None = None
    tenant_plan: str | None = None
