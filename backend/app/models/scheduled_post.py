from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
    ForeignKey,
    Boolean,
)

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class ScheduledPost(Base):

    __tablename__ = "scheduled_posts"

    # ==================================================
    # Primary Key
    # ==================================================

    id = Column(Integer, primary_key=True, index=True)

    # ==================================================
    # Relationships
    # ==================================================

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    campaign_id = Column(
        Integer,
        ForeignKey("campaigns.id"),
        nullable=True,
    )

    social_account_id = Column(
        Integer,
        ForeignKey("social_accounts.id"),
        nullable=True,
    )

    # ==================================================
    # Post Details
    # ==================================================

    title = Column(
        String(200),
        nullable=False,
    )

    caption = Column(
        Text,
        nullable=True,
    )

    # text
    # image
    # video
    # carousel
    # story
    # reel
    # audio
    # document

    content_type = Column(
        String(50),
        nullable=False,
        default="text",
    )

    hashtags = Column(
        Text,
        nullable=True,
    )

    mentions = Column(
        Text,
        nullable=True,
    )

    first_comment = Column(
        Text,
        nullable=True,
    )

    # ==================================================
    # Platform
    # ==================================================

    platform = Column(
        String(50),
        nullable=False,
    )

    # linkedin
    # instagram
    # facebook
    # x
    # youtube
    # pinterest

    # ==================================================
    # Scheduling
    # ==================================================

    scheduled_time = Column(
        DateTime,
        nullable=True,
    )

    timezone = Column(
        String(50),
        nullable=False,
        default="UTC",
    )

    # ==================================================
    # Recurring Schedule
    # ==================================================

    is_recurring = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    recurrence_type = Column(
        String(50),
        nullable=True,
    )
    # daily
    # weekly
    # monthly

    recurrence_interval = Column(
        Integer,
        default=1,
    )

    next_run_time = Column(
        DateTime,
        nullable=True,
    )

    recurrence_end_date = Column(
        DateTime,
        nullable=True,
    )

    # ==================================================
    # Approval Workflow
    # ==================================================

    approval_status = Column(
        String(50),
        nullable=False,
        default="pending",
    )
    # pending
    # approved
    # rejected

    approved_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
    )

    approved_at = Column(
        DateTime,
        nullable=True,
    )

    # ==================================================
    # Publishing Status
    # ==================================================

    status = Column(
        String(50),
        nullable=False,
        default="draft",
    )
    # draft
    # scheduled
    # processing
    # published
    # failed
    # cancelled
    # partially_published

    failure_reason = Column(
        Text,
        nullable=True,
    )

    retry_count = Column(
        Integer,
        default=0,
    )

    published_at = Column(
        DateTime,
        nullable=True,
    )

    # ==================================================
    # External Platform Tracking
    # ==================================================

    platform_post_id = Column(
        String(500),
        nullable=True,
    )

    published_url = Column(
        String(500),
        nullable=True,
    )

    # ==================================================
    # Audit
    # ==================================================

    created_at = Column(
        DateTime,
        default=func.now(),
    )

    updated_at = Column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
    )

    is_deleted = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    # ==================================================
    # Relationships
    # ==================================================

    user = relationship(
        "User",
        foreign_keys=[user_id],
        back_populates="scheduled_posts",
    )

    campaign = relationship(
        "Campaign",
        back_populates="scheduled_posts",
    )

    social_account = relationship(
        "SocialAccount",
        back_populates="scheduled_posts",
    )

    media_files = relationship(
        "PostMedia",
        back_populates="post",
        cascade="all, delete-orphan",
    )

    analytics = relationship(
        "PostAnalytics",
        back_populates="post",
        cascade="all, delete-orphan",
    )
    publish_logs = relationship(
    "PublishLog",
    back_populates="scheduled_post",
    cascade="all, delete-orphan",
)