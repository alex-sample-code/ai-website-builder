"""
API v1 routes
"""

from fastapi import APIRouter
from app.api.v1 import (
    auth, sites, pages, health,
    blog, forms, publish, settings, assets,
    analytics, team, integrations, templates,
    public, ai
)

api_router = APIRouter()

# Include all route modules
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(sites.router, prefix="/sites", tags=["sites"])
api_router.include_router(pages.router, prefix="/sites/{site_id}/pages", tags=["pages"])

# Blog routes
api_router.include_router(blog.router, prefix="/sites/{site_id}/blog", tags=["blog"])

# Form routes
api_router.include_router(forms.router, prefix="/sites/{site_id}/forms", tags=["forms"])

# Publish routes
api_router.include_router(publish.router, prefix="/sites", tags=["publish"])

# Settings routes
api_router.include_router(settings.router, prefix="/sites", tags=["settings"])

# Asset routes
api_router.include_router(assets.router, prefix="/sites", tags=["assets"])

# Analytics routes
api_router.include_router(analytics.router, prefix="/sites", tags=["analytics"])

# Team routes
api_router.include_router(team.router, prefix="/team", tags=["team"])

# Integration routes
api_router.include_router(integrations.router, prefix="/sites", tags=["integrations"])

# Template routes
api_router.include_router(templates.router, prefix="/templates", tags=["templates"])

# AI routes
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])

# Public routes (no auth required)
api_router.include_router(public.router, prefix="/public", tags=["public"])

__all__ = ["api_router"]
