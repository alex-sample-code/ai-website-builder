"""
AI Session schemas
"""

from pydantic import Field
from uuid import UUID
from typing import Dict, Any
from app.schemas.common import BaseSchema, TimestampSchema, IDSchema


class AISessionCreate(BaseSchema):
    """Schema for creating an AI session"""

    company_info: str | None = None
    site_id: UUID | None = None


class AISessionMessageRequest(BaseSchema):
    """Schema for sending a message to AI"""

    message: str = Field(..., min_length=1)


class AISessionGenerateRequest(BaseSchema):
    """Schema for triggering site generation"""

    regenerate: bool = False


class AISessionResponse(IDSchema, TimestampSchema):
    """Schema for AI session response"""

    tenant_id: UUID
    site_id: UUID | None = None
    conversation: Dict[str, Any] | None = None
    company_info: str | None = None
    company_info_s3_key: str | None = None
    generated_config: Dict[str, Any] | None = None
    generated_pages: Dict[str, Any] | None = None
    model_id: str | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    generation_time_ms: int | None = None
    status: str


class AISessionStatusResponse(BaseSchema):
    """Schema for AI session status check"""

    session_id: UUID
    status: str
    progress: int | None = None
    message: str | None = None
