"""
Integration model
"""

from sqlalchemy import String, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.models.base import Base, UUIDMixin, TimestampMixin
import uuid


class Integration(Base, UUIDMixin, TimestampMixin):
    """Integration model - represents third-party service integrations"""

    __tablename__ = "integrations"

    site_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("sites.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    config: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    site: Mapped["Site"] = relationship("Site", back_populates="integrations")

    def __repr__(self) -> str:
        return f"<Integration(id={self.id}, type={self.type}, enabled={self.is_enabled})>"
