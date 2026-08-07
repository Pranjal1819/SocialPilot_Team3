from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class PostMedia(Base):

    __tablename__ = "post_media"

    id = Column(Integer, primary_key=True, index=True)

    post_id = Column(
        Integer,
        ForeignKey("scheduled_posts.id", ondelete="CASCADE"),
        nullable=False,
    )

    media_url = Column(String(500), nullable=False)

    file_path = Column(String(500), nullable=True)

    media_type = Column(String(50), nullable=False)

    thumbnail_url = Column(String(500), nullable=True)

    mime_type = Column(String(100), nullable=True)

    file_size = Column(Integer, nullable=True)

    duration = Column(Integer, nullable=True)

    display_order = Column(Integer, default=1)

    created_at = Column(DateTime, default=func.now())

    post = relationship("ScheduledPost", back_populates="media_files")
