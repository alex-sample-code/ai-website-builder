"""
Site schemas
"""

from pydantic import Field
from datetime import datetime
from uuid import UUID
from typing import Dict, Any
from app.schemas.common import BaseSchema, TimestampSchema, IDSchema


class SiteBase(BaseSchema):
    """Base site schema"""

    name: str = Field(..., min_length=1, max_length=255)


class SiteCreate(SiteBase):
    """Schema for creating a site"""

    template_id: str | None = None


class SiteUpdate(BaseSchema):
    """Schema for updating a site"""

    name: str | None = Field(None, min_length=1, max_length=255)
    status: str | None = Field(None, pattern="^(draft|published|offline)$")


class SiteResponse(SiteBase, IDSchema, TimestampSchema):
    """Schema for site response"""

    tenant_id: UUID
    status: str
    template_id: str | None = None
    current_version_id: UUID | None = None
    published_at: datetime | None = None
    publish_url: str | None = None
    settings_snapshot: Dict[str, Any] | None = None


class SiteDetail(SiteResponse):
    """Detailed site schema with page count"""

    page_count: int | None = None
    total_submissions: int | None = None


class SitePublishRequest(BaseSchema):
    """Schema for site publish request"""

    notes: str | None = None


class SitePublishResponse(BaseSchema):
    """Schema for site publish response"""

    version_id: UUID
    version_number: int
    publish_url: str
    published_at: datetime
