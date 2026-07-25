from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class PostAnalytics(Base):

    __tablename__ = "post_analytics"

    id = Column(Integer, primary_key=True, index=True)

    post_id = Column(
        Integer,
        ForeignKey("scheduled_posts.id"),
        nullable=True
    )

    campaign_id = Column(
        Integer,
        ForeignKey("campaigns.id"),
        nullable=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    platform = Column(String(50), nullable=False)

    likes = Column(Integer, default=0)

    shares = Column(Integer, default=0)

    comments = Column(Integer, default=0)

    views = Column(Integer, default=0)

    recorded_at = Column(
        DateTime,
        default=func.now()
    )

    user = relationship("User")

    campaign = relationship(
        "Campaign",
        back_populates="analytics"
    )

    post = relationship(
        "ScheduledPost",
        back_populates="analytics"
    )