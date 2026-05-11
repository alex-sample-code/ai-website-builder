"""
Page model
"""

from sqlalchemy import String, ForeignKey, Boolean, Integer, Text, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.models.base import Base, UUIDMixin, TimestampMixin
import enum
import uuid


class PageStatus(str, enum.Enum):
    """Page status enum"""
    ACTIVE = "active"
    HIDDEN = "hidden"
    DELETED = "deleted"


class Page(Base, UUIDMixin, TimestampMixin):
    """Page model - represents a website page"""

    __tablename__ = "pages"

    site_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("sites.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    slug: Mapped[str] = mapped_column(String(255), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    seo_meta: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    grapesjs_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    html: Mapped[str | None] = mapped_column(Text, nullable=True)
    css: Mapped[str | None] = mapped_column(Text, nullable=True)
    js: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_homepage: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    status: Mapped[str] = mapped_column(
        SQLEnum(PageStatus, values_callable=lambda x: [e.value for e in x]),
        default=PageStatus.ACTIVE.value,
        nullable=False
    )

    # Relationships
    site: Mapped["Site"] = relationship("Site", back_populates="pages")
    form_submissions: Mapped[list["FormSubmission"]] = relationship("FormSubmission", back_populates="page", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Page(id={self.id}, slug={self.slug}, title={self.title})>"
