"""
Tenant schemas
"""

from pydantic import Field
from datetime import datetime
from uuid import UUID
from app.schemas.common import BaseSchema, TimestampSchema, IDSchema


class TenantBase(BaseSchema):
    """Base tenant schema"""

    name: str = Field(..., min_length=1, max_length=255)
    plan: str = Field(default="free", pattern="^(free|pro|enterprise)$")


class TenantCreate(TenantBase):
    """Schema for creating a tenant"""
    pass


class TenantUpdate(BaseSchema):
    """Schema for updating a tenant"""

    name: str | None = Field(None, min_length=1, max_length=255)
    plan: str | None = Field(None, pattern="^(free|pro|enterprise)$")
    custom_domain: str | None = None
    ai_quota_limit: int | None = None


class TenantResponse(TenantBase, IDSchema, TimestampSchema):
    """Schema for tenant response"""

    custom_domain: str | None = None
    cf_tenant_id: str | None = None
    cf_connection_group_id: str | None = None
    domain_status: str
    status: str
    ai_quota_used: int
    ai_quota_limit: int


class TenantDetail(TenantResponse):
    """Detailed tenant schema with relationships"""

    # Can add related data here if needed
    pass
