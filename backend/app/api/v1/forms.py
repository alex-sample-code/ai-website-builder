"""
Form management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
from uuid import UUID
from datetime import datetime
import csv
import io
from app.database import get_db
from app.models.form import FormDefinition, FormSubmission
from app.models.site import Site
from app.models.tenant import Tenant
from app.models.user import User
from app.schemas.form import (
    FormDefinitionCreate, FormDefinitionUpdate, FormDefinitionResponse,
    FormSubmissionUpdate, FormSubmissionResponse
)
from app.auth.deps import get_current_user, get_current_tenant
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


# Form Definition endpoints
@router.get("", response_model=List[FormDefinitionResponse])
async def list_form_definitions(
    site_id: UUID,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all form definitions for a site.
    """
    # Verify site belongs to tenant
    site_result = await db.execute(
        select(Site).where(Site.id == site_id, Site.tenant_id == tenant.id)
    )
    site = site_result.scalar_one_or_none()
    if not site:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site not found")

    result = await db.execute(
        select(FormDefinition).where(FormDefinition.site_id == site_id).order_by(FormDefinition.created_at.desc())
    )
    forms = result.scalars().all()
    return forms


@router.post("", response_model=FormDefinitionResponse, status_code=status.HTTP_201_CREATED)
async def create_form_definition(
    site_id: UUID,
    form_data: FormDefinitionCreate,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new form definition.
    """
    # Verify site belongs to tenant
    site_result = await db.execute(
        select(Site).where(Site.id == site_id, Site.tenant_id == tenant.id)
    )
    site = site_result.scalar_one_or_none()
    if not site:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site not found")

    form = FormDefinition(
        site_id=site_id,
        name=form_data.name,
        fields=form_data.fields,
        notification_emails=form_data.notification_emails,
        webhook_url=form_data.webhook_url,
        success_message=form_data.success_message,
        is_enabled=form_data.is_enabled
    )

    db.add(form)
    await db.commit()
    await db.refresh(form)

    logger.info(f"Form definition created: {form.id} by user {user.id}")
    return form


@router.put("/{form_id}", response_model=FormDefinitionResponse)
async def update_form_definition(
    site_id: UUID,
    form_id: UUID,
    form_data: FormDefinitionUpdate,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Update a form definition.
    """
    result = await db.execute(
        select(FormDefinition).join(Site).where(
            FormDefinition.id == form_id,
            FormDefinition.site_id == site_id,
            Site.tenant_id == tenant.id
        )
    )
    form = result.scalar_one_or_none()

    if not form:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Form definition not found")

    # Update fields
    if form_data.name is not None:
        form.name = form_data.name
    if form_data.fields is not None:
        form.fields = form_data.fields
    if form_data.notification_emails is not None:
        form.notification_emails = form_data.notification_emails
    if form_data.webhook_url is not None:
        form.webhook_url = form_data.webhook_url
    if form_data.success_message is not None:
        form.success_message = form_data.success_message
    if form_data.is_enabled is not None:
        form.is_enabled = form_data.is_enabled

    await db.commit()
    await db.refresh(form)

    logger.info(f"Form definition updated: {form.id} by user {user.id}")
    return form


# Form Submission endpoints
@router.get("/{form_id}/submissions", response_model=List[FormSubmissionResponse])
async def list_form_submissions(
    site_id: UUID,
    form_id: UUID,
    status_filter: str | None = Query(None, pattern="^(new|read|replied|archived)$"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all submissions for a form with optional filtering and pagination.
    """
    # Verify form belongs to tenant's site
    form_result = await db.execute(
        select(FormDefinition).join(Site).where(
            FormDefinition.id == form_id,
            FormDefinition.site_id == site_id,
            Site.tenant_id == tenant.id
        )
    )
    form = form_result.scalar_one_or_none()
    if not form:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Form not found")

    # Build query
    query = select(FormSubmission).where(FormSubmission.form_def_id == form_id)

    if status_filter:
        query = query.where(FormSubmission.status == status_filter)

    query = query.order_by(FormSubmission.submitted_at.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)

    result = await db.execute(query)
    submissions = result.scalars().all()
    return submissions


@router.put("/submissions/{submission_id}/status", response_model=FormSubmissionResponse)
async def update_submission_status(
    site_id: UUID,
    submission_id: UUID,
    update_data: FormSubmissionUpdate,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Update a form submission status.
    """
    result = await db.execute(
        select(FormSubmission).join(Site).where(
            FormSubmission.id == submission_id,
            FormSubmission.site_id == site_id,
            Site.tenant_id == tenant.id
        )
    )
    submission = result.scalar_one_or_none()

    if not submission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Submission not found")

    # Update status
    submission.status = update_data.status
    if update_data.notes is not None:
        submission.notes = update_data.notes

    # Set replied_at if status is replied
    if update_data.status == "replied" and submission.replied_at is None:
        submission.replied_at = datetime.utcnow()

    await db.commit()
    await db.refresh(submission)

    logger.info(f"Form submission status updated: {submission_id} by user {user.id}")
    return submission


@router.get("/{form_id}/submissions/export")
async def export_form_submissions(
    site_id: UUID,
    form_id: UUID,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Export form submissions as CSV.
    """
    # Verify form belongs to tenant's site
    form_result = await db.execute(
        select(FormDefinition).join(Site).where(
            FormDefinition.id == form_id,
            FormDefinition.site_id == site_id,
            Site.tenant_id == tenant.id
        )
    )
    form = form_result.scalar_one_or_none()
    if not form:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Form not found")

    # Get all submissions
    result = await db.execute(
        select(FormSubmission).where(
            FormSubmission.form_def_id == form_id
        ).order_by(FormSubmission.submitted_at.desc())
    )
    submissions = result.scalars().all()

    # Generate CSV
    output = io.StringIO()

    if not submissions:
        # Empty CSV with headers
        writer = csv.writer(output)
        writer.writerow(['ID', 'Submitted At', 'Status', 'Notes'])
        output.seek(0)
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=form_{form_id}_submissions.csv"}
        )

    # Extract all unique field names from submissions
    field_names = set()
    for submission in submissions:
        if submission.data:
            field_names.update(submission.data.keys())

    field_names = sorted(field_names)

    # Write CSV
    writer = csv.writer(output)

    # Header row
    headers = ['ID', 'Submitted At', 'Status', 'IP Address', 'Notes'] + field_names
    writer.writerow(headers)

    # Data rows
    for submission in submissions:
        row = [
            str(submission.id),
            submission.submitted_at.isoformat() if submission.submitted_at else '',
            submission.status,
            submission.ip_address or '',
            submission.notes or ''
        ]
        # Add field values
        for field_name in field_names:
            value = submission.data.get(field_name, '') if submission.data else ''
            row.append(str(value))

        writer.writerow(row)

    output.seek(0)

    logger.info(f"Form submissions exported: {form_id} by user {user.id}")

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=form_{form_id}_submissions.csv"}
    )
