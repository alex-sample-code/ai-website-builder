"""
Site Version model
"""

from sqlalchemy import String, ForeignKey, Boolean, Integer, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.models.base import Base, UUIDMixin
from datetime import datetime
import uuid


class SiteVersion(Base, UUIDMixin):
    """SiteVersion model - represents a published version of a site"""

    __tablename__ = "site_versions"

    site_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("sites.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    snapshot: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    s3_prefix: Mapped[str | None] = mapped_column(String(500), nullable=True)
    published_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default="now()")
    is_current: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    site: Mapped["Site"] = relationship("Site", back_populates="site_versions", foreign_keys=[site_id])
    published_by_user: Mapped["User"] = relationship("User", back_populates="site_versions")

    def __repr__(self) -> str:
        return f"<SiteVersion(id={self.id}, site_id={self.site_id}, version={self.version_number})>"
