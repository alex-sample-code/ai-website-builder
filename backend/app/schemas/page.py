"""
Page schemas
"""

from pydantic import Field
from uuid import UUID
from typing import Dict, Any
from app.schemas.common import BaseSchema, TimestampSchema, IDSchema


class PageBase(BaseSchema):
    """Base page schema"""

    slug: str = Field(..., min_length=1, max_length=255, pattern=r"^[a-z0-9-]+$")
    title: str = Field(..., min_length=1, max_length=255)


class PageCreate(PageBase):
    """Schema for creating a page"""

    seo_meta: Dict[str, Any] | None = None
    grapesjs_data: Dict[str, Any] | None = None
    html: str | None = None
    css: str | None = None
    js: str | None = None
    is_homepage: bool = False
    sort_order: int = 0


class PageUpdate(BaseSchema):
    """Schema for updating a page"""

    slug: str | None = Field(None, min_length=1, max_length=255, pattern=r"^[a-z0-9-]+$")
    title: str | None = Field(None, min_length=1, max_length=255)
    seo_meta: Dict[str, Any] | None = None
    grapesjs_data: Dict[str, Any] | None = None
    html: str | None = None
    css: str | None = None
    js: str | None = None
    is_homepage: bool | None = None
    sort_order: int | None = None
    status: str | None = Field(None, pattern="^(active|hidden|deleted)$")


class PageContentUpdate(BaseSchema):
    """Schema for quick content updates"""

    grapesjs_data: Dict[str, Any]


class PageResponse(PageBase, IDSchema, TimestampSchema):
    """Schema for page response"""

    site_id: UUID
    seo_meta: Dict[str, Any] | None = None
    is_homepage: bool
    sort_order: int
    status: str


class PageDetail(PageResponse):
    """Detailed page schema with full content"""

    grapesjs_data: Dict[str, Any] | None = None
    html: str | None = None
    css: str | None = None
    js: str | None = None


class PageReorderRequest(BaseSchema):
    """Schema for reordering pages"""

    page_ids: list[UUID]
