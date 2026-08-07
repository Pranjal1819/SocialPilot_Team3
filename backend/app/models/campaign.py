from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Campaign(Base):

    __tablename__ = "campaigns"

    # ==================================================
    # Primary Key
    # ==================================================

    id = Column(Integer, primary_key=True, index=True)

    # ==================================================
    # Business User Owner
    # ==================================================

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # ==================================================
    # Marketing Team Manager
    # ==================================================

    marketing_team_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # ==================================================
    # Campaign Details
    # ==================================================

    name = Column(String(200), nullable=False)

    description = Column(Text, nullable=True)

    platform = Column(String(50), nullable=False)

    start_date = Column(DateTime, nullable=False)

    end_date = Column(DateTime, nullable=False)

    status = Column(String(50), default="active")

    # ==================================================
    # Audit
    # ==================================================

    created_at = Column(DateTime, default=func.now())

    # ==================================================
    # Relationships
    # ==================================================

    user = relationship("User", foreign_keys=[user_id], back_populates="campaigns")

    marketing_team = relationship(
        "User", foreign_keys=[marketing_team_id], back_populates="managed_campaigns"
    )

    scheduled_posts = relationship(
        "ScheduledPost", back_populates="campaign", cascade="all, delete-orphan"
    )

    # ==================================================
    # Analytics
    # Matches analytics.py:
    #
    # campaign = relationship(
    #     "Campaign",
    #     back_populates="analytics"
    # )
    #
    # ==================================================

    analytics = relationship(
        "PostAnalytics", back_populates="campaign", cascade="all, delete-orphan"
    )
