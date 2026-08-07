from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
    UniqueConstraint,
    Index,
)

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class SocialAccount(Base):

    __tablename__ = "social_accounts"

    __table_args__ = (
        UniqueConstraint(
            "platform",
            "account_id",
            name="unique_platform_account",
        ),
        Index("idx_social_platform", "platform"),
        Index("idx_social_account_id", "account_id"),
    )

    # ==================================================
    # Primary Key
    # ==================================================

    id = Column(Integer, primary_key=True, index=True)

    # ==================================================
    # User Relationship
    # ==================================================

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ==================================================
    # Platform Details
    # ==================================================

    # linkedin
    # instagram
    # facebook
    # x
    # youtube
    # pinterest

    platform = Column(
        String(50),
        nullable=False,
    )

    account_name = Column(
        String(200),
        nullable=False,
    )

    # OAuth Provider User ID

    account_id = Column(
        String(200),
        nullable=True,
    )

    profile_url = Column(
        String(500),
        nullable=True,
    )

    profile_picture = Column(
        String(500),
        nullable=True,
    )

    # ==================================================
    # OAuth Tokens
    # ==================================================

    access_token = Column(
        Text,
        nullable=True,
    )

    refresh_token = Column(
        Text,
        nullable=True,
    )

    token_expires_at = Column(
        DateTime,
        nullable=True,
    )

    # ==================================================
    # Analytics Snapshot
    # ==================================================

    followers_count = Column(
        Integer,
        default=0,
    )

    following_count = Column(
        Integer,
        default=0,
    )

    total_posts = Column(
        Integer,
        default=0,
    )

    # ==================================================
    # Connection Status
    # ==================================================

    is_connected = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    last_synced = Column(
        DateTime,
        nullable=True,
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
    # Relationships
    # ==================================================

    user = relationship(
        "User",
        back_populates="social_accounts",
    )

    scheduled_posts = relationship(
        "ScheduledPost",
        back_populates="social_account",
        cascade="all, delete-orphan",
    )
