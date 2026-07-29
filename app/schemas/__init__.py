# app/schemas/__init__.py

from .user import (
    UserBase,
    UserCreate,
    UserCreateOAuth,
    UserLogin,
    UserUpdate,
    UserResponse,
    UserProfileResponse,
    Token,
    TokenData,
    UserRole
)

from .campaign import (
    CampaignBase,
    CampaignCreate,
    CampaignUpdate,
    CampaignResponse,
    CampaignAnalytics,
    CampaignStatus
)

from .scheduled_post import (
    ScheduledPostBase,
    ScheduledPostCreate,
    ScheduledPostUpdate,
    ScheduledPostResponse,
    ScheduledPostWithAnalytics,
    PostStatus
)

from .social_account import (
    SocialAccountBase,
    SocialAccountCreate,
    SocialAccountUpdate,
    SocialAccountResponse,
    SocialAccountConnect,
    SocialAccountRefresh,
    SocialAccountConnectResponse,
    SocialPlatform
)

from .analytics import (
    PostAnalyticsBase,
    PostAnalyticsCreate,
    PostAnalyticsUpdate,
    PostAnalyticsResponse,
    AnalyticsOverview,
    AudienceAnalytics,
    PlatformAnalytics,
    PostPerformanceMetrics
)

__all__ = [
    # User schemas
    "UserBase",
    "UserCreate",
    "UserCreateOAuth",
    "UserLogin",
    "UserUpdate",
    "UserResponse",
    "UserProfileResponse",
    "Token",
    "TokenData",
    "UserRole",
    
    # Campaign schemas
    "CampaignBase",
    "CampaignCreate",
    "CampaignUpdate",
    "CampaignResponse",
    "CampaignAnalytics",
    "CampaignStatus",
    
    # Scheduled Post schemas
    "ScheduledPostBase",
    "ScheduledPostCreate",
    "ScheduledPostUpdate",
    "ScheduledPostResponse",
    "ScheduledPostWithAnalytics",
    "PostStatus",
    
    # Social Account schemas
    "SocialAccountBase",
    "SocialAccountCreate",
    "SocialAccountUpdate",
    "SocialAccountResponse",
    "SocialAccountConnect",
    "SocialAccountRefresh",
    "SocialAccountConnectResponse",
    "SocialPlatform",
    
    # Analytics schemas
    "PostAnalyticsBase",
    "PostAnalyticsCreate",
    "PostAnalyticsUpdate",
    "PostAnalyticsResponse",
    "AnalyticsOverview",
    "AudienceAnalytics",
    "PlatformAnalytics",
    "PostPerformanceMetrics",
]