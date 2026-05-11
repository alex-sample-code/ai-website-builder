"""
User model
"""

from sqlalchemy import String, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base, UUIDMixin, TimestampMixin
from datetime import datetime
import enum
import uuid


class UserRole(str, enum.Enum):
    """User role enum"""
    OWNER = "owner"
    EDITOR = "editor"
    VIEWER = "viewer"


class User(Base, UUIDMixin, TimestampMixin):
    """User model - represents a platform user"""

    __tablename__ = "users"

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    cognito_sub: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(
        SQLEnum(UserRole, values_callable=lambda x: [e.value for e in x]),
        default=UserRole.OWNER.value,
        nullable=False
    )
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="users")
    site_versions: Mapped[list["SiteVersion"]] = relationship("SiteVersion", back_populates="published_by_user", lazy="selectin")
    audit_logs: Mapped[list["AuditLog"]] = relationship("AuditLog", back_populates="user", lazy="selectin")
    invitations_sent: Mapped[list["TeamInvitation"]] = relationship(
        "TeamInvitation",
        back_populates="invited_by_user",
        foreign_keys="TeamInvitation.invited_by",
        lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
