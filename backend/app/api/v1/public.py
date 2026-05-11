"""
Public API endpoints (no authentication required)

These endpoints are called from published websites.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID, uuid4
from datetime import datetime
import boto3
import logging
import os

from app.database import get_db
from app.models.site import Site
from app.models.form import FormDefinition, FormSubmission
from app.models.blog import BlogPost
from app.schemas.form import FormSubmissionCreate
from app.schemas.blog import BlogPostResponse
from app.schemas.analytics import AnalyticsTrackRequest

logger = logging.getLogger(__name__)
router = APIRouter()

# DynamoDB for analytics
dynamodb = boto3.resource('dynamodb', region_name=os.getenv("AWS_REGION", "us-east-1"))
pageviews_table = dynamodb.Table(os.getenv("DYNAMODB_PAGEVIEWS_TABLE", "ai-wb-page-views"))

# SES for form notifications
ses_client = boto3.client('ses', region_name=os.getenv("AWS_REGION", "us-east-1"))


@router.post("/forms/{site_id}/submit", status_code=status.HTTP_201_CREATED)
async def submit_form(
    site_id: UUID,
    submission: FormSubmissionCreate,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    Public form submission endpoint.

    This is called directly from published websites.
    """
    # Verify site exists
    site_result = await db.execute(
        select(Site).where(Site.id == site_id)
    )
    site = site_result.scalar_one_or_none()

    if not site or site.status != "published":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site not found or not published"
        )

    # Get form definition if provided
    form_def = None
    if submission.form_def_id:
        form_result = await db.execute(
            select(FormDefinition).where(
                FormDefinition.id == submission.form_def_id,
                FormDefinition.site_id == site_id,
                FormDefinition.is_enabled == True
            )
        )
        form_def = form_result.scalar_one_or_none()

        if not form_def:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Form not found or disabled"
            )

    # Create submission
    form_submission = FormSubmission(
        site_id=site_id,
        form_def_id=submission.form_def_id,
        page_id=submission.page_id,
        data=submission.data,
        status="new",
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get('user-agent')
    )

    db.add(form_submission)
    await db.commit()

    # Send notification emails if configured
    if form_def and form_def.notification_emails:
        try:
            email_body = "<h3>New Form Submission</h3><ul>"
            for key, value in submission.data.items():
                email_body += f"<li><strong>{key}:</strong> {value}</li>"
            email_body += "</ul>"

            ses_client.send_email(
                Source=os.getenv("SES_SENDER_EMAIL", "noreply@chinabjalex.com"),
                Destination={'ToAddresses': form_def.notification_emails},
                Message={
                    'Subject': {'Data': f"New form submission on {site.name}"},
                    'Body': {'Html': {'Data': email_body}}
                }
            )
        except Exception as e:
            logger.error(f"Failed to send form notification email: {str(e)}")

    logger.info(f"Form submission created: {form_submission.id} for site {site_id}")

    return {
        "success": True,
        "message": form_def.success_message if form_def and form_def.success_message else "Thank you for your submission!"
    }


@router.get("/blogs/{site_id}/posts", response_model=List[BlogPostResponse])
async def list_public_blog_posts(
    site_id: UUID,
    category_id: UUID | None = None,
    limit: int = 20,
    db: AsyncSession = Depends(get_db)
):
    """
    Get published blog posts for a site (public access).
    """
    # Verify site is published
    site_result = await db.execute(
        select(Site).where(Site.id == site_id, Site.status == "published")
    )
    site = site_result.scalar_one_or_none()

    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site not found or not published"
        )

    # Build query - only published posts
    query = select(BlogPost).where(
        BlogPost.site_id == site_id,
        BlogPost.status == "published"
    )

    if category_id:
        query = query.where(BlogPost.category_id == category_id)

    query = query.order_by(BlogPost.published_at.desc()).limit(limit)

    result = await db.execute(query)
    posts = result.scalars().all()
    return posts


@router.get("/blogs/{site_id}/posts/{slug}", response_model=BlogPostResponse)
async def get_public_blog_post(
    site_id: UUID,
    slug: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific published blog post by slug (public access).
    """
    # Verify site is published
    site_result = await db.execute(
        select(Site).where(Site.id == site_id, Site.status == "published")
    )
    site = site_result.scalar_one_or_none()

    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site not found or not published"
        )

    # Get post
    result = await db.execute(
        select(BlogPost).where(
            BlogPost.site_id == site_id,
            BlogPost.slug == slug,
            BlogPost.status == "published"
        )
    )
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog post not found"
        )

    return post


@router.post("/analytics/{site_id}/track", status_code=status.HTTP_202_ACCEPTED)
async def track_pageview(
    site_id: UUID,
    track_data: AnalyticsTrackRequest,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    Analytics tracking beacon (public).

    Lightweight endpoint to track page views from published sites.
    """
    # Verify site exists and is published
    site_result = await db.execute(
        select(Site).where(Site.id == site_id, Site.status == "published")
    )
    site = site_result.scalar_one_or_none()

    if not site:
        # Silently fail for invalid sites
        return {"success": True}

    try:
        # Generate or use visitor_id
        visitor_id = track_data.visitor_id or str(uuid4())

        # Determine device type from user agent
        user_agent = request.headers.get('user-agent', '').lower()
        if 'mobile' in user_agent or 'android' in user_agent or 'iphone' in user_agent:
            device_type = 'mobile'
        elif 'tablet' in user_agent or 'ipad' in user_agent:
            device_type = 'tablet'
        else:
            device_type = 'desktop'

        # Store in DynamoDB
        timestamp = datetime.utcnow().isoformat()
        pageviews_table.put_item(
            Item={
                'site_id': str(site_id),
                'timestamp_visitor': f"{timestamp}#{visitor_id}",
                'page_path': track_data.page_path,
                'referrer': track_data.referrer or '',
                'user_agent': request.headers.get('user-agent', ''),
                'device_type': device_type,
                'timestamp': timestamp,
                'ttl': int((datetime.utcnow().timestamp() + 90 * 24 * 3600))  # 90 days TTL
            }
        )

        logger.debug(f"Pageview tracked: {site_id} {track_data.page_path}")
    except Exception as e:
        logger.error(f"Failed to track pageview: {str(e)}")
        # Silently fail, don't block the visitor

    return {"success": True}
