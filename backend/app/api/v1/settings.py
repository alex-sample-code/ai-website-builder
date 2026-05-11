"""
Site settings endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID
from app.database import get_db
from app.models.site import Site
from app.models.site_settings import SiteSettings
from app.models.nav_menu import NavMenu
from app.models.tenant import Tenant
from app.models.user import User
from app.schemas.settings import (
    SiteSettingsUpdate, SiteSettingsResponse,
    NavMenuUpdate, NavMenuResponse
)
from app.auth.deps import get_current_user, get_current_tenant
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/{site_id}/settings", response_model=SiteSettingsResponse)
async def get_site_settings(
    site_id: UUID,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Get site settings.
    """
    # Verify site belongs to tenant
    site_result = await db.execute(
        select(Site).where(Site.id == site_id, Site.tenant_id == tenant.id)
    )
    site = site_result.scalar_one_or_none()

    if not site:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site not found")

    # Get or create settings
    settings_result = await db.execute(
        select(SiteSettings).where(SiteSettings.site_id == site_id)
    )
    settings = settings_result.scalar_one_or_none()

    if not settings:
        # Create default settings
        settings = SiteSettings(site_id=site_id)
        db.add(settings)
        await db.commit()
        await db.refresh(settings)

    return settings


@router.put("/{site_id}/settings", response_model=SiteSettingsResponse)
async def update_site_settings(
    site_id: UUID,
    settings_data: SiteSettingsUpdate,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Update site settings.
    """
    # Verify site belongs to tenant
    site_result = await db.execute(
        select(Site).where(Site.id == site_id, Site.tenant_id == tenant.id)
    )
    site = site_result.scalar_one_or_none()

    if not site:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site not found")

    # Get or create settings
    settings_result = await db.execute(
        select(SiteSettings).where(SiteSettings.site_id == site_id)
    )
    settings = settings_result.scalar_one_or_none()

    if not settings:
        settings = SiteSettings(site_id=site_id)
        db.add(settings)

    # Update fields
    if settings_data.logo_url is not None:
        settings.logo_url = settings_data.logo_url
    if settings_data.favicon_url is not None:
        settings.favicon_url = settings_data.favicon_url
    if settings_data.company_name is not None:
        settings.company_name = settings_data.company_name
    if settings_data.company_address is not None:
        settings.company_address = settings_data.company_address
    if settings_data.company_phone is not None:
        settings.company_phone = settings_data.company_phone
    if settings_data.company_email is not None:
        settings.company_email = settings_data.company_email
    if settings_data.social_links is not None:
        settings.social_links = settings_data.social_links
    if settings_data.analytics_id is not None:
        settings.analytics_id = settings_data.analytics_id
    if settings_data.custom_head_code is not None:
        settings.custom_head_code = settings_data.custom_head_code
    if settings_data.custom_body_code is not None:
        settings.custom_body_code = settings_data.custom_body_code
    if settings_data.color_scheme is not None:
        settings.color_scheme = settings_data.color_scheme
    if settings_data.font_family is not None:
        settings.font_family = settings_data.font_family

    await db.commit()
    await db.refresh(settings)

    logger.info(f"Site settings updated: {site_id} by user {user.id}")
    return settings


@router.get("/{site_id}/nav-menus", response_model=List[NavMenuResponse])
async def get_nav_menus(
    site_id: UUID,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all navigation menus for a site.
    """
    # Verify site belongs to tenant
    site_result = await db.execute(
        select(Site).where(Site.id == site_id, Site.tenant_id == tenant.id)
    )
    site = site_result.scalar_one_or_none()

    if not site:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site not found")

    # Get menus
    menus_result = await db.execute(
        select(NavMenu).where(NavMenu.site_id == site_id)
    )
    menus = menus_result.scalars().all()

    return menus


@router.put("/{site_id}/nav-menus", response_model=List[NavMenuResponse])
async def update_nav_menus(
    site_id: UUID,
    menus_data: List[NavMenuUpdate],
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Update navigation menus for a site.

    This replaces all existing menus with the provided data.
    """
    # Verify site belongs to tenant
    site_result = await db.execute(
        select(Site).where(Site.id == site_id, Site.tenant_id == tenant.id)
    )
    site = site_result.scalar_one_or_none()

    if not site:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site not found")

    # Delete existing menus
    existing_menus_result = await db.execute(
        select(NavMenu).where(NavMenu.site_id == site_id)
    )
    existing_menus = existing_menus_result.scalars().all()
    for menu in existing_menus:
        await db.delete(menu)

    # Create new menus
    new_menus = []
    for menu_data in menus_data:
        menu = NavMenu(
            site_id=site_id,
            position=menu_data.items[0].get("position", "header") if menu_data.items else "header",
            items=menu_data.items
        )
        db.add(menu)
        new_menus.append(menu)

    await db.commit()

    # Refresh all
    for menu in new_menus:
        await db.refresh(menu)

    logger.info(f"Navigation menus updated: {site_id} by user {user.id}")
    return new_menus
