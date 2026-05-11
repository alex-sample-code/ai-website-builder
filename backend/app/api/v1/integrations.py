"""
Integration management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID
from app.database import get_db
from app.models.integration import Integration
from app.models.site import Site
from app.models.tenant import Tenant
from app.models.user import User
from app.schemas.integration import IntegrationUpsert, IntegrationResponse
from app.auth.deps import get_current_user, get_current_tenant
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/{site_id}/integrations", response_model=List[IntegrationResponse])
async def list_integrations(
    site_id: UUID,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all integrations for a site.
    """
    # Verify site belongs to tenant
    site_result = await db.execute(
        select(Site).where(Site.id == site_id, Site.tenant_id == tenant.id)
    )
    site = site_result.scalar_one_or_none()

    if not site:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site not found")

    result = await db.execute(
        select(Integration).where(Integration.site_id == site_id).order_by(Integration.created_at)
    )
    integrations = result.scalars().all()
    return integrations


@router.put("/{site_id}/integrations/{integration_type}", response_model=IntegrationResponse)
async def upsert_integration(
    site_id: UUID,
    integration_type: str,
    integration_data: IntegrationUpsert,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Create or update an integration.

    Common integration types:
    - google_analytics
    - baidu_tongji
    - crisp
    - tidio
    - wechat
    - custom_webhook
    """
    # Verify site belongs to tenant
    site_result = await db.execute(
        select(Site).where(Site.id == site_id, Site.tenant_id == tenant.id)
    )
    site = site_result.scalar_one_or_none()

    if not site:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site not found")

    # Check if integration already exists
    result = await db.execute(
        select(Integration).where(
            Integration.site_id == site_id,
            Integration.type == integration_type
        )
    )
    integration = result.scalar_one_or_none()

    if integration:
        # Update existing
        integration.config = integration_data.config
        integration.is_enabled = integration_data.is_enabled
        action = "updated"
    else:
        # Create new
        integration = Integration(
            site_id=site_id,
            type=integration_type,
            config=integration_data.config,
            is_enabled=integration_data.is_enabled
        )
        db.add(integration)
        action = "created"

    await db.commit()
    await db.refresh(integration)

    logger.info(f"Integration {action}: {integration.id} type={integration_type} by user {user.id}")
    return integration


@router.delete("/{site_id}/integrations/{integration_type}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_integration(
    site_id: UUID,
    integration_type: str,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete an integration.
    """
    # Verify integration belongs to tenant's site
    result = await db.execute(
        select(Integration).join(Site).where(
            Integration.site_id == site_id,
            Integration.type == integration_type,
            Site.tenant_id == tenant.id
        )
    )
    integration = result.scalar_one_or_none()

    if not integration:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Integration not found")

    await db.delete(integration)
    await db.commit()

    logger.info(f"Integration deleted: {integration.id} type={integration_type} by user {user.id}")
    return None
