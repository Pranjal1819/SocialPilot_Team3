from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class ScheduledPost(Base):

    __tablename__ = "scheduled_posts"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    title = Column(String(200), nullable=False)

    caption = Column(Text)

    media_url = Column(String(500))

    platform = Column(String(50), nullable=False)

    scheduled_time = Column(DateTime, nullable=False)

    status = Column(
        String(50),
        default="scheduled"
    )

    published_at = Column(DateTime)

    created_at = Column(
        DateTime,
        default=func.now()
    )

    user = relationship(
        "User",
        back_populates="scheduled_posts"
    )

    analytics = relationship(
        "PostAnalytics",
        back_populates="post",
        cascade="all, delete-orphan"
    )