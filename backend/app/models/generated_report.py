from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    JSON,
)

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class GeneratedReport(Base):

    __tablename__ = "generated_reports"

    # ==================================================
    # Primary Key
    # ==================================================

    id = Column(Integer, primary_key=True, index=True)

    # ==================================================
    # Relationships
    # ==================================================

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    campaign_id = Column(
        Integer,
        ForeignKey("campaigns.id", ondelete="SET NULL"),
        nullable=True,
    )

    # ==================================================
    # Report Details
    # ==================================================

    report_name = Column(
        String(200),
        nullable=False,
    )

    # engagement
    # campaign
    # audience_growth
    # publishing
    # platform_comparison

    report_type = Column(
        String(50),
        nullable=False,
    )

    # Stores platform, content_type, date_range, etc.
    filters = Column(
        JSON,
        nullable=True,
    )

    # pdf
    # excel
    export_format = Column(
        String(20),
        nullable=False,
    )

    # pending
    # processing
    # completed
    # failed
    status = Column(
        String(20),
        nullable=False,
        default="pending",
    )

    file_path = Column(
        String(500),
        nullable=True,
    )

    download_count = Column(
        Integer,
        default=0,
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

    user = relationship("User")

    campaign = relationship("Campaign")
