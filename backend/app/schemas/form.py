"""
Form schemas
"""

from pydantic import Field
from datetime import datetime
from uuid import UUID
from typing import Dict, Any
from app.schemas.common import BaseSchema, TimestampSchema, IDSchema


# Form Definition schemas
class FormDefinitionBase(BaseSchema):
    """Base form definition schema"""

    name: str = Field(..., min_length=1, max_length=255)


class FormDefinitionCreate(FormDefinitionBase):
    """Schema for creating a form definition"""

    fields: Dict[str, Any] | None = None
    notification_emails: list[str] = []
    webhook_url: str | None = None
    success_message: str | None = None
    is_enabled: bool = True


class FormDefinitionUpdate(BaseSchema):
    """Schema for updating a form definition"""

    name: str | None = Field(None, min_length=1, max_length=255)
    fields: Dict[str, Any] | None = None
    notification_emails: list[str] | None = None
    webhook_url: str | None = None
    success_message: str | None = None
    is_enabled: bool | None = None


class FormDefinitionResponse(FormDefinitionBase, IDSchema, TimestampSchema):
    """Schema for form definition response"""

    site_id: UUID
    fields: Dict[str, Any] | None = None
    notification_emails: list[str] | None = None
    webhook_url: str | None = None
    success_message: str | None = None
    is_enabled: bool


# Form Submission schemas
class FormSubmissionCreate(BaseSchema):
    """Schema for creating a form submission (public)"""

    form_def_id: UUID | None = None
    page_id: UUID | None = None
    data: Dict[str, Any]


class FormSubmissionUpdate(BaseSchema):
    """Schema for updating a form submission"""

    status: str = Field(..., pattern="^(new|read|replied|archived)$")
    notes: str | None = None


class FormSubmissionResponse(IDSchema):
    """Schema for form submission response"""

    site_id: UUID
    form_def_id: UUID | None = None
    page_id: UUID | None = None
    data: Dict[str, Any] | None = None
    status: str
    replied_at: datetime | None = None
    notes: str | None = None
    ip_address: str | None = None
    user_agent: str | None = None
    submitted_at: datetime
