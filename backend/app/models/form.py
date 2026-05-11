"""
Form models
"""

from sqlalchemy import String, ForeignKey, Boolean, Text, DateTime, Enum as SQLEnum, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.models.base import Base, UUIDMixin, TimestampMixin
from datetime import datetime
import enum
import uuid


class FormSubmissionStatus(str, enum.Enum):
    """Form submission status enum"""
    NEW = "new"
    READ = "read"
    REPLIED = "replied"
    ARCHIVED = "archived"


class FormDefinition(Base, UUIDMixin, TimestampMixin):
    """FormDefinition model - represents a form configuration"""

    __tablename__ = "form_definitions"

    site_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("sites.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    fields: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    notification_emails: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    webhook_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    success_message: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    site: Mapped["Site"] = relationship("Site", back_populates="form_definitions")
    submissions: Mapped[list["FormSubmission"]] = relationship("FormSubmission", back_populates="form_definition", lazy="selectin")

    def __repr__(self) -> str:
        return f"<FormDefinition(id={self.id}, name={self.name})>"


class FormSubmission(Base, UUIDMixin):
    """FormSubmission model - represents a form submission"""

    __tablename__ = "form_submissions"

    site_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("sites.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    form_def_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("form_definitions.id", ondelete="SET NULL"),
        nullable=True
    )
    page_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("pages.id", ondelete="SET NULL"),
        nullable=True
    )
    data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    status: Mapped[str] = mapped_column(
        SQLEnum(FormSubmissionStatus, values_callable=lambda x: [e.value for e in x]),
        default=FormSubmissionStatus.NEW.value,
        nullable=False,
        index=True
    )
    replied_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(50), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(500), nullable=True)
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default="now()")

    # Relationships
    site: Mapped["Site"] = relationship("Site", back_populates="form_submissions")
    form_definition: Mapped["FormDefinition"] = relationship("FormDefinition", back_populates="submissions")
    page: Mapped["Page"] = relationship("Page", back_populates="form_submissions")

    def __repr__(self) -> str:
        return f"<FormSubmission(id={self.id}, status={self.status})>"
