# app/schemas/campaign.py

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.scheduled_post import ScheduledPostResponse

# ==========================================================
# Campaign Status Enum
# ==========================================================


class CampaignStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


# ==========================================================
# Base Schema
# ==========================================================


class CampaignBase(BaseModel):

    name: str = Field(..., min_length=1, max_length=200)

    description: Optional[str] = None

    platform: str

    start_date: datetime

    end_date: datetime

    status: CampaignStatus = CampaignStatus.ACTIVE


# ==========================================================
# Create Campaign
# ==========================================================


class CampaignCreate(CampaignBase):
    pass


# ==========================================================
# Update Campaign
# ==========================================================


class CampaignUpdate(BaseModel):

    name: Optional[str] = None

    description: Optional[str] = None

    platform: Optional[str] = None

    start_date: Optional[datetime] = None

    end_date: Optional[datetime] = None

    status: Optional[CampaignStatus] = None

    marketing_team_id: Optional[int] = None


# ==========================================================
# Status Update
# ==========================================================


class CampaignStatusUpdate(BaseModel):

    status: CampaignStatus


# ==========================================================
# Campaign Response
# ==========================================================


class CampaignResponse(CampaignBase):

    id: int

    user_id: int

    created_at: datetime

    # Post Metrics

    total_posts: int = 0

    published_posts: int = 0

    failed_posts: int = 0

    draft_posts: int = 0

    # Engagement Metrics

    likes: int = 0

    shares: int = 0

    comments: int = 0

    views: int = 0

    total_engagement: int = 0

    engagement_rate: float = 0.0

    engagement_metrics: Dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(from_attributes=True)


# ==========================================================
# Campaign Detail Response
# ==========================================================


class CampaignDetailResponse(CampaignResponse):

    # Linked Scheduled Posts
    # campaigns.id -> scheduled_posts.campaign_id

    posts: List[ScheduledPostResponse] = Field(default_factory=list)

    # Analytics

    analytics: Optional[Dict[str, Any]] = None

    engagement_over_time: List[dict] = Field(default_factory=list)

    post_performance: List[dict] = Field(default_factory=list)

    progress: float = 0.0

    model_config = ConfigDict(from_attributes=True)


# ==========================================================
# Campaign List Response
# ==========================================================


class CampaignListResponse(BaseModel):

    total: int

    skip: int = 0

    limit: int = 20

    campaigns: List[CampaignResponse]

    model_config = ConfigDict(from_attributes=True)


# ==========================================================
# Campaign Analytics
# ==========================================================


class CampaignAnalytics(BaseModel):

    campaign_id: int

    campaign_name: str

    platform: str

    start_date: datetime

    end_date: datetime

    status: str

    total_posts: int = 0

    published_posts: int = 0

    scheduled_posts: int = 0

    failed_posts: int = 0

    draft_posts: int = 0

    likes: int = 0

    shares: int = 0

    comments: int = 0

    views: int = 0

    total_engagement: int = 0

    engagement_rate: float = 0.0

    daily_performance: List[dict] = Field(default_factory=list)

    platform_breakdown: List[dict] = Field(default_factory=list)

    period_days: int = 30

    model_config = ConfigDict(from_attributes=True)


# ==========================================================
# Campaign Performance Metrics
# ==========================================================


class CampaignPerformanceMetrics(BaseModel):

    total_campaigns: int = 0

    active_campaigns: int = 0

    completed_campaigns: int = 0

    paused_campaigns: int = 0

    cancelled_campaigns: int = 0

    total_likes: int = 0

    total_shares: int = 0

    total_comments: int = 0

    total_views: int = 0

    total_engagement: int = 0

    average_engagement_per_campaign: float = 0.0

    best_performing_campaign: Optional[dict] = None

    period_days: int = 30

    model_config = ConfigDict(from_attributes=True)
