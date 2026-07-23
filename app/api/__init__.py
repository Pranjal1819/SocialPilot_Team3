# app/api/__init__.py

from .auth import router as auth_router
from .posts import router as posts_router
from .campaigns import router as campaigns_router
from .social import router as social_router
from .analytics import router as analytics_router

__all__ = ["auth_router", "posts_router", "campaigns_router", "social_router", "analytics_router"]