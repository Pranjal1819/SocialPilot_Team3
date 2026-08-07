from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class BusinessAssignment(Base):

    __tablename__ = "business_assignments"

    id = Column(Integer, primary_key=True, index=True)

    business_user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    marketing_team_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    assigned_at = Column(
        DateTime,
        server_default=func.now(),
    )

    # Business User
    business_user = relationship(
        "User",
        foreign_keys=[business_user_id],
        back_populates="business_assignments",
    )

    # Marketing Team
    marketing_team = relationship(
        "User",
        foreign_keys=[marketing_team_id],
        back_populates="assigned_businesses",
    )

    __table_args__ = (
        UniqueConstraint(
            "business_user_id",
            "marketing_team_id",
            name="uq_business_marketing",
        ),
    )
