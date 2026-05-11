"""
Site model
"""

from sqlalchemy import String, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.models.base import Base, UUIDMixin, TimestampMixin
from datetime import datetime
import enum
import uuid


class SiteStatus(str, enum.Enum):
    """Site status enum"""
    DRAFT = "draft"
    PUBLISHED = "published"
    OFFLINE = "offline"


class Site(Base, UUIDMixin, TimestampMixin):
    """Site model - represents a website"""

    __tablename__ = "sites"

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(
        SQLEnum(SiteStatus, values_callable=lambda x: [e.value for e in x]),
        default=SiteStatus.DRAFT.value,
        nullable=False,
        index=True
    )
    template_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    current_version_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("site_versions.id", ondelete="SET NULL"),
        nullable=True
    )
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    publish_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    settings_snapshot: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    # Relationships
    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="sites")
    pages: Mapped[list["Page"]] = relationship("Page", back_populates="site", cascade="all, delete-orphan", lazy="selectin")
    site_versions: Mapped[list["SiteVersion"]] = relationship(
        "SiteVersion",
        back_populates="site",
        foreign_keys="SiteVersion.site_id",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    site_settings: Mapped["SiteSettings"] = relationship(
        "SiteSettings",
        back_populates="site",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    nav_menus: Mapped[list["NavMenu"]] = relationship("NavMenu", back_populates="site", cascade="all, delete-orphan", lazy="selectin")
    assets: Mapped[list["Asset"]] = relationship("Asset", back_populates="site", lazy="selectin")
    ai_sessions: Mapped[list["AISession"]] = relationship("AISession", back_populates="site", lazy="selectin")
    blog_posts: Mapped[list["BlogPost"]] = relationship("BlogPost", back_populates="site", cascade="all, delete-orphan", lazy="selectin")
    blog_categories: Mapped[list["BlogCategory"]] = relationship("BlogCategory", back_populates="site", cascade="all, delete-orphan", lazy="selectin")
    blog_tags: Mapped[list["BlogTag"]] = relationship("BlogTag", back_populates="site", cascade="all, delete-orphan", lazy="selectin")
    form_definitions: Mapped[list["FormDefinition"]] = relationship("FormDefinition", back_populates="site", cascade="all, delete-orphan", lazy="selectin")
    form_submissions: Mapped[list["FormSubmission"]] = relationship("FormSubmission", back_populates="site", lazy="selectin")
    integrations: Mapped[list["Integration"]] = relationship("Integration", back_populates="site", cascade="all, delete-orphan", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Site(id={self.id}, name={self.name}, status={self.status})>"
