from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class NotificationPreference(Base):

    __tablename__ = "notification_preferences"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    # ---------------------------------------------
    # Category toggles
    # ---------------------------------------------

    publishing_enabled = Column(Boolean, default=True, nullable=False)

    campaign_enabled = Column(Boolean, default=True, nullable=False)

    account_activity_enabled = Column(Boolean, default=True, nullable=False)

    team_collaboration_enabled = Column(Boolean, default=True, nullable=False)

    system_enabled = Column(Boolean, default=True, nullable=False)

    # ---------------------------------------------
    # Channel toggles
    # ---------------------------------------------

    in_app_enabled = Column(Boolean, default=True, nullable=False)

    email_enabled = Column(Boolean, default=True, nullable=False)

    push_enabled = Column(Boolean, default=False, nullable=False)

    # ---------------------------------------------
    # Email preferences
    # ---------------------------------------------

    # immediate / daily / weekly
    email_frequency = Column(String(20), default="immediate", nullable=False)

    promotional_emails_enabled = Column(Boolean, default=False, nullable=False)

    # ---------------------------------------------
    # Audit
    # ---------------------------------------------

    created_at = Column(DateTime, default=func.now())

    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    user = relationship("User")