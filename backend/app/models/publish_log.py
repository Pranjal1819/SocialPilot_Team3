from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    Index,
)

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class PublishLog(Base):

    __tablename__ = "publish_logs"

    __table_args__ = (
        Index("idx_publish_log_post", "scheduled_post_id"),
        Index("idx_publish_log_status", "status"),
    )

    # ==================================================
    # Primary Key
    # ==================================================

    id = Column(Integer, primary_key=True, index=True)

    # ==================================================
    # Relationships
    # ==================================================

    scheduled_post_id = Column(
        Integer,
        ForeignKey("scheduled_posts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    social_account_id = Column(
        Integer,
        ForeignKey("social_accounts.id"),
        nullable=True,
    )

    # ==================================================
    # Attempt Details
    # ==================================================

    platform = Column(
        String(50),
        nullable=False,
    )

    attempt_number = Column(
        Integer,
        nullable=False,
        default=1,
    )

    # success
    # failed
    # retrying

    status = Column(
        String(50),
        nullable=False,
    )

    error_message = Column(
        Text,
        nullable=True,
    )

    response_data = Column(
        Text,
        nullable=True,
    )

    # ==================================================
    # External Platform Tracking
    # ==================================================

    platform_post_id = Column(
        String(500),
        nullable=True,
    )

    published_url = Column(
        String(500),
        nullable=True,
    )

    # ==================================================
    # Audit
    # ==================================================

    created_at = Column(
        DateTime,
        default=func.now(),
    )

    # ==================================================
    # Relationships
    # ==================================================

    scheduled_post = relationship(
        "ScheduledPost",
        back_populates="publish_logs",
    )

    social_account = relationship(
        "SocialAccount",
    )
