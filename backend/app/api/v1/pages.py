"""
Page management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID
from app.database import get_db
from app.models.site import Site
from app.models.page import Page
from app.models.tenant import Tenant
from app.models.user import User
from app.schemas.page import (
    PageCreate,
    PageUpdate,
    PageContentUpdate,
    PageResponse,
    PageDetail,
    PageReorderRequest
)
from app.auth.deps import get_current_user, get_current_tenant
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


async def get_site_or_404(
    site_id: UUID,
    tenant_id: UUID,
    db: AsyncSession
) -> Site:
    """Helper to get site and verify ownership"""
    result = await db.execute(
        select(Site).where(Site.id == site_id, Site.tenant_id == tenant_id)
    )
    site = result.scalar_one_or_none()
    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site not found"
        )
    return site


@router.get("", response_model=List[PageResponse])
async def list_pages(
    site_id: UUID,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all pages for a site.
    """
    # Verify site ownership
    await get_site_or_404(site_id, tenant.id, db)

    result = await db.execute(
        select(Page).where(Page.site_id == site_id).order_by(Page.sort_order)
    )
    pages = result.scalars().all()
    return pages


@router.post("", response_model=PageResponse, status_code=status.HTTP_201_CREATED)
async def create_page(
    site_id: UUID,
    page_data: PageCreate,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new page.
    """
    # Verify site ownership
    await get_site_or_404(site_id, tenant.id, db)

    # Check for slug uniqueness
    result = await db.execute(
        select(Page).where(Page.site_id == site_id, Page.slug == page_data.slug)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Page with slug '{page_data.slug}' already exists"
        )

    # If this is set as homepage, unset other homepage
    if page_data.is_homepage:
        await db.execute(
            select(Page).where(Page.site_id == site_id, Page.is_homepage == True)
        )
        # Update existing homepage
        result = await db.execute(
            select(Page).where(Page.site_id == site_id, Page.is_homepage == True)
        )
        existing_homepage = result.scalar_one_or_none()
        if existing_homepage:
            existing_homepage.is_homepage = False

    page = Page(
        site_id=site_id,
        slug=page_data.slug,
        title=page_data.title,
        seo_meta=page_data.seo_meta,
        grapesjs_data=page_data.grapesjs_data,
        html=page_data.html,
        css=page_data.css,
        js=page_data.js,
        is_homepage=page_data.is_homepage,
        sort_order=page_data.sort_order,
        status="active"
    )
    db.add(page)
    await db.commit()
    await db.refresh(page)

    logger.info(f"Page created: {page.id} for site {site_id}")
    return page


@router.get("/{page_id}", response_model=PageDetail)
async def get_page(
    site_id: UUID,
    page_id: UUID,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific page with full content.
    """
    # Verify site ownership
    await get_site_or_404(site_id, tenant.id, db)

    result = await db.execute(
        select(Page).where(Page.id == page_id, Page.site_id == site_id)
    )
    page = result.scalar_one_or_none()

    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Page not found"
        )

    return page


@router.put("/{page_id}", response_model=PageResponse)
async def update_page(
    site_id: UUID,
    page_id: UUID,
    page_data: PageUpdate,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Update a page.
    """
    # Verify site ownership
    await get_site_or_404(site_id, tenant.id, db)

    result = await db.execute(
        select(Page).where(Page.id == page_id, Page.site_id == site_id)
    )
    page = result.scalar_one_or_none()

    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Page not found"
        )

    # Update fields
    update_data = page_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(page, field, value)

    # Handle homepage logic
    if page_data.is_homepage is True and not page.is_homepage:
        # Unset other homepages
        result = await db.execute(
            select(Page).where(
                Page.site_id == site_id,
                Page.is_homepage == True,
                Page.id != page_id
            )
        )
        existing_homepage = result.scalar_one_or_none()
        if existing_homepage:
            existing_homepage.is_homepage = False

    await db.commit()
    await db.refresh(page)

    logger.info(f"Page updated: {page_id}")
    return page


@router.put("/{page_id}/content", response_model=PageResponse)
async def update_page_content(
    site_id: UUID,
    page_id: UUID,
    content_data: PageContentUpdate,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Quick update of page content (GrapesJS data only).
    """
    # Verify site ownership
    await get_site_or_404(site_id, tenant.id, db)

    result = await db.execute(
        select(Page).where(Page.id == page_id, Page.site_id == site_id)
    )
    page = result.scalar_one_or_none()

    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Page not found"
        )

    page.grapesjs_data = content_data.grapesjs_data
    await db.commit()
    await db.refresh(page)

    return page


@router.delete("/{page_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_page(
    site_id: UUID,
    page_id: UUID,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a page.
    """
    # Verify site ownership
    await get_site_or_404(site_id, tenant.id, db)

    result = await db.execute(
        select(Page).where(Page.id == page_id, Page.site_id == site_id)
    )
    page = result.scalar_one_or_none()

    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Page not found"
        )

    await db.delete(page)
    await db.commit()

    logger.info(f"Page deleted: {page_id}")
    return None


@router.put("/reorder", status_code=status.HTTP_204_NO_CONTENT)
async def reorder_pages(
    site_id: UUID,
    reorder_data: PageReorderRequest,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Reorder pages by providing a list of page IDs in desired order.
    """
    # Verify site ownership
    await get_site_or_404(site_id, tenant.id, db)

    # Update sort_order for each page
    for idx, page_id in enumerate(reorder_data.page_ids):
        result = await db.execute(
            select(Page).where(Page.id == page_id, Page.site_id == site_id)
        )
        page = result.scalar_one_or_none()
        if page:
            page.sort_order = idx

    await db.commit()
    logger.info(f"Pages reordered for site {site_id}")
    return None
