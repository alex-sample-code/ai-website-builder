"""
Blog models
"""

from sqlalchemy import String, ForeignKey, Text, DateTime, Integer, Enum as SQLEnum, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base, UUIDMixin, TimestampMixin
from datetime import datetime
import enum
import uuid


class BlogPostStatus(str, enum.Enum):
    """Blog post status enum"""
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


# Many-to-many association table for blog posts and tags
blog_post_tags = Table(
    "blog_post_tags",
    Base.metadata,
    Column("post_id", UUID(as_uuid=True), ForeignKey("blog_posts.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", UUID(as_uuid=True), ForeignKey("blog_tags.id", ondelete="CASCADE"), primary_key=True),
)


class BlogPost(Base, UUIDMixin, TimestampMixin):
    """BlogPost model - represents a blog article"""

    __tablename__ = "blog_posts"

    site_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("sites.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    category_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("blog_categories.id", ondelete="SET NULL"),
        nullable=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    content_html: Mapped[str | None] = mapped_column(Text, nullable=True)
    excerpt: Mapped[str | None] = mapped_column(String(500), nullable=True)
    cover_image: Mapped[str | None] = mapped_column(String(500), nullable=True)
    seo_title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    seo_description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    author_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(
        SQLEnum(BlogPostStatus, values_callable=lambda x: [e.value for e in x]),
        default=BlogPostStatus.DRAFT.value,
        nullable=False,
        index=True
    )
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    scheduled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    site: Mapped["Site"] = relationship("Site", back_populates="blog_posts")
    category: Mapped["BlogCategory"] = relationship("BlogCategory", back_populates="posts")
    tags: Mapped[list["BlogTag"]] = relationship(
        "BlogTag",
        secondary=blog_post_tags,
        back_populates="posts"
    )

    def __repr__(self) -> str:
        return f"<BlogPost(id={self.id}, title={self.title}, status={self.status})>"


class BlogCategory(Base, UUIDMixin):
    """BlogCategory model - represents a blog category"""

    __tablename__ = "blog_categories"

    site_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("sites.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Relationships
    site: Mapped["Site"] = relationship("Site", back_populates="blog_categories")
    posts: Mapped[list["BlogPost"]] = relationship("BlogPost", back_populates="category", lazy="selectin")

    def __repr__(self) -> str:
        return f"<BlogCategory(id={self.id}, name={self.name})>"


class BlogTag(Base, UUIDMixin):
    """BlogTag model - represents a blog tag"""

    __tablename__ = "blog_tags"

    site_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("sites.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), nullable=False)

    # Relationships
    site: Mapped["Site"] = relationship("Site", back_populates="blog_tags")
    posts: Mapped[list["BlogPost"]] = relationship(
        "BlogPost",
        secondary=blog_post_tags,
        back_populates="tags"
    )

    def __repr__(self) -> str:
        return f"<BlogTag(id={self.id}, name={self.name})>"
