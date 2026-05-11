"""
AI Session model
"""

from sqlalchemy import String, ForeignKey, Text, Integer, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.models.base import Base, UUIDMixin, TimestampMixin
import enum
import uuid


class AISessionStatus(str, enum.Enum):
    """AI Session status enum"""
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class AISession(Base, UUIDMixin, TimestampMixin):
    """AISession model - represents an AI website generation session"""

    __tablename__ = "ai_sessions"

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    site_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("sites.id", ondelete="CASCADE"),
        nullable=True
    )
    conversation: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    company_info: Mapped[str | None] = mapped_column(Text, nullable=True)
    company_info_s3_key: Mapped[str | None] = mapped_column(String(500), nullable=True)
    generated_config: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    generated_pages: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    model_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    input_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    output_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    generation_time_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(
        SQLEnum(AISessionStatus, values_callable=lambda x: [e.value for e in x]),
        default=AISessionStatus.IN_PROGRESS.value,
        nullable=False
    )

    # Relationships
    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="ai_sessions")
    site: Mapped["Site"] = relationship("Site", back_populates="ai_sessions")

    def __repr__(self) -> str:
        return f"<AISession(id={self.id}, status={self.status})>"
