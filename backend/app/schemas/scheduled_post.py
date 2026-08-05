# app/schemas/scheduled_post.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

# --------------------------------------
# Post Status Enum
# --------------------------------------


class PostStatus(str, Enum):

    DRAFT = "draft"
    SCHEDULED = "scheduled"
    PROCESSING = "processing"
    PUBLISHED = "published"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PENDING_APPROVAL = "pending_approval"


# --------------------------------------
# Base Schema
# --------------------------------------


class ScheduledPostBase(BaseModel):

    title: str = Field(..., min_length=1, max_length=200)

    caption: Optional[str] = None

    media_url: Optional[str] = Field(None, max_length=500)

    platform: str = Field(..., description="linkedin, instagram, facebook, twitter")

    scheduled_time: datetime

    campaign_id: Optional[int] = None

    # Exact social account to publish with
    social_account_id: int


# --------------------------------------
# Create Post
# --------------------------------------


class ScheduledPostCreate(ScheduledPostBase):

    pass


# --------------------------------------
# Update Post
# --------------------------------------


class ScheduledPostUpdate(BaseModel):

    title: Optional[str] = None

    caption: Optional[str] = None

    media_url: Optional[str] = None

    platform: Optional[str] = None

    scheduled_time: Optional[datetime] = None

    campaign_id: Optional[int] = None

    social_account_id: Optional[int] = None

    status: Optional[PostStatus] = None


# --------------------------------------
# Response Schema
# --------------------------------------


class ScheduledPostResponse(ScheduledPostBase):

    id: int

    user_id: int

    status: PostStatus

    retry_count: int = 0

    failure_reason: Optional[str] = None

    published_at: Optional[datetime] = None

    # LinkedIn / Platform tracking

    platform_post_id: Optional[str] = None

    published_url: Optional[str] = None

    created_at: datetime

    updated_at: Optional[datetime] = None

    class Config:

        from_attributes = True


# --------------------------------------
# Analytics Response
# --------------------------------------


class ScheduledPostWithAnalytics(ScheduledPostResponse):

    likes: int = 0

    shares: int = 0

    comments: int = 0

    views: int = 0

    class Config:

        from_attributes = True
