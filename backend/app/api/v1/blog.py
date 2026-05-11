"""
Blog management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from typing import List
from uuid import UUID
from datetime import datetime
import markdown
import bleach
from app.database import get_db
from app.models.blog import BlogPost, BlogCategory, BlogTag, blog_post_tags
from app.models.site import Site
from app.models.tenant import Tenant
from app.models.user import User
from app.schemas.blog import (
    BlogPostCreate, BlogPostUpdate, BlogPostResponse,
    BlogCategoryCreate, BlogCategoryUpdate, BlogCategoryResponse,
    BlogTagCreate, BlogTagResponse
)
from app.auth.deps import get_current_user, get_current_tenant
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/posts", response_model=List[BlogPostResponse])
async def list_blog_posts(
    site_id: UUID,
    status_filter: str | None = Query(None, pattern="^(draft|published|archived)$"),
    category_id: UUID | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all blog posts for a site with optional filtering and pagination.
    """
    # Verify site belongs to tenant
    site_result = await db.execute(
        select(Site).where(Site.id == site_id, Site.tenant_id == tenant.id)
    )
    site = site_result.scalar_one_or_none()
    if not site:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site not found")

    # Build query
    query = select(BlogPost).where(BlogPost.site_id == site_id)

    if status_filter:
        query = query.where(BlogPost.status == status_filter)
    if category_id:
        query = query.where(BlogPost.category_id == category_id)

    query = query.order_by(BlogPost.created_at.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)

    result = await db.execute(query)
    posts = result.scalars().all()
    return posts


@router.post("/posts", response_model=BlogPostResponse, status_code=status.HTTP_201_CREATED)
async def create_blog_post(
    site_id: UUID,
    post_data: BlogPostCreate,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new blog post.
    """
    # Verify site belongs to tenant
    site_result = await db.execute(
        select(Site).where(Site.id == site_id, Site.tenant_id == tenant.id)
    )
    site = site_result.scalar_one_or_none()
    if not site:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site not found")

    # Convert markdown to HTML if content provided
    content_html = None
    if post_data.content:
        html = markdown.markdown(post_data.content, extensions=['extra', 'codehilite'])
        content_html = bleach.clean(
            html,
            tags=['p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                  'ul', 'ol', 'li', 'a', 'img', 'blockquote', 'code', 'pre', 'hr'],
            attributes={'a': ['href', 'title'], 'img': ['src', 'alt', 'title']}
        )

    # Create post
    post = BlogPost(
        site_id=site_id,
        category_id=post_data.category_id,
        title=post_data.title,
        slug=post_data.slug,
        content=post_data.content,
        content_html=content_html,
        excerpt=post_data.excerpt,
        cover_image=post_data.cover_image,
        seo_title=post_data.seo_title,
        seo_description=post_data.seo_description,
        author_name=post_data.author_name or user.name,
        status=post_data.status,
        scheduled_at=post_data.scheduled_at,
        published_at=datetime.utcnow() if post_data.status == "published" else None
    )

    db.add(post)
    await db.flush()

    # Handle tags
    if post_data.tag_ids:
        for tag_id in post_data.tag_ids:
            await db.execute(
                blog_post_tags.insert().values(post_id=post.id, tag_id=tag_id)
            )

    await db.commit()
    await db.refresh(post)

    logger.info(f"Blog post created: {post.id} by user {user.id}")
    return post


@router.get("/posts/{post_id}", response_model=BlogPostResponse)
async def get_blog_post(
    site_id: UUID,
    post_id: UUID,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific blog post by ID.
    """
    result = await db.execute(
        select(BlogPost).join(Site).where(
            BlogPost.id == post_id,
            BlogPost.site_id == site_id,
            Site.tenant_id == tenant.id
        )
    )
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog post not found")

    return post


@router.put("/posts/{post_id}", response_model=BlogPostResponse)
async def update_blog_post(
    site_id: UUID,
    post_id: UUID,
    post_data: BlogPostUpdate,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Update a blog post.
    """
    result = await db.execute(
        select(BlogPost).join(Site).where(
            BlogPost.id == post_id,
            BlogPost.site_id == site_id,
            Site.tenant_id == tenant.id
        )
    )
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog post not found")

    # Update fields
    if post_data.title is not None:
        post.title = post_data.title
    if post_data.slug is not None:
        post.slug = post_data.slug
    if post_data.content is not None:
        post.content = post_data.content
        # Regenerate HTML from markdown
        html = markdown.markdown(post_data.content, extensions=['extra', 'codehilite'])
        post.content_html = bleach.clean(
            html,
            tags=['p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                  'ul', 'ol', 'li', 'a', 'img', 'blockquote', 'code', 'pre', 'hr'],
            attributes={'a': ['href', 'title'], 'img': ['src', 'alt', 'title']}
        )
    if post_data.content_html is not None:
        post.content_html = post_data.content_html
    if post_data.excerpt is not None:
        post.excerpt = post_data.excerpt
    if post_data.category_id is not None:
        post.category_id = post_data.category_id
    if post_data.cover_image is not None:
        post.cover_image = post_data.cover_image
    if post_data.seo_title is not None:
        post.seo_title = post_data.seo_title
    if post_data.seo_description is not None:
        post.seo_description = post_data.seo_description
    if post_data.author_name is not None:
        post.author_name = post_data.author_name
    if post_data.status is not None:
        # Update published_at if transitioning to published
        if post_data.status == "published" and post.status != "published":
            post.published_at = datetime.utcnow()
        post.status = post_data.status
    if post_data.scheduled_at is not None:
        post.scheduled_at = post_data.scheduled_at

    # Handle tag updates
    if post_data.tag_ids is not None:
        # Remove existing tags
        await db.execute(
            blog_post_tags.delete().where(blog_post_tags.c.post_id == post_id)
        )
        # Add new tags
        for tag_id in post_data.tag_ids:
            await db.execute(
                blog_post_tags.insert().values(post_id=post.id, tag_id=tag_id)
            )

    await db.commit()
    await db.refresh(post)

    logger.info(f"Blog post updated: {post.id} by user {user.id}")
    return post


@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog_post(
    site_id: UUID,
    post_id: UUID,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a blog post.
    """
    result = await db.execute(
        select(BlogPost).join(Site).where(
            BlogPost.id == post_id,
            BlogPost.site_id == site_id,
            Site.tenant_id == tenant.id
        )
    )
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog post not found")

    await db.delete(post)
    await db.commit()

    logger.info(f"Blog post deleted: {post_id} by user {user.id}")
    return None


# Category endpoints
@router.get("/categories", response_model=List[BlogCategoryResponse])
async def list_blog_categories(
    site_id: UUID,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all blog categories for a site.
    """
    # Verify site belongs to tenant
    site_result = await db.execute(
        select(Site).where(Site.id == site_id, Site.tenant_id == tenant.id)
    )
    site = site_result.scalar_one_or_none()
    if not site:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site not found")

    result = await db.execute(
        select(BlogCategory).where(BlogCategory.site_id == site_id).order_by(BlogCategory.sort_order)
    )
    categories = result.scalars().all()
    return categories


@router.post("/categories", response_model=BlogCategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_blog_category(
    site_id: UUID,
    category_data: BlogCategoryCreate,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new blog category.
    """
    # Verify site belongs to tenant
    site_result = await db.execute(
        select(Site).where(Site.id == site_id, Site.tenant_id == tenant.id)
    )
    site = site_result.scalar_one_or_none()
    if not site:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site not found")

    category = BlogCategory(
        site_id=site_id,
        name=category_data.name,
        slug=category_data.slug,
        sort_order=category_data.sort_order
    )

    db.add(category)
    await db.commit()
    await db.refresh(category)

    logger.info(f"Blog category created: {category.id} by user {user.id}")
    return category


# Tag endpoints
@router.get("/tags", response_model=List[BlogTagResponse])
async def list_blog_tags(
    site_id: UUID,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all blog tags for a site.
    """
    # Verify site belongs to tenant
    site_result = await db.execute(
        select(Site).where(Site.id == site_id, Site.tenant_id == tenant.id)
    )
    site = site_result.scalar_one_or_none()
    if not site:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site not found")

    result = await db.execute(
        select(BlogTag).where(BlogTag.site_id == site_id).order_by(BlogTag.name)
    )
    tags = result.scalars().all()
    return tags
