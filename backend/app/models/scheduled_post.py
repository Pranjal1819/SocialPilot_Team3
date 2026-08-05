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

    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=True)

    # --------------------------
    # Social Account Relationship
    # --------------------------
    #
    # Exact social account used
    # for publishing
    #
    # Example:
    #
    # User
    #    |
    #    |-- LinkedIn Account A
    #    |
    #    |-- LinkedIn Account B
    #
    # Post selects one account
    #

    social_account_id = Column(Integer, ForeignKey("social_accounts.id"), nullable=True)

    # --------------------------
    # Post Details
    # --------------------------

    title = Column(String(200), nullable=False)

    caption = Column(Text, nullable=True)

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

    timezone = Column(String(50), nullable=False, default="UTC")

    # --------------------------
    # Recurring Scheduling
    # --------------------------

    is_recurring = Column(Boolean, default=False, nullable=False)

    recurrence_type = Column(String(50), nullable=True)

    recurrence_interval = Column(Integer, default=1)

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

    failure_reason = Column(Text, nullable=True)

    retry_count = Column(Integer, default=0)

    published_at = Column(DateTime, nullable=True)

    # --------------------------
    # External Platform Tracking
    # --------------------------

    # LinkedIn share URN
    # Example:
    # urn:li:share:7488501498956591105

    platform_post_id = Column(String(500), nullable=True)

    # Public URL

    published_url = Column(String(500), nullable=True)

    # --------------------------
    # Timestamps
    # --------------------------

    created_at = Column(DateTime, default=func.now())

    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # --------------------------
    # Relationships
    # --------------------------

    user = relationship("User", back_populates="scheduled_posts")

    campaign = relationship("Campaign", back_populates="scheduled_posts")

    social_account = relationship("SocialAccount", back_populates="scheduled_posts")

    analytics = relationship(
        "PostAnalytics", back_populates="post", cascade="all, delete-orphan"
    )
