"""
Asset model
"""

from sqlalchemy import String, ForeignKey, BigInteger, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base, UUIDMixin, TimestampMixin
import uuid


class Asset(Base, UUIDMixin, TimestampMixin):
    """Asset model - represents uploaded files (images, videos, documents)"""

    __tablename__ = "assets"

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    site_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("sites.id", ondelete="CASCADE"),
        nullable=True,
        index=True
    )
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    s3_key: Mapped[str] = mapped_column(String(500), nullable=False)
    cdn_url: Mapped[str] = mapped_column(String(500), nullable=False)
    content_type: Mapped[str] = mapped_column(String(100), nullable=False)
    size_bytes: Mapped[int] = mapped_column(BigInteger, nullable=False)
    width: Mapped[int | None] = mapped_column(Integer, nullable=True)
    height: Mapped[int | None] = mapped_column(Integer, nullable=True)
    folder: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Relationships
    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="assets")
    site: Mapped["Site"] = relationship("Site", back_populates="assets")

    def __repr__(self) -> str:
        return f"<Asset(id={self.id}, filename={self.filename})>"
