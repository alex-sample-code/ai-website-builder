"""
API v1 routes
"""

from fastapi import APIRouter
from app.api.v1 import auth, sites, pages, health

api_router = APIRouter()

# Include all route modules
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(sites.router, prefix="/sites", tags=["sites"])
api_router.include_router(pages.router, prefix="/sites/{site_id}/pages", tags=["pages"])

# Additional routers will be included as they're implemented
# api_router.include_router(publish.router, prefix="/sites/{site_id}", tags=["publish"])
# api_router.include_router(blog.router, prefix="/sites/{site_id}/blog", tags=["blog"])
# api_router.include_router(forms.router, prefix="/sites/{site_id}/forms", tags=["forms"])
# etc...

__all__ = ["api_router"]
