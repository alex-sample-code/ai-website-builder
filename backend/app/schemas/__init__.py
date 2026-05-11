"""
Pydantic schemas for request/response validation
"""

from app.schemas.common import (
    BaseSchema,
    TimestampSchema,
    IDSchema,
    PaginationParams,
    PaginatedResponse,
)
from app.schemas.tenant import (
    TenantBase,
    TenantCreate,
    TenantUpdate,
    TenantResponse,
    TenantDetail,
)
from app.schemas.user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
    UserLogin,
    UserRegister,
    TokenResponse,
    CurrentUser,
)
from app.schemas.site import (
    SiteBase,
    SiteCreate,
    SiteUpdate,
    SiteResponse,
    SiteDetail,
    SitePublishRequest,
    SitePublishResponse,
)
from app.schemas.page import (
    PageBase,
    PageCreate,
    PageUpdate,
    PageContentUpdate,
    PageResponse,
    PageDetail,
    PageReorderRequest,
)
from app.schemas.blog import (
    BlogPostBase,
    BlogPostCreate,
    BlogPostUpdate,
    BlogPostResponse,
    BlogCategoryBase,
    BlogCategoryCreate,
    BlogCategoryUpdate,
    BlogCategoryResponse,
    BlogTagBase,
    BlogTagCreate,
    BlogTagResponse,
)
from app.schemas.form import (
    FormDefinitionBase,
    FormDefinitionCreate,
    FormDefinitionUpdate,
    FormDefinitionResponse,
    FormSubmissionCreate,
    FormSubmissionUpdate,
    FormSubmissionResponse,
)
from app.schemas.ai_session import (
    AISessionCreate,
    AISessionMessageRequest,
    AISessionGenerateRequest,
    AISessionResponse,
    AISessionStatusResponse,
)

__all__ = [
    # Common
    "BaseSchema",
    "TimestampSchema",
    "IDSchema",
    "PaginationParams",
    "PaginatedResponse",
    # Tenant
    "TenantBase",
    "TenantCreate",
    "TenantUpdate",
    "TenantResponse",
    "TenantDetail",
    # User
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserLogin",
    "UserRegister",
    "TokenResponse",
    "CurrentUser",
    # Site
    "SiteBase",
    "SiteCreate",
    "SiteUpdate",
    "SiteResponse",
    "SiteDetail",
    "SitePublishRequest",
    "SitePublishResponse",
    # Page
    "PageBase",
    "PageCreate",
    "PageUpdate",
    "PageContentUpdate",
    "PageResponse",
    "PageDetail",
    "PageReorderRequest",
    # Blog
    "BlogPostBase",
    "BlogPostCreate",
    "BlogPostUpdate",
    "BlogPostResponse",
    "BlogCategoryBase",
    "BlogCategoryCreate",
    "BlogCategoryUpdate",
    "BlogCategoryResponse",
    "BlogTagBase",
    "BlogTagCreate",
    "BlogTagResponse",
    # Form
    "FormDefinitionBase",
    "FormDefinitionCreate",
    "FormDefinitionUpdate",
    "FormDefinitionResponse",
    "FormSubmissionCreate",
    "FormSubmissionUpdate",
    "FormSubmissionResponse",
    # AI Session
    "AISessionCreate",
    "AISessionMessageRequest",
    "AISessionGenerateRequest",
    "AISessionResponse",
    "AISessionStatusResponse",
]
