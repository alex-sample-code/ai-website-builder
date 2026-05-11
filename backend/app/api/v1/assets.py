"""
Asset management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID, uuid4
from datetime import datetime, timedelta
from app.database import get_db
from app.models.asset import Asset
from app.models.site import Site
from app.models.tenant import Tenant
from app.models.user import User
from app.schemas.asset import AssetUploadRequest, AssetUploadResponse, AssetResponse
from app.auth.deps import get_current_user, get_current_tenant
import boto3
from botocore.config import Config
import logging
import os

logger = logging.getLogger(__name__)
router = APIRouter()

# AWS S3 configuration
S3_BUCKET = os.getenv("AWS_ASSETS_BUCKET", "ai-wb-assets-959545103699")
S3_REGION = os.getenv("AWS_REGION", "us-east-1")
CLOUDFRONT_DOMAIN = os.getenv("CLOUDFRONT_DOMAIN", "d2raj73d783uqn.cloudfront.net")

s3_client = boto3.client('s3', region_name=S3_REGION, config=Config(signature_version='s3v4'))


@router.get("/{site_id}/assets", response_model=List[AssetResponse])
async def list_assets(
    site_id: UUID,
    folder: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all assets for a site.
    """
    # Verify site belongs to tenant
    site_result = await db.execute(
        select(Site).where(Site.id == site_id, Site.tenant_id == tenant.id)
    )
    site = site_result.scalar_one_or_none()

    if not site:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site not found")

    # Build query
    query = select(Asset).where(Asset.site_id == site_id)

    if folder:
        query = query.where(Asset.folder == folder)

    query = query.order_by(Asset.created_at.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)

    result = await db.execute(query)
    assets = result.scalars().all()
    return assets


@router.post("/{site_id}/assets/upload", response_model=AssetUploadResponse)
async def generate_upload_url(
    site_id: UUID,
    upload_request: AssetUploadRequest,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Generate a presigned S3 URL for direct upload.

    Returns the upload URL and the final CDN URL for the asset.
    """
    # Verify site belongs to tenant
    site_result = await db.execute(
        select(Site).where(Site.id == site_id, Site.tenant_id == tenant.id)
    )
    site = site_result.scalar_one_or_none()

    if not site:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site not found")

    # Generate unique asset ID
    asset_id = uuid4()

    # Build S3 key: tenant_id/site_id/folder/filename
    folder_prefix = f"{upload_request.folder}/" if upload_request.folder else ""
    s3_key = f"{tenant.id}/{site_id}/{folder_prefix}{asset_id}_{upload_request.filename}"

    # Generate presigned URL
    try:
        upload_url = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': S3_BUCKET,
                'Key': s3_key,
                'ContentType': upload_request.content_type
            },
            ExpiresIn=3600  # 1 hour
        )
    except Exception as e:
        logger.error(f"Failed to generate presigned URL: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate upload URL"
        )

    # CDN URL
    cdn_url = f"https://{CLOUDFRONT_DOMAIN}/{s3_key}"

    # Create asset record
    asset = Asset(
        id=asset_id,
        tenant_id=tenant.id,
        site_id=site_id,
        filename=upload_request.filename,
        s3_key=s3_key,
        cdn_url=cdn_url,
        content_type=upload_request.content_type,
        size_bytes=0,  # Will be updated after upload
        folder=upload_request.folder
    )

    db.add(asset)
    await db.commit()

    logger.info(f"Upload URL generated for asset: {asset_id} by user {user.id}")

    return AssetUploadResponse(
        asset_id=asset_id,
        upload_url=upload_url,
        cdn_url=cdn_url
    )


@router.delete("/{site_id}/assets/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_asset(
    site_id: UUID,
    asset_id: UUID,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete an asset from S3 and database.
    """
    # Verify asset belongs to tenant's site
    result = await db.execute(
        select(Asset).join(Site).where(
            Asset.id == asset_id,
            Asset.site_id == site_id,
            Site.tenant_id == tenant.id
        )
    )
    asset = result.scalar_one_or_none()

    if not asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")

    # Delete from S3
    try:
        s3_client.delete_object(Bucket=S3_BUCKET, Key=asset.s3_key)
    except Exception as e:
        logger.error(f"Failed to delete asset from S3: {str(e)}")
        # Continue with database deletion even if S3 deletion fails

    # Delete from database
    await db.delete(asset)
    await db.commit()

    logger.info(f"Asset deleted: {asset_id} by user {user.id}")
    return None
