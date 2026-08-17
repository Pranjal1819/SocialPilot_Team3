from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
)

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):

    __tablename__ = "users"

    # ==================================================
    # Primary Key
    # ==================================================

    id = Column(Integer, primary_key=True, index=True)

    # ==================================================
    # Basic Information
    # ==================================================

    name = Column(
        String(100),
        nullable=False,
    )

    email = Column(
        String(200),
        unique=True,
        nullable=False,
        index=True,
    )

    password = Column(
        String(255),
        nullable=True,
    )

    linkedin_id = Column(
        String(255),
        unique=True,
        nullable=True,
    )

    # ==================================================
    # Profile
    # ==================================================

    phone = Column(
        String(20),
        nullable=True,
    )

    organization = Column(
        String(200),
        nullable=True,
    )

    designation = Column(
        String(100),
        nullable=True,
    )

    profile_picture = Column(
        String(500),
        nullable=True,
    )

    bio = Column(
        String(500),
        nullable=True,
    )

    # ==================================================
    # Role
    # ==================================================

    role = Column(
        String(50),
        nullable=False,
    )

    # ==================================================
    # Status
    # ==================================================

    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    is_verified = Column(
        Boolean,
        default=False,
        nullable=False,
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

    # ==================================================
    # Campaigns
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
    # Posts
    # ==================================================

    scheduled_posts = relationship(
        "ScheduledPost",
        foreign_keys="ScheduledPost.user_id",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    approved_posts = relationship(
        "ScheduledPost",
        foreign_keys="ScheduledPost.approved_by",
    )

    # ==================================================
    # Social Accounts
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
    # Login Devices
    # ==================================================

    login_devices = relationship(
        "LoginDevice",
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

    # ==================================================
    # Analytics
    # Matches analytics.py:
    # user = relationship("User", back_populates="analytics")
    # ==================================================

    analytics = relationship(
        "PostAnalytics",
        back_populates="user",
        cascade="all, delete-orphan"
    )
