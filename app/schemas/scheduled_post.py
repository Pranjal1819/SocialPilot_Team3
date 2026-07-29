# app/schemas/scheduled_post.py

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class PostStatus(str, Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PENDING_APPROVAL = "pending_approval"

class ScheduledPostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    caption: Optional[str] = None
    media_url: Optional[str] = Field(None, max_length=500)
    platform: str = Field(..., description="facebook, instagram, linkedin, twitter, etc.")
    scheduled_time: datetime
    campaign_id: Optional[int] = None

class ScheduledPostCreate(ScheduledPostBase):
    pass

class ScheduledPostUpdate(BaseModel):
    title: Optional[str] = None
    caption: Optional[str] = None
    media_url: Optional[str] = None
    platform: Optional[str] = None
    scheduled_time: Optional[datetime] = None
    status: Optional[PostStatus] = None

class ScheduledPostResponse(ScheduledPostBase):
    id: int
    user_id: int
    status: PostStatus
    published_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class ScheduledPostWithAnalytics(ScheduledPostResponse):
    """Post with analytics data"""
    likes: int = 0
    shares: int = 0
    comments: int = 0
    views: int = 0
    
    class Config:
        from_attributes = True