# app/schemas/campaign.py

from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum

class CampaignStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class CampaignBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    platform: str = Field(..., description="facebook, instagram, linkedin, twitter, etc.")
    start_date: datetime
    end_date: datetime
    status: Optional[CampaignStatus] = CampaignStatus.ACTIVE

class CampaignCreate(CampaignBase):
    pass

class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    platform: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[CampaignStatus] = None

class CampaignResponse(CampaignBase):
    id: int
    user_id: int
    created_at: datetime
    total_posts: int = 0
    published_posts: int = 0
    engagement_metrics: Optional[Dict] = {}
    
    class Config:
        from_attributes = True

class CampaignAnalytics(BaseModel):
    campaign_id: int
    campaign_name: str
    total_posts: int
    published_posts: int
    pending_posts: int
    failed_posts: int
    likes: int = 0
    shares: int = 0
    comments: int = 0
    views: int = 0
    engagement_rate: float = 0.0
    reach: int = 0
    impressions: int = 0
    start_date: datetime
    end_date: datetime
    
    class Config:
        from_attributes = True