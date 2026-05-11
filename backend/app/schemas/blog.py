"""
Blog schemas
"""

from pydantic import Field
from datetime import datetime
from uuid import UUID
from app.schemas.common import BaseSchema, TimestampSchema, IDSchema


# Blog Post schemas
class BlogPostBase(BaseSchema):
    """Base blog post schema"""

    title: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255, pattern=r"^[a-z0-9-]+$")
    content: str | None = None
    excerpt: str | None = Field(None, max_length=500)


class BlogPostCreate(BlogPostBase):
    """Schema for creating a blog post"""

    category_id: UUID | None = None
    cover_image: str | None = None
    seo_title: str | None = None
    seo_description: str | None = None
    author_name: str | None = None
    status: str = Field(default="draft", pattern="^(draft|published|archived)$")
    scheduled_at: datetime | None = None
    tag_ids: list[UUID] = []


class BlogPostUpdate(BaseSchema):
    """Schema for updating a blog post"""

    title: str | None = Field(None, min_length=1, max_length=255)
    slug: str | None = Field(None, min_length=1, max_length=255, pattern=r"^[a-z0-9-]+$")
    content: str | None = None
    content_html: str | None = None
    excerpt: str | None = Field(None, max_length=500)
    category_id: UUID | None = None
    cover_image: str | None = None
    seo_title: str | None = None
    seo_description: str | None = None
    author_name: str | None = None
    status: str | None = Field(None, pattern="^(draft|published|archived)$")
    scheduled_at: datetime | None = None
    tag_ids: list[UUID] | None = None


class BlogPostResponse(BlogPostBase, IDSchema, TimestampSchema):
    """Schema for blog post response"""

    site_id: UUID
    category_id: UUID | None = None
    content_html: str | None = None
    cover_image: str | None = None
    seo_title: str | None = None
    seo_description: str | None = None
    author_name: str | None = None
    status: str
    published_at: datetime | None = None
    scheduled_at: datetime | None = None


# Blog Category schemas
class BlogCategoryBase(BaseSchema):
    """Base blog category schema"""

    name: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255, pattern=r"^[a-z0-9-]+$")


class BlogCategoryCreate(BlogCategoryBase):
    """Schema for creating a blog category"""

    sort_order: int = 0


class BlogCategoryUpdate(BaseSchema):
    """Schema for updating a blog category"""

    name: str | None = Field(None, min_length=1, max_length=255)
    slug: str | None = Field(None, min_length=1, max_length=255, pattern=r"^[a-z0-9-]+$")
    sort_order: int | None = None


class BlogCategoryResponse(BlogCategoryBase, IDSchema):
    """Schema for blog category response"""

    site_id: UUID
    sort_order: int


# Blog Tag schemas
class BlogTagBase(BaseSchema):
    """Base blog tag schema"""

    name: str = Field(..., min_length=1, max_length=100)
    slug: str = Field(..., min_length=1, max_length=100, pattern=r"^[a-z0-9-]+$")


class BlogTagCreate(BlogTagBase):
    """Schema for creating a blog tag"""
    pass


class BlogTagResponse(BlogTagBase, IDSchema):
    """Schema for blog tag response"""

    site_id: UUID
