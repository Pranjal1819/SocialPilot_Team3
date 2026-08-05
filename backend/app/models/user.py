# app/models/user.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):

    __tablename__ = "users"

    # =========================
    # User Columns
    # =========================

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    email = Column(String(200), unique=True, nullable=False, index=True)

    password = Column(String(255), nullable=True)

    # LinkedIn OAuth user id (optional)

    linkedin_id = Column(String(255), unique=True, nullable=True)

    # =========================
    # User Role
    # =========================

    # admin
    # business_user
    # marketing_team
    # content_creator

    role = Column(String(50), nullable=False)

    profile_picture = Column(String(500), nullable=True)

    is_active = Column(Boolean, default=True, nullable=False)

    # =========================
    # Timestamps
    # =========================

    created_at = Column(DateTime, default=func.now())

    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # ==================================================
    # Campaign Relationships
    # ==================================================

    campaigns = relationship(
        "Campaign",
        foreign_keys="Campaign.user_id",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    managed_campaigns = relationship(
        "Campaign",
        foreign_keys="Campaign.marketing_team_id",
        back_populates="marketing_team",
    )

    # ==================================================
    # Scheduled Posts
    # ==================================================

    scheduled_posts = relationship(
        "ScheduledPost",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    # ==================================================
    # Social Accounts
    #
    # User
    #   |
    #   |
    #   +---- LinkedIn Account
    #   |
    #   +---- Instagram Account
    #
    # ==================================================

    social_accounts = relationship(
        "SocialAccount",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    # ==================================================
    # Notifications
    # ==================================================

    notifications = relationship(
        "Notification",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    # ==================================================
    # Business Assignment
    # ==================================================

    business_assignments = relationship(
        "BusinessAssignment",
        foreign_keys="BusinessAssignment.business_user_id",
        back_populates="business_user",
        cascade="all, delete-orphan",
    )

    assigned_businesses = relationship(
        "BusinessAssignment",
        foreign_keys="BusinessAssignment.marketing_team_id",
        back_populates="marketing_team",
        cascade="all, delete-orphan",
    )
