# app/schemas/scheduled_post.py

from pydantic import BaseModel, Field, model_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

from app.models.enums import ContentType, MEDIA_REQUIRED_CONTENT_TYPES

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
# Media Item (maps to PostMedia rows)
# --------------------------------------


class PostMediaItem(BaseModel):

    media_url: str = Field(..., max_length=500)

    media_type: str = Field(..., description="image, video, audio, gif, document")

    thumbnail_url: Optional[str] = Field(None, max_length=500)

    mime_type: Optional[str] = None

    file_size: Optional[int] = None

    duration: Optional[int] = None

    display_order: int = 1


class PostMediaResponse(PostMediaItem):

    id: int

    class Config:

        from_attributes = True


# --------------------------------------
# Base Schema
# --------------------------------------


class ScheduledPostBase(BaseModel):

    title: str = Field(..., min_length=1, max_length=200)

    caption: Optional[str] = None

    content_type: ContentType = ContentType.TEXT

    platform: str = Field(..., description="linkedin, instagram, facebook, twitter")

    scheduled_time: datetime

    campaign_id: Optional[int] = None

    # Exact social account to publish with
    social_account_id: int


# --------------------------------------
# Create Post
# --------------------------------------


class ScheduledPostCreate(ScheduledPostBase):

    media: Optional[List[PostMediaItem]] = None

    @model_validator(mode="after")
    def validate_media_for_content_type(self):

        if self.content_type in MEDIA_REQUIRED_CONTENT_TYPES and not self.media:

            raise ValueError(
                f"content_type '{self.content_type.value}' requires at least one media item"
            )

        if self.content_type == ContentType.CAROUSEL and (
            not self.media or len(self.media) < 2
        ):

            raise ValueError("content_type 'carousel' requires at least 2 media items")

        return self


# --------------------------------------
# Update Post
# --------------------------------------


class ScheduledPostUpdate(BaseModel):

    title: Optional[str] = None

    caption: Optional[str] = None

    content_type: Optional[ContentType] = None

    # Passing this replaces all existing media for the post
    media: Optional[List[PostMediaItem]] = None

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

    media_files: List[PostMediaResponse] = []

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
