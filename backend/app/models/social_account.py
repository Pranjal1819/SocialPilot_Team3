from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class SocialAccount(Base):

    __tablename__ = "social_accounts"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # User relation
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Platform details
    # Instagram, Facebook, LinkedIn
    platform = Column(String(50), nullable=False)

    account_name = Column(String(200), nullable=False)

    account_id = Column(String(200), nullable=True)

    # OAuth tokens

    access_token = Column(String(500), nullable=True)

    refresh_token = Column(String(500), nullable=True)

    # Token expiry time
    # Used by Celery auto refresh task

    token_expires_at = Column(DateTime, nullable=True)

    # Account connection status

    is_connected = Column(Boolean, default=True)

    # Active status
    # Used in refresh_expiring_tokens()

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=func.now())

    # -------------------------
    # Relationships
    # -------------------------

    user = relationship("User", back_populates="social_accounts")
