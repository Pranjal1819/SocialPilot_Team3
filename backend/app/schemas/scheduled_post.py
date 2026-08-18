# app/schemas/scheduled_post.py

from pydantic import BaseModel, Field, model_validator, field_validator
from typing import Optional, List
from datetime import datetime, timezone, timedelta
from enum import Enum

from app.models.enums import ContentType, MEDIA_REQUIRED_CONTENT_TYPES

IST = timezone(timedelta(hours=5, minutes=30))


def parse_scheduled_time(value):
    """
    Accepts scheduled_time as either:
      - 12-hour format: "2026-08-18 10:45 AM" or "2026-08-18 10:45:00 AM"
      - Standard ISO format: "2026-08-18T10:45:00" or "...Z" (UTC)
    Returns a datetime object either way.
    """

    if isinstance(value, datetime):
        return value

    if isinstance(value, str):

        for fmt in ("%Y-%m-%d %I:%M %p", "%Y-%m-%d %I:%M:%S %p"):
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue

        # Fall back to ISO parsing (handles "...T...:00" and "...Z")
        return datetime.fromisoformat(value.replace("Z", "+00:00"))

    return value


def normalize_to_ist(dt: datetime) -> datetime:
    """
    Ensures scheduled_time always represents IST wall-clock time,
    stored as a naive datetime (matching this server's local clock,
    which is IST — see tasks.py's datetime.now() comparisons).

    - Naive input (no tzinfo) is assumed to ALREADY be IST wall-clock
      time, exactly as the user picked it — no conversion.
    - Timezone-aware input (e.g. a "...Z" / UTC string) is converted
      to IST, then stripped of tzinfo, so it still compares cleanly
      against the naive datetime.now() used elsewhere.
    """

    if dt.tzinfo is None:
        return dt

    return dt.astimezone(IST).replace(tzinfo=None)


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

    @field_validator("scheduled_time", mode="before")
    @classmethod
    def parse_time(cls, value):
        return parse_scheduled_time(value)


# --------------------------------------
# Create Post
# --------------------------------------


class ScheduledPostCreate(ScheduledPostBase):

    media: Optional[List[PostMediaItem]] = None

    status: PostStatus = PostStatus.SCHEDULED

    @model_validator(mode="after")
    def normalize_scheduled_time(self):

        self.scheduled_time = normalize_to_ist(self.scheduled_time)

        return self

    @model_validator(mode="after")
    def validate_media_for_content_type(self):

        if self.status not in (PostStatus.DRAFT, PostStatus.SCHEDULED):

            raise ValueError(
                "status on create must be 'draft' or 'scheduled'"
            )

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

    @field_validator("scheduled_time", mode="before")
    @classmethod
    def parse_time(cls, value):

        if value is None:
            return value

        return parse_scheduled_time(value)

    @model_validator(mode="after")
    def normalize_scheduled_time(self):

        if self.scheduled_time is not None:
            self.scheduled_time = normalize_to_ist(self.scheduled_time)

        return self


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