from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Notification(Base):

    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # ---------------------------------------------
    # Existing fields — unchanged, still used by
    # tasks.py exactly as before
    # ---------------------------------------------

    message = Column(Text, nullable=False)

    type = Column(String(50), nullable=False)

    is_read = Column(Boolean, default=False)

    created_at = Column(DateTime, default=func.now())

    # ---------------------------------------------
    # New fields — added for Module 7 spec
    # ---------------------------------------------

    title = Column(String(200), nullable=True)

    category = Column(String(50), nullable=True)

    delivery_channel = Column(String(20), nullable=False, default="in_app")

    read_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="notifications")
