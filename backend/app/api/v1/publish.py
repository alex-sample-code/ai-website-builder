"""
Site publishing endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID
from app.database import get_db
from app.models.site import Site
from app.models.site_version import SiteVersion
from app.models.tenant import Tenant
from app.models.user import User
from app.schemas.site import SitePublishRequest, SitePublishResponse
from app.schemas.version import SiteVersionResponse, SiteVersionRollbackRequest
from app.services.publish_service import PublishService
from app.auth.deps import get_current_user, get_current_tenant
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/{site_id}/publish", response_model=SitePublishResponse)
async def publish_site(
    site_id: UUID,
    publish_request: SitePublishRequest,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Publish a site to S3/CloudFront.

    This generates static HTML from all pages and deploys to the CDN.
    """
    # Verify site belongs to tenant
    result = await db.execute(
        select(Site).where(Site.id == site_id, Site.tenant_id == tenant.id)
    )
    site = result.scalar_one_or_none()

    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site not found"
        )

    # Use publish service to generate and deploy site
    publish_service = PublishService(db)

    try:
        version = await publish_service.publish_site(
            site_id=site_id,
            user_id=user.id,
            notes=publish_request.notes
        )

        logger.info(f"Site published: {site_id} version {version.version_number} by user {user.id}")

        return SitePublishResponse(
            version_id=version.id,
            version_number=version.version_number,
            publish_url=site.publish_url or "",
            published_at=version.published_at
        )
    except Exception as e:
        logger.error(f"Failed to publish site {site_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to publish site: {str(e)}"
        )


@router.get("/{site_id}/versions", response_model=List[SiteVersionResponse])
async def list_site_versions(
    site_id: UUID,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all published versions of a site.
    """
    # Verify site belongs to tenant
    result = await db.execute(
        select(Site).where(Site.id == site_id, Site.tenant_id == tenant.id)
    )
    site = result.scalar_one_or_none()

    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site not found"
        )

    # Get versions
    versions_result = await db.execute(
        select(SiteVersion).where(
            SiteVersion.site_id == site_id
        ).order_by(SiteVersion.version_number.desc())
    )
    versions = versions_result.scalars().all()

    return versions


@router.post("/{site_id}/versions/{version_id}/rollback", response_model=SitePublishResponse)
async def rollback_to_version(
    site_id: UUID,
    version_id: UUID,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Rollback site to a previous version.
    """
    # Verify site belongs to tenant
    site_result = await db.execute(
        select(Site).where(Site.id == site_id, Site.tenant_id == tenant.id)
    )
    site = site_result.scalar_one_or_none()

    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site not found"
        )

    # Verify version exists and belongs to this site
    version_result = await db.execute(
        select(SiteVersion).where(
            SiteVersion.id == version_id,
            SiteVersion.site_id == site_id
        )
    )
    version = version_result.scalar_one_or_none()

    if not version:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Version not found"
        )

    # Use publish service to rollback
    publish_service = PublishService(db)

    try:
        success = await publish_service.rollback_to_version(site_id, version_id)

        if success:
            await db.refresh(version)
            logger.info(f"Site rolled back: {site_id} to version {version.version_number} by user {user.id}")

            return SitePublishResponse(
                version_id=version.id,
                version_number=version.version_number,
                publish_url=site.publish_url or "",
                published_at=version.published_at
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to rollback version"
            )
    except Exception as e:
        logger.error(f"Failed to rollback site {site_id} to version {version_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to rollback: {str(e)}"
        )
