"""
Team Invitation model
"""

from sqlalchemy import String, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base, UUIDMixin, TimestampMixin
from datetime import datetime
import enum
import uuid


class InvitationStatus(str, enum.Enum):
    """Invitation status enum"""
    PENDING = "pending"
    ACCEPTED = "accepted"
    EXPIRED = "expired"


class TeamInvitation(Base, UUIDMixin, TimestampMixin):
    """TeamInvitation model - represents a team member invitation"""

    __tablename__ = "team_invitations"

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    token: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    status: Mapped[str] = mapped_column(
        SQLEnum(InvitationStatus, values_callable=lambda x: [e.value for e in x]),
        default=InvitationStatus.PENDING.value,
        nullable=False
    )
    invited_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    # Relationships
    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="team_invitations")
    invited_by_user: Mapped["User"] = relationship("User", back_populates="invitations_sent", foreign_keys=[invited_by])

    def __repr__(self) -> str:
        return f"<TeamInvitation(id={self.id}, email={self.email}, status={self.status})>"
