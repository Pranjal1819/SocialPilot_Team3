# app/schemas/analytics.py

from pydantic import BaseModel
from typing import Optional, Dict, List
from datetime import datetime

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

class AnalyticsOverview(BaseModel):
    """Dashboard overview analytics"""
    total_posts: int
    published_posts: int
    scheduled_posts: int
    failed_posts: int
    total_engagement: int
    average_engagement_per_post: float
    total_reach: int
    total_impressions: int
    
class AudienceAnalytics(BaseModel):
    """Audience analytics data"""
    follower_growth: List[Dict]  # List of {date: str, followers: int}
    demographics: Dict  # Age distribution
    geographic_distribution: Dict  # Country distribution
    active_hours: Dict  # Best posting times

class PlatformAnalytics(BaseModel):
    """Analytics per platform"""
    platform: str
    total_posts: int
    total_engagement: int
    likes: int
    shares: int
    comments: int
    views: int
    average_engagement: float

class PostPerformanceMetrics(BaseModel):
    """Individual post performance metrics"""
    post_id: int
    title: str
    platform: str
    scheduled_time: datetime
    published_at: Optional[datetime]
    likes: int
    shares: int
    comments: int
    views: int
    engagement_rate: float
    
    class Config:
        from_attributes = True