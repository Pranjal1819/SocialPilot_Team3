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

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    platform = Column(
        String(50),
        nullable=False
    )

    account_name = Column(
        String(200),
        nullable=False
    )

    account_id = Column(
        String(200),
        nullable=True
    )

    access_token = Column(
        String(500),
        nullable=True
    )

    refresh_token = Column(
        String(500),
        nullable=True
    )

    is_connected = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        default=func.now()
    )

    user = relationship(
        "User",
        back_populates="social_accounts"
    )