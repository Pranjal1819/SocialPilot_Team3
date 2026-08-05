# app/models/campaign.py

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Campaign(Base):

    __tablename__ = "campaigns"

    # ==========================
    # Primary Key
    # ==========================

    id = Column(Integer, primary_key=True, index=True)

    # ==========================
    # Business User Owner
    # ==========================
    #
    # Business user who created the campaign
    #
    # campaigns.user_id -> users.id
    #

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    # ==========================
    # Marketing Team Manager
    # ==========================
    #
    # Marketing team member managing campaign
    #
    # campaigns.marketing_team_id -> users.id
    #

    marketing_team_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    # ==========================
    # Campaign Details
    # ==========================

    name = Column(
        String(200),
        nullable=False
    )

    description = Column(
        Text,
        nullable=True
    )

    platform = Column(
        String(50),
        nullable=False
    )

    start_date = Column(
        DateTime,
        nullable=False
    )

    end_date = Column(
        DateTime,
        nullable=False
    )

    status = Column(
        String(50),
        default="active"
    )

    created_at = Column(
        DateTime,
        default=func.now()
    )

    # ==========================
    # Relationships
    # ==========================

    # --------------------------------
    # Business User Relationship
    #
    # Example:
    # New Business
    #      |
    #      ↓
    # Campaign
    #
    # --------------------------------

    user = relationship(
        "User",
        foreign_keys=[user_id],
        back_populates="campaigns"
    )


    # --------------------------------
    # Marketing Team Relationship
    #
    # Example:
    # Marketing Team
    #        |
    #        ↓
    # Campaign
    #
    # --------------------------------

    marketing_team = relationship(
        "User",
        foreign_keys=[marketing_team_id],
        back_populates="managed_campaigns"
    )


    # --------------------------------
    # Scheduled Posts
    # --------------------------------

    scheduled_posts = relationship(
        "ScheduledPost",
        back_populates="campaign"
    )


    # --------------------------------
    # Analytics
    # --------------------------------

    analytics = relationship(
        "PostAnalytics",
        back_populates="campaign",
        cascade="all, delete-orphan"
    )