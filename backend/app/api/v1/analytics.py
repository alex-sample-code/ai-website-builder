"""
Analytics endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from datetime import datetime, timedelta
from typing import List
from app.database import get_db
from app.models.site import Site
from app.models.tenant import Tenant
from app.models.user import User
from app.schemas.analytics import (
    AnalyticsOverviewRequest, AnalyticsOverviewResponse,
    PageRankingResponse, SourceAnalysisResponse, DeviceBreakdownResponse
)
from app.auth.deps import get_current_user, get_current_tenant
import boto3
from boto3.dynamodb.conditions import Key
import logging
import os

logger = logging.getLogger(__name__)
router = APIRouter()

# DynamoDB configuration
dynamodb = boto3.resource('dynamodb', region_name=os.getenv("AWS_REGION", "us-east-1"))
pageviews_table = dynamodb.Table(os.getenv("DYNAMODB_PAGEVIEWS_TABLE", "ai-wb-page-views"))
daily_table = dynamodb.Table(os.getenv("DYNAMODB_DAILY_TABLE", "ai-wb-page-view-daily"))


@router.get("/{site_id}/analytics/overview", response_model=AnalyticsOverviewResponse)
async def get_analytics_overview(
    site_id: UUID,
    start_date: str,
    end_date: str,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Get analytics overview with date range.

    Returns total PV/UV and trend data.
    """
    # Verify site belongs to tenant
    site_result = await db.execute(
        select(Site).where(Site.id == site_id, Site.tenant_id == tenant.id)
    )
    site = site_result.scalar_one_or_none()

    if not site:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site not found")

    try:
        # Query DynamoDB daily aggregates
        response = daily_table.query(
            KeyConditionExpression=Key('site_id').eq(str(site_id)) &
                                 Key('date_page').between(f"{start_date}#", f"{end_date}#~")
        )

        items = response.get('Items', [])

        # Aggregate totals
        total_pv = sum(item.get('pv_count', 0) for item in items)
        total_uv = sum(item.get('uv_count', 0) for item in items)

        # Build trend data (group by date)
        trend_dict = {}
        for item in items:
            date_page = item.get('date_page', '')
            date = date_page.split('#')[0]
            if date:
                if date not in trend_dict:
                    trend_dict[date] = {'date': date, 'pageviews': 0, 'visitors': 0}
                trend_dict[date]['pageviews'] += item.get('pv_count', 0)
                trend_dict[date]['visitors'] += item.get('uv_count', 0)

        trend_data = sorted(trend_dict.values(), key=lambda x: x['date'])

        return AnalyticsOverviewResponse(
            total_pageviews=total_pv,
            total_unique_visitors=total_uv,
            trend_data=trend_data,
            change_percentage=None  # TODO: Calculate from previous period
        )
    except Exception as e:
        logger.error(f"Failed to fetch analytics overview: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch analytics data"
        )


@router.get("/{site_id}/analytics/pages", response_model=List[PageRankingResponse])
async def get_page_ranking(
    site_id: UUID,
    start_date: str,
    end_date: str,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Get page ranking by pageviews.
    """
    # Verify site belongs to tenant
    site_result = await db.execute(
        select(Site).where(Site.id == site_id, Site.tenant_id == tenant.id)
    )
    site = site_result.scalar_one_or_none()

    if not site:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site not found")

    try:
        # Query DynamoDB daily aggregates
        response = daily_table.query(
            KeyConditionExpression=Key('site_id').eq(str(site_id)) &
                                 Key('date_page').between(f"{start_date}#", f"{end_date}#~")
        )

        items = response.get('Items', [])

        # Aggregate by page
        page_stats = {}
        for item in items:
            date_page = item.get('date_page', '')
            parts = date_page.split('#')
            if len(parts) >= 2:
                page_path = parts[1]
                if page_path not in page_stats:
                    page_stats[page_path] = {'page_path': page_path, 'pageviews': 0, 'unique_visitors': 0}
                page_stats[page_path]['pageviews'] += item.get('pv_count', 0)
                page_stats[page_path]['unique_visitors'] += item.get('uv_count', 0)

        # Sort by pageviews and return top pages
        ranking = sorted(page_stats.values(), key=lambda x: x['pageviews'], reverse=True)[:20]

        return [PageRankingResponse(**item) for item in ranking]
    except Exception as e:
        logger.error(f"Failed to fetch page ranking: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch page ranking"
        )


@router.get("/{site_id}/analytics/sources", response_model=List[SourceAnalysisResponse])
async def get_source_analysis(
    site_id: UUID,
    start_date: str,
    end_date: str,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Get referrer analysis.
    """
    # Verify site belongs to tenant
    site_result = await db.execute(
        select(Site).where(Site.id == site_id, Site.tenant_id == tenant.id)
    )
    site = site_result.scalar_one_or_none()

    if not site:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site not found")

    try:
        # Query raw pageviews (for referrer data)
        response = pageviews_table.query(
            KeyConditionExpression=Key('site_id').eq(str(site_id)),
            FilterExpression='#ts BETWEEN :start AND :end',
            ExpressionAttributeNames={'#ts': 'timestamp'},
            ExpressionAttributeValues={
                ':start': start_date,
                ':end': end_date
            },
            Limit=10000  # Sample recent data
        )

        items = response.get('Items', [])

        # Aggregate by referrer
        referrer_counts = {}
        for item in items:
            referrer = item.get('referrer', 'Direct')
            if not referrer or referrer == '':
                referrer = 'Direct'
            referrer_counts[referrer] = referrer_counts.get(referrer, 0) + 1

        total = sum(referrer_counts.values())

        # Build response
        sources = [
            SourceAnalysisResponse(
                referrer=ref,
                visits=count,
                percentage=round((count / total * 100), 2) if total > 0 else 0
            )
            for ref, count in sorted(referrer_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        ]

        return sources
    except Exception as e:
        logger.error(f"Failed to fetch source analysis: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch source analysis"
        )


@router.get("/{site_id}/analytics/devices", response_model=List[DeviceBreakdownResponse])
async def get_device_breakdown(
    site_id: UUID,
    start_date: str,
    end_date: str,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Get device breakdown.
    """
    # Verify site belongs to tenant
    site_result = await db.execute(
        select(Site).where(Site.id == site_id, Site.tenant_id == tenant.id)
    )
    site = site_result.scalar_one_or_none()

    if not site:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site not found")

    try:
        # Query raw pageviews (for device_type data)
        response = pageviews_table.query(
            KeyConditionExpression=Key('site_id').eq(str(site_id)),
            FilterExpression='#ts BETWEEN :start AND :end',
            ExpressionAttributeNames={'#ts': 'timestamp'},
            ExpressionAttributeValues={
                ':start': start_date,
                ':end': end_date
            },
            Limit=10000  # Sample recent data
        )

        items = response.get('Items', [])

        # Aggregate by device type
        device_counts = {}
        for item in items:
            device_type = item.get('device_type', 'Unknown')
            device_counts[device_type] = device_counts.get(device_type, 0) + 1

        total = sum(device_counts.values())

        # Build response
        devices = [
            DeviceBreakdownResponse(
                device_type=device,
                count=count,
                percentage=round((count / total * 100), 2) if total > 0 else 0
            )
            for device, count in sorted(device_counts.items(), key=lambda x: x[1], reverse=True)
        ]

        return devices
    except Exception as e:
        logger.error(f"Failed to fetch device breakdown: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch device breakdown"
        )
