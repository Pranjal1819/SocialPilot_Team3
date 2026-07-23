from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    email = Column(
        String(200),
        unique=True,
        nullable=False,
        index=True
    )

    password = Column(
        String(255),
        nullable=True
    )
    linkedin_id = Column(
        String(255),
        unique=True,
        nullable=True
        
    )
    role = Column(
        String(50),
        default="user"
    )

    profile_picture = Column(
        String(500),
        nullable=True
    )

    is_active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        default=func.now()
    )

    campaigns = relationship(
        "Campaign",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    scheduled_posts = relationship(
        "ScheduledPost",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    social_accounts = relationship(
        "SocialAccount",
        back_populates="user",
        cascade="all, delete-orphan"
    )