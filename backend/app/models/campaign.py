from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Campaign(Base):

    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    name = Column(String(200), nullable=False)

    description = Column(Text, nullable=True)

    platform = Column(String(50), nullable=False)

    start_date = Column(DateTime, nullable=False)

    end_date = Column(DateTime, nullable=False)

    status = Column(String(50), default="active")

    created_at = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="campaigns")
    scheduled_posts = relationship("ScheduledPost", back_populates="campaign")

    analytics = relationship(
        "PostAnalytics", back_populates="campaign", cascade="all, delete-orphan"
    )
