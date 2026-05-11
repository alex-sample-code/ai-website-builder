"""
Template library endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
import boto3
import json
import logging
import os

from app.schemas.template import TemplateResponse, TemplatePreviewResponse
from app.models.user import User
from app.auth.deps import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter()

# S3 configuration for templates
S3_TEMPLATES_BUCKET = os.getenv("AWS_TEMPLATES_BUCKET", "ai-wb-templates-959545103699")
S3_REGION = os.getenv("AWS_REGION", "us-east-1")
s3_client = boto3.client('s3', region_name=S3_REGION)


@router.get("", response_model=List[TemplateResponse])
async def list_templates(
    category: str | None = None,
    tag: str | None = None,
    user: User = Depends(get_current_user)
):
    """
    Get all available templates.

    Templates are stored in S3 as: templates/{template_id}/metadata.json

    Optional filters:
    - category: Filter by industry/category
    - tag: Filter by tag
    """
    try:
        # List all templates from S3
        response = s3_client.list_objects_v2(
            Bucket=S3_TEMPLATES_BUCKET,
            Prefix="templates/",
            Delimiter="/"
        )

        templates = []

        # Get common prefixes (template directories)
        for prefix in response.get('CommonPrefixes', []):
            template_id = prefix['Prefix'].rstrip('/').split('/')[-1]

            # Try to fetch metadata
            try:
                metadata_obj = s3_client.get_object(
                    Bucket=S3_TEMPLATES_BUCKET,
                    Key=f"templates/{template_id}/metadata.json"
                )
                metadata = json.loads(metadata_obj['Body'].read())

                # Build template response
                template = TemplateResponse(
                    id=template_id,
                    name=metadata.get('name', template_id),
                    description=metadata.get('description'),
                    category=metadata.get('category'),
                    preview_url=metadata.get('preview_url'),
                    thumbnail_url=metadata.get('thumbnail_url'),
                    tags=metadata.get('tags', []),
                    metadata=metadata
                )

                # Apply filters
                if category and template.category != category:
                    continue
                if tag and tag not in template.tags:
                    continue

                templates.append(template)
            except s3_client.exceptions.NoSuchKey:
                # Skip templates without metadata
                logger.warning(f"Template {template_id} missing metadata.json")
                continue
            except Exception as e:
                logger.error(f"Error loading template {template_id}: {str(e)}")
                continue

        return templates

    except Exception as e:
        logger.error(f"Failed to list templates: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch templates"
        )


@router.get("/{template_id}/preview", response_model=TemplatePreviewResponse)
async def get_template_preview(
    template_id: str,
    user: User = Depends(get_current_user)
):
    """
    Get template preview data including page structure.
    """
    try:
        # Fetch template preview data
        preview_obj = s3_client.get_object(
            Bucket=S3_TEMPLATES_BUCKET,
            Key=f"templates/{template_id}/preview.json"
        )
        preview_data = json.loads(preview_obj['Body'].read())

        # Fetch metadata for preview_url
        metadata_obj = s3_client.get_object(
            Bucket=S3_TEMPLATES_BUCKET,
            Key=f"templates/{template_id}/metadata.json"
        )
        metadata = json.loads(metadata_obj['Body'].read())

        return TemplatePreviewResponse(
            template_id=template_id,
            preview_url=metadata.get('preview_url', ''),
            pages=preview_data.get('pages', [])
        )

    except s3_client.exceptions.NoSuchKey:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    except Exception as e:
        logger.error(f"Failed to get template preview: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch template preview"
        )
