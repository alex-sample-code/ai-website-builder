"""
Site management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
from uuid import UUID
from app.database import get_db
from app.models.site import Site
from app.models.tenant import Tenant
from app.models.user import User
from app.models.form import FormSubmission
from app.schemas.site import SiteCreate, SiteUpdate, SiteResponse, SiteDetail
from app.auth.deps import get_current_user, get_current_tenant
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("", response_model=List[SiteResponse])
async def list_sites(
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all sites for the current tenant.
    """
    result = await db.execute(
        select(Site).where(Site.tenant_id == tenant.id).order_by(Site.created_at.desc())
    )
    sites = result.scalars().all()
    return sites


@router.post("", response_model=SiteResponse, status_code=status.HTTP_201_CREATED)
async def create_site(
    site_data: SiteCreate,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new site.
    """
    site = Site(
        tenant_id=tenant.id,
        name=site_data.name,
        template_id=site_data.template_id,
        status="draft"
    )
    db.add(site)
    await db.commit()
    await db.refresh(site)

    logger.info(f"Site created: {site.id} by user {user.id}")
    return site


@router.get("/{site_id}", response_model=SiteDetail)
async def get_site(
    site_id: UUID,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific site by ID.
    """
    result = await db.execute(
        select(Site).where(Site.id == site_id, Site.tenant_id == tenant.id)
    )
    site = result.scalar_one_or_none()

    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site not found"
        )

    # Get page count
    page_count_result = await db.execute(
        select(func.count()).select_from(site.pages.__class__).where(
            site.pages.__class__.site_id == site_id
        )
    )
    page_count = page_count_result.scalar()

    # Get submission count
    submission_count_result = await db.execute(
        select(func.count()).select_from(FormSubmission).where(
            FormSubmission.site_id == site_id
        )
    )
    submission_count = submission_count_result.scalar()

    # Convert to response schema
    site_dict = {
        "id": site.id,
        "tenant_id": site.tenant_id,
        "name": site.name,
        "status": site.status,
        "template_id": site.template_id,
        "current_version_id": site.current_version_id,
        "published_at": site.published_at,
        "publish_url": site.publish_url,
        "settings_snapshot": site.settings_snapshot,
        "created_at": site.created_at,
        "updated_at": site.updated_at,
        "page_count": page_count,
        "total_submissions": submission_count
    }

    return SiteDetail(**site_dict)


@router.put("/{site_id}", response_model=SiteResponse)
async def update_site(
    site_id: UUID,
    site_data: SiteUpdate,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Update a site.
    """
    result = await db.execute(
        select(Site).where(Site.id == site_id, Site.tenant_id == tenant.id)
    )
    site = result.scalar_one_or_none()

    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site not found"
        )

    # Update fields
    if site_data.name is not None:
        site.name = site_data.name
    if site_data.status is not None:
        site.status = site_data.status

    await db.commit()
    await db.refresh(site)

    logger.info(f"Site updated: {site.id} by user {user.id}")
    return site


@router.delete("/{site_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_site(
    site_id: UUID,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a site (soft delete by setting status to deleted).
    """
    # Only owners can delete sites
    if user.role != "owner":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only owners can delete sites"
        )

    result = await db.execute(
        select(Site).where(Site.id == site_id, Site.tenant_id == tenant.id)
    )
    site = result.scalar_one_or_none()

    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site not found"
        )

    # Soft delete
    await db.delete(site)
    await db.commit()

    logger.info(f"Site deleted: {site_id} by user {user.id}")
    return None
