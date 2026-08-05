# app/schemas/analytics.py

from pydantic import BaseModel
from typing import Optional, Dict, List, Any
from datetime import datetime


# ==========================================
# Base Post Analytics
# ==========================================

class PostAnalyticsBase(BaseModel):

    post_id: Optional[int] = None

    campaign_id: Optional[int] = None

    user_id: int

    platform: str

    likes: int = 0

    shares: int = 0

    comments: int = 0

    views: int = 0



class PostAnalyticsCreate(PostAnalyticsBase):
    pass



class PostAnalyticsUpdate(BaseModel):

    likes: Optional[int] = None

    shares: Optional[int] = None

    comments: Optional[int] = None

    views: Optional[int] = None



class PostAnalyticsResponse(PostAnalyticsBase):

    id: int

    recorded_at: datetime


    class Config:
        from_attributes = True



# ==========================================
# Dashboard Overview
# ==========================================

class AnalyticsOverview(BaseModel):

    total_posts: int

    published_posts: int

    scheduled_posts: int

    draft_posts: int = 0

    failed_posts: int

    pending_posts: int = 0


    total_engagement: int

    total_likes: int = 0

    total_shares: int = 0

    total_comments: int = 0

    total_views: int = 0


    average_engagement_per_post: float

    engagement_rate: float

    total_reach: int

    total_impressions: int = 0

    period_days: int

    platform_breakdown: Dict = {}



# ==========================================
# Audience Analytics
# ==========================================

class AudienceAnalytics(BaseModel):

    total_followers: int

    follower_growth: List[Dict]

    demographics: Dict

    geographic_distribution: Dict


    total_likes: int

    total_shares: int

    total_comments: int

    total_views: int

    total_engagement: int


    engagement_rate: float

    period_days: int

    total_posts: int



# ==========================================
# Platform Analytics
# ==========================================

class PlatformAnalytics(BaseModel):

    platform: str

    total_posts: int

    published_posts: int = 0

    scheduled_posts: int = 0

    failed_posts: int = 0

    draft_posts: int = 0


    likes: int = 0

    shares: int = 0

    comments: int = 0

    views: int = 0


    total_engagement: int

    average_engagement: float

    engagement_rate: float = 0



# ==========================================
# Post Performance
# ==========================================

class PostPerformanceMetrics(BaseModel):

    post_id: int

    title: str

    caption: Optional[str] = None

    platform: str


    scheduled_time: Optional[datetime] = None

    published_at: Optional[datetime] = None


    likes: int

    shares: int

    comments: int

    views: int


    total_engagement: int = 0

    engagement_rate: float


    status: str

    created_at: datetime


    class Config:
        from_attributes = True



# ==========================================
# Campaign Analytics
# ==========================================

class CampaignAnalyticsResponse(BaseModel):

    campaign_id: int

    campaign_name: str

    platform: str

    description: Optional[str] = None


    start_date: datetime

    end_date: datetime

    status: str


    total_posts: int

    published_posts: int

    scheduled_posts: int

    failed_posts: int

    draft_posts: int


    likes: int = 0

    shares: int = 0

    comments: int = 0

    views: int = 0


    total_engagement: int = 0

    engagement_rate: float = 0


    post_performance: List[Dict] = []

    period_days: int



# ==========================================
# Analytics Summary
# ==========================================

class AnalyticsSummary(BaseModel):

    total_posts: int

    published_posts: int

    scheduled_posts: int

    failed_posts: int


    today_posts: int

    total_engagement: int


    active_campaigns: int

    connected_accounts: int


    recent_posts: List[Dict]



# ==========================================
# Engagement Trend
# ==========================================

class EngagementTrend(BaseModel):

    period_days: int

    data: List[Dict]


    average_daily_engagement: float

    average_daily_views: float


    total_engagement: int

    total_views: int