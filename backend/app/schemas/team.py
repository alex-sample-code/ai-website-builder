"""
Team and audit log schemas
"""

from pydantic import Field, EmailStr
from datetime import datetime
from uuid import UUID
from typing import Dict, Any
from app.schemas.common import BaseSchema, IDSchema, TimestampSchema


# Team Member schemas
class TeamMemberResponse(IDSchema, TimestampSchema):
    """Schema for team member response"""

    tenant_id: UUID
    email: str
    name: str | None = None
    role: str
    avatar_url: str | None = None
    last_login_at: datetime | None = None


class TeamInviteRequest(BaseSchema):
    """Schema for inviting a team member"""

    email: EmailStr = Field(..., description="Email address of the person to invite")
    role: str = Field(..., pattern="^(owner|editor|viewer)$", description="Role to assign")


class TeamInviteResponse(BaseSchema):
    """Schema for team invitation response"""

    invitation_id: UUID
    email: str
    role: str
    status: str
    expires_at: datetime


class TeamMemberRoleUpdate(BaseSchema):
    """Schema for updating team member role"""

    role: str = Field(..., pattern="^(owner|editor|viewer)$")


# Audit Log schemas
class AuditLogResponse(IDSchema):
    """Schema for audit log response"""

    tenant_id: UUID
    user_id: UUID | None = None
    action: str
    resource_type: str | None = None
    resource_id: UUID | None = None
    details: Dict[str, Any] | None = None
    ip_address: str | None = None
    created_at: datetime
