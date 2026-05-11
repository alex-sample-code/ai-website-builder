"""
Site version schemas
"""

from pydantic import Field
from datetime import datetime
from uuid import UUID
from typing import Dict, Any
from app.schemas.common import BaseSchema, IDSchema


class SiteVersionResponse(IDSchema):
    """Schema for site version response"""

    site_id: UUID
    version_number: int
    snapshot: Dict[str, Any] | None = None
    s3_prefix: str | None = None
    published_by: UUID | None = None
    published_at: datetime
    is_current: bool
    notes: str | None = None


class SiteVersionRollbackRequest(BaseSchema):
    """Schema for version rollback request"""

    version_id: UUID = Field(..., description="Version ID to rollback to")
