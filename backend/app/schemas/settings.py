"""
Site settings and navigation menu schemas
"""

from pydantic import Field
from uuid import UUID
from typing import Dict, Any
from app.schemas.common import BaseSchema, IDSchema


# Site Settings schemas
class SiteSettingsBase(BaseSchema):
    """Base site settings schema"""

    logo_url: str | None = None
    favicon_url: str | None = None
    company_name: str | None = Field(None, max_length=255)
    company_address: str | None = None
    company_phone: str | None = Field(None, max_length=50)
    company_email: str | None = Field(None, max_length=255)
    social_links: Dict[str, str] | None = None
    analytics_id: str | None = Field(None, max_length=255)
    custom_head_code: str | None = None
    custom_body_code: str | None = None
    color_scheme: Dict[str, str] | None = None
    font_family: str | None = Field(None, max_length=255)


class SiteSettingsUpdate(SiteSettingsBase):
    """Schema for updating site settings"""
    pass


class SiteSettingsResponse(SiteSettingsBase, IDSchema):
    """Schema for site settings response"""

    site_id: UUID


# Navigation Menu schemas
class NavMenuBase(BaseSchema):
    """Base navigation menu schema"""

    position: str = Field(..., pattern="^(header|footer|sidebar)$")
    items: list[Dict[str, Any]] = []


class NavMenuUpdate(BaseSchema):
    """Schema for updating navigation menu"""

    items: list[Dict[str, Any]]


class NavMenuResponse(NavMenuBase, IDSchema):
    """Schema for navigation menu response"""

    site_id: UUID
