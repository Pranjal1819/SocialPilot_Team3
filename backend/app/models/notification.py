from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Notification(Base):

    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    message = Column(Text, nullable=False)

    type = Column(String(50), nullable=False)

    # Database column is INTEGER (0 = unread, 1 = read)
    is_read = Column(Boolean, default=0)

    created_at = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="notifications")
