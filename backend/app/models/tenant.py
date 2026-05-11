"""
Tenant model
"""

from sqlalchemy import String, Integer, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, UUIDMixin, TimestampMixin
import enum


class TenantStatus(str, enum.Enum):
    """Tenant status enum"""
    ACTIVE = "active"
    SUSPENDED = "suspended"
    DELETED = "deleted"


class TenantPlan(str, enum.Enum):
    """Tenant plan enum"""
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class DomainStatus(str, enum.Enum):
    """Domain status enum"""
    PENDING = "pending"
    DNS_CONFIGURED = "dns_configured"
    SSL_PROVISIONING = "ssl_provisioning"
    ACTIVE = "active"
    ERROR = "error"


class Tenant(Base, UUIDMixin, TimestampMixin):
    """Tenant model - represents a company/organization"""

    __tablename__ = "tenants"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    plan: Mapped[str] = mapped_column(
        SQLEnum(TenantPlan, values_callable=lambda x: [e.value for e in x]),
        default=TenantPlan.FREE.value,
        nullable=False
    )
    custom_domain: Mapped[str | None] = mapped_column(String(255), nullable=True)
    cf_tenant_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    cf_connection_group_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    domain_status: Mapped[str] = mapped_column(
        SQLEnum(DomainStatus, values_callable=lambda x: [e.value for e in x]),
        default=DomainStatus.PENDING.value,
        nullable=False
    )
    status: Mapped[str] = mapped_column(
        SQLEnum(TenantStatus, values_callable=lambda x: [e.value for e in x]),
        default=TenantStatus.ACTIVE.value,
        nullable=False
    )
    ai_quota_used: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    ai_quota_limit: Mapped[int] = mapped_column(Integer, default=3, nullable=False)

    # Relationships
    users: Mapped[list["User"]] = relationship("User", back_populates="tenant", lazy="selectin")
    sites: Mapped[list["Site"]] = relationship("Site", back_populates="tenant", lazy="selectin")
    assets: Mapped[list["Asset"]] = relationship("Asset", back_populates="tenant", lazy="selectin")
    ai_sessions: Mapped[list["AISession"]] = relationship("AISession", back_populates="tenant", lazy="selectin")
    audit_logs: Mapped[list["AuditLog"]] = relationship("AuditLog", back_populates="tenant", lazy="selectin")
    team_invitations: Mapped[list["TeamInvitation"]] = relationship("TeamInvitation", back_populates="tenant", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Tenant(id={self.id}, name={self.name}, plan={self.plan})>"
