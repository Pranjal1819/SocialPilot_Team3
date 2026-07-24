from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class ScheduledPost(Base):

    __tablename__ = "scheduled_posts"

    # --------------------------
    # Primary Key
    # --------------------------

    id = Column(Integer, primary_key=True, index=True)

    # --------------------------
    # User Relationship
    # --------------------------

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # --------------------------
    # Campaign Relationship
    # --------------------------
    # One campaign can contain many posts

    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=True)

    # --------------------------
    # Post Details
    # --------------------------

    title = Column(String(200), nullable=False)

    caption = Column(Text, nullable=True)

    # Content Types:
    # text
    # image
    # video
    # carousel
    # story
    # reel

    content_type = Column(String(50), nullable=False, default="text")

    media_url = Column(String(500), nullable=True)

    # --------------------------
    # Platform Details
    # --------------------------

    platform = Column(String(50), nullable=False)

    # --------------------------
    # Scheduling
    # --------------------------

    scheduled_time = Column(DateTime, nullable=True)

    # User timezone
    # Examples:
    # Asia/Kolkata
    # America/New_York
    # Europe/London

    timezone = Column(String(50), nullable=False, default="UTC")

    # --------------------------
    # Recurring Scheduling
    # --------------------------

    # True if post repeats

    is_recurring = Column(Boolean, default=False, nullable=False)

    # daily
    # weekly
    # monthly

    recurrence_type = Column(String(50), nullable=True)

    # Example:
    # Every 1 day
    # Every 2 weeks

    recurrence_interval = Column(Integer, default=1)

    # Next time recurring post runs

    next_run_time = Column(DateTime, nullable=True)

    # --------------------------
    # Publishing Status
    # --------------------------

    # draft
    # scheduled
    # processing
    # published
    # failed

    status = Column(String(50), nullable=False, default="draft")

    # Failure reason

    failure_reason = Column(Text, nullable=True)

    # Celery retry count

    retry_count = Column(Integer, default=0)

    # Actual publishing time

    published_at = Column(DateTime, nullable=True)

    # --------------------------
    # Timestamps
    # --------------------------

    created_at = Column(DateTime, default=func.now())

    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # --------------------------
    # Relationships
    # --------------------------

    # User → Scheduled Posts

    user = relationship("User", back_populates="scheduled_posts")

    # Campaign → Scheduled Posts

    campaign = relationship("Campaign", back_populates="scheduled_posts")

    # Post → Analytics

    analytics = relationship(
        "PostAnalytics", back_populates="post", cascade="all, delete-orphan"
    )
