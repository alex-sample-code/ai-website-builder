"""
AI Builder endpoints - Bedrock Claude integration
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from typing import AsyncGenerator
import json
import logging

from app.database import get_db
from app.models.ai_session import AISession
from app.models.site import Site
from app.models.tenant import Tenant
from app.models.user import User
from app.schemas.ai_session import (
    AISessionCreate, AISessionResponse, AISessionMessageRequest,
    AISessionGenerateRequest, AISessionStatusResponse
)
from app.services.ai_service import AIService
from app.auth.deps import get_current_user, get_current_tenant

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/sessions", response_model=AISessionResponse, status_code=status.HTTP_201_CREATED)
async def create_ai_session(
    session_data: AISessionCreate,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new AI website generation session.
    """
    # Verify site if provided
    if session_data.site_id:
        site_result = await db.execute(
            select(Site).where(
                Site.id == session_data.site_id,
                Site.tenant_id == tenant.id
            )
        )
        site = site_result.scalar_one_or_none()
        if not site:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Site not found"
            )

    ai_service = AIService(db)

    try:
        session = await ai_service.create_session(
            tenant_id=tenant.id,
            site_id=session_data.site_id,
            company_info=session_data.company_info
        )

        logger.info(f"AI session created: {session.id} by user {user.id}")
        return session

    except Exception as e:
        logger.error(f"Failed to create AI session: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create AI session: {str(e)}"
        )


@router.post("/sessions/{session_id}/message")
async def send_ai_message(
    session_id: UUID,
    message_request: AISessionMessageRequest,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Send a message to the AI and get streaming response.

    Returns Server-Sent Events (SSE) stream.
    """
    # Verify session belongs to tenant
    session_result = await db.execute(
        select(AISession).where(
            AISession.id == session_id,
            AISession.tenant_id == tenant.id
        )
    )
    session = session_result.scalar_one_or_none()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="AI session not found"
        )

    ai_service = AIService(db)

    async def generate_response() -> AsyncGenerator[str, None]:
        """Generate SSE stream"""
        try:
            async for chunk in ai_service.send_message_streaming(
                session_id=session_id,
                message=message_request.message
            ):
                yield f"data: {json.dumps(chunk)}\n\n"

            yield "data: [DONE]\n\n"

        except Exception as e:
            logger.error(f"Error in AI message stream: {str(e)}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(
        generate_response(),
        media_type="text/event-stream"
    )


@router.post("/sessions/{session_id}/upload")
async def upload_company_doc(
    session_id: UUID,
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload company document (PDF/DOCX/TXT) to AI session.

    The document content will be extracted and used as context.
    """
    # Verify session belongs to tenant
    session_result = await db.execute(
        select(AISession).where(
            AISession.id == session_id,
            AISession.tenant_id == tenant.id
        )
    )
    session = session_result.scalar_one_or_none()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="AI session not found"
        )

    # Validate file type
    allowed_types = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain']
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF, DOCX, and TXT files are supported"
        )

    ai_service = AIService(db)

    try:
        content = await file.read()
        extracted_text = await ai_service.upload_document(
            session_id=session_id,
            filename=file.filename,
            content=content,
            content_type=file.content_type
        )

        logger.info(f"Document uploaded to AI session: {session_id} by user {user.id}")

        return {
            "success": True,
            "filename": file.filename,
            "extracted_text_length": len(extracted_text)
        }

    except Exception as e:
        logger.error(f"Failed to upload document: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process document: {str(e)}"
        )


@router.post("/sessions/{session_id}/generate")
async def generate_site(
    session_id: UUID,
    generate_request: AISessionGenerateRequest,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Trigger full site generation from AI session.

    This generates complete HTML/CSS for all pages based on the conversation.
    """
    # Verify session belongs to tenant
    session_result = await db.execute(
        select(AISession).where(
            AISession.id == session_id,
            AISession.tenant_id == tenant.id
        )
    )
    session = session_result.scalar_one_or_none()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="AI session not found"
        )

    ai_service = AIService(db)

    try:
        site = await ai_service.generate_site(
            session_id=session_id,
            regenerate=generate_request.regenerate
        )

        logger.info(f"Site generated from AI session: {session_id} -> site {site.id} by user {user.id}")

        return {
            "success": True,
            "site_id": site.id,
            "session_id": session_id
        }

    except Exception as e:
        logger.error(f"Failed to generate site: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate site: {str(e)}"
        )


@router.get("/sessions/{session_id}/status", response_model=AISessionStatusResponse)
async def get_session_status(
    session_id: UUID,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Check the status of an AI generation session.
    """
    # Verify session belongs to tenant
    session_result = await db.execute(
        select(AISession).where(
            AISession.id == session_id,
            AISession.tenant_id == tenant.id
        )
    )
    session = session_result.scalar_one_or_none()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="AI session not found"
        )

    # Calculate progress based on status
    progress = 0
    message = ""

    if session.status == "in_progress":
        progress = 50
        message = "Generating website..."
    elif session.status == "completed":
        progress = 100
        message = "Website generated successfully"
    elif session.status == "failed":
        progress = 0
        message = "Generation failed"

    return AISessionStatusResponse(
        session_id=session.id,
        status=session.status,
        progress=progress,
        message=message
    )


@router.post("/sessions/{session_id}/regenerate")
async def regenerate_page(
    session_id: UUID,
    page_slug: str,
    feedback: str,
    user: User = Depends(get_current_user),
    tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Regenerate a specific page based on feedback.
    """
    # Verify session belongs to tenant
    session_result = await db.execute(
        select(AISession).where(
            AISession.id == session_id,
            AISession.tenant_id == tenant.id
        )
    )
    session = session_result.scalar_one_or_none()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="AI session not found"
        )

    ai_service = AIService(db)

    try:
        result = await ai_service.regenerate_page(
            session_id=session_id,
            page_slug=page_slug,
            feedback=feedback
        )

        logger.info(f"Page regenerated: {page_slug} in session {session_id} by user {user.id}")

        return result

    except Exception as e:
        logger.error(f"Failed to regenerate page: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to regenerate page: {str(e)}"
        )
