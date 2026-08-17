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


class LoginDevice(Base):

    __tablename__ = "login_devices"

    # ==================================================
    # Primary Key
    # ==================================================

    id = Column(Integer, primary_key=True, index=True)

    # ==================================================
    # Owner
    # ==================================================

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    # ==================================================
    # Device Fingerprint
    # (hash of IP + User-Agent — good enough signal for a
    # "new device/location" notification without building
    # full device fingerprinting)
    # ==================================================

    fingerprint = Column(
        String(64),
        nullable=False,
        index=True,
    )

    ip_address = Column(
        String(45),  # long enough for IPv6
        nullable=True,
    )

    user_agent = Column(
        String(500),
        nullable=True,
    )

    # ==================================================
    # Audit
    # ==================================================

    first_seen_at = Column(
        DateTime,
        default=func.now(),
    )

    last_seen_at = Column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
    )

    # ==================================================
    # Relationship
    # ==================================================

    user = relationship(
        "User",
        back_populates="login_devices",
    )