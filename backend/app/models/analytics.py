from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    JSON,
)

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class PostAnalytics(Base):

    __tablename__ = "post_analytics"

    # ==================================================
    # Primary Key
    # ==================================================

    id = Column(Integer, primary_key=True, index=True)

    # ==================================================
    # Relationships
    # ==================================================

    post_id = Column(
        Integer,
        ForeignKey("scheduled_posts.id", ondelete="CASCADE"),
        nullable=False,
    )

    campaign_id = Column(
        Integer,
        ForeignKey("campaigns.id", ondelete="CASCADE"),
        nullable=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
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
    # Engagement Metrics
    # ==================================================

    likes = Column(
        Integer,
        default=0,
    )

    shares = Column(
        Integer,
        default=0,
    )

    comments = Column(
        Integer,
        default=0,
    )

    views = Column(
        Integer,
        default=0,
    )

    # ==================================================
    # Reach / Delivery Metrics
    # ==================================================
    #
    # Added for Module 6 - Analytics Dashboard
    # Required by Content/Platform/Campaign analytics
    #

    reach = Column(
        Integer,
        default=0,
    )

    impressions = Column(
        Integer,
        default=0,
    )

    clicks = Column(
        Integer,
        default=0,
    )

    saves = Column(
        Integer,
        default=0,
    )

    # ==================================================
    # Analytics Timestamp
    # ==================================================

    recorded_at = Column(
        DateTime,
        default=func.now(),
    )

    # ==================================================
    # Relationships
    # ==================================================

    user = relationship(
        "User",
        back_populates="analytics",
    )

    campaign = relationship(
        "Campaign",
        back_populates="analytics",
    )

    post = relationship(
        "ScheduledPost",
        back_populates="analytics",
    )


class AudienceAnalytics(Base):

    __tablename__ = "audience_analytics"

    # ==================================================
    # Primary Key
    # ==================================================

    id = Column(Integer, primary_key=True, index=True)

    # ==================================================
    # Relationships
    # ==================================================

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    social_account_id = Column(
        Integer,
        ForeignKey("social_accounts.id", ondelete="CASCADE"),
        nullable=True,
    )

    # ==================================================
    # Platform
    # ==================================================

    platform = Column(
        String(50),
        nullable=False,
    )

    # ==================================================
    # Follower Metrics
    # ==================================================

    total_followers = Column(
        Integer,
        default=0,
    )

    new_followers = Column(
        Integer,
        default=0,
    )

    lost_followers = Column(
        Integer,
        default=0,
    )

    net_growth = Column(
        Integer,
        default=0,
    )

    # ==================================================
    # Audience Details
    # ==================================================

    gender_distribution = Column(
        JSON,
        nullable=True,
    )

    age_distribution = Column(
        JSON,
        nullable=True,
    )

    country = Column(
        String(100),
        nullable=True,
    )

    city = Column(
        String(100),
        nullable=True,
    )

    languages = Column(
        JSON,
        nullable=True,
    )

    # ==================================================
    # Activity
    # ==================================================

    most_active_hours = Column(
        JSON,
        nullable=True,
    )

    most_active_days = Column(
        JSON,
        nullable=True,
    )

    # ==================================================
    # Analytics Timestamp
    # ==================================================

    recorded_at = Column(
        DateTime,
        default=func.now(),
    )

    # ==================================================
    # Relationships
    # ==================================================

    user = relationship(
        "User",
    )

    social_account = relationship(
        "SocialAccount",
    )


class CampaignAnalyticsSnapshot(Base):

    __tablename__ = "campaign_analytics_snapshots"

    # ==================================================
    # Primary Key
    # ==================================================

    id = Column(Integer, primary_key=True, index=True)

    # ==================================================
    # Relationships
    # ==================================================

    campaign_id = Column(
        Integer,
        ForeignKey("campaigns.id", ondelete="CASCADE"),
        nullable=False,
    )

    # ==================================================
    # Campaign Metrics
    # ==================================================

    total_posts = Column(
        Integer,
        default=0,
    )

    reach = Column(
        Integer,
        default=0,
    )

    impressions = Column(
        Integer,
        default=0,
    )

    engagement = Column(
        Integer,
        default=0,
    )

    clicks = Column(
        Integer,
        default=0,
    )

    likes = Column(
        Integer,
        default=0,
    )

    roi = Column(
        Integer,
        nullable=True,
    )

    completion_percentage = Column(
        Integer,
        default=0,
    )

    # ==================================================
    # Analytics Timestamp
    # ==================================================

    recorded_at = Column(
        DateTime,
        default=func.now(),
    )

    # ==================================================
    # Relationships
    # ==================================================

    campaign = relationship(
        "Campaign",
    )


class PlatformAnalytics(Base):

    __tablename__ = "platform_analytics"

    # ==================================================
    # Primary Key
    # ==================================================

    id = Column(Integer, primary_key=True, index=True)

    # ==================================================
    # Relationships
    # ==================================================

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    # ==================================================
    # Platform
    # ==================================================

    platform_name = Column(
        String(50),
        nullable=False,
    )

    # ==================================================
    # Platform Metrics
    # ==================================================

    followers = Column(
        Integer,
        default=0,
    )

    reach = Column(
        Integer,
        default=0,
    )

    engagement = Column(
        Integer,
        default=0,
    )

    impressions = Column(
        Integer,
        default=0,
    )

    clicks = Column(
        Integer,
        default=0,
    )

    # ==================================================
    # Analytics Timestamp
    # ==================================================

    recorded_at = Column(
        DateTime,
        default=func.now(),
    )

    # ==================================================
    # Relationships
    # ==================================================

    user = relationship(
        "User",
    )
