"""
Template schemas
"""

from pydantic import Field
from typing import Dict, Any
from app.schemas.common import BaseSchema


class TemplateResponse(BaseSchema):
    """Schema for template response"""

    id: str = Field(..., description="Template ID")
    name: str = Field(..., description="Template name")
    description: str | None = Field(None, description="Template description")
    category: str | None = Field(None, description="Template category (industry)")
    preview_url: str | None = Field(None, description="Preview image URL")
    thumbnail_url: str | None = Field(None, description="Thumbnail URL")
    tags: list[str] = []
    metadata: Dict[str, Any] | None = None


class TemplatePreviewResponse(BaseSchema):
    """Schema for template preview response"""

    template_id: str
    preview_url: str
    pages: list[Dict[str, Any]] = []
