"""
Navigation Menu model
"""

from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.models.base import Base, UUIDMixin
from datetime import datetime
import uuid


class NavMenu(Base, UUIDMixin):
    """NavMenu model - represents navigation menu configuration"""

    __tablename__ = "nav_menus"

    site_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("sites.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    position: Mapped[str] = mapped_column(String(50), nullable=False)  # header/footer/sidebar
    items: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default="now()", onupdate=datetime.utcnow)

    # Relationships
    site: Mapped["Site"] = relationship("Site", back_populates="nav_menus")

    def __repr__(self) -> str:
        return f"<NavMenu(id={self.id}, site_id={self.site_id}, position={self.position})>"
