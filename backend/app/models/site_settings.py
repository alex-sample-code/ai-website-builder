"""
Site Settings model
"""

from sqlalchemy import String, ForeignKey, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.models.base import Base, UUIDMixin
from datetime import datetime
import uuid


class SiteSettings(Base, UUIDMixin):
    """SiteSettings model - represents site-wide settings"""

    __tablename__ = "site_settings"

    site_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("sites.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )
    logo_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    favicon_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    company_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    company_address: Mapped[str | None] = mapped_column(Text, nullable=True)
    company_phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    company_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    social_links: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    analytics_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    custom_head_code: Mapped[str | None] = mapped_column(Text, nullable=True)
    custom_body_code: Mapped[str | None] = mapped_column(Text, nullable=True)
    color_scheme: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    font_family: Mapped[str | None] = mapped_column(String(255), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default="now()", onupdate=datetime.utcnow)

    # Relationships
    site: Mapped["Site"] = relationship("Site", back_populates="site_settings")

    def __repr__(self) -> str:
        return f"<SiteSettings(id={self.id}, site_id={self.site_id})>"
