"""
Asset schemas
"""

from pydantic import Field
from datetime import datetime
from uuid import UUID
from app.schemas.common import BaseSchema, IDSchema


class AssetBase(BaseSchema):
    """Base asset schema"""

    filename: str = Field(..., min_length=1, max_length=255)
    folder: str | None = Field(None, max_length=255)


class AssetUploadRequest(BaseSchema):
    """Schema for requesting asset upload presigned URL"""

    filename: str = Field(..., min_length=1, max_length=255)
    content_type: str = Field(..., min_length=1, max_length=100)
    folder: str | None = Field(None, max_length=255)


class AssetUploadResponse(BaseSchema):
    """Schema for asset upload response"""

    asset_id: UUID
    upload_url: str
    cdn_url: str


class AssetResponse(AssetBase, IDSchema):
    """Schema for asset response"""

    tenant_id: UUID
    site_id: UUID | None = None
    s3_key: str
    cdn_url: str
    content_type: str
    size_bytes: int
    width: int | None = None
    height: int | None = None
    created_at: datetime
