"""
Common schemas and base classes
"""

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID


class BaseSchema(BaseModel):
    """Base schema with common configuration"""

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )


class TimestampSchema(BaseModel):
    """Schema for timestamp fields"""

    created_at: datetime
    updated_at: datetime


class IDSchema(BaseModel):
    """Schema for ID field"""

    id: UUID


class PaginationParams(BaseModel):
    """Pagination parameters"""

    page: int = 1
    page_size: int = 20


class PaginatedResponse(BaseModel):
    """Paginated response wrapper"""

    items: list
    total: int
    page: int
    page_size: int
    total_pages: int
