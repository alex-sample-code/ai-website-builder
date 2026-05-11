"""
Integration schemas
"""

from pydantic import Field
from datetime import datetime
from uuid import UUID
from typing import Dict, Any
from app.schemas.common import BaseSchema, IDSchema


class IntegrationBase(BaseSchema):
    """Base integration schema"""

    type: str = Field(..., min_length=1, max_length=50)
    config: Dict[str, Any] = {}
    is_enabled: bool = True


class IntegrationUpsert(IntegrationBase):
    """Schema for creating/updating an integration"""
    pass


class IntegrationResponse(IntegrationBase, IDSchema):
    """Schema for integration response"""

    site_id: UUID
    created_at: datetime
    updated_at: datetime
