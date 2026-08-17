# app/schemas/generated_report.py

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

# ==========================================================
# Report Type Enum
# ==========================================================


class ReportType(str, Enum):
    ENGAGEMENT = "engagement"
    CAMPAIGN = "campaign"
    AUDIENCE_GROWTH = "audience_growth"
    PUBLISHING = "publishing"
    PLATFORM_COMPARISON = "platform_comparison"


# ==========================================================
# Export Format Enum
# ==========================================================


class ExportFormat(str, Enum):
    PDF = "pdf"
    EXCEL = "excel"


# ==========================================================
# Report Status Enum
# ==========================================================


class ReportStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


# ==========================================================
# Generate Report — Request
# ==========================================================


class ReportGenerateRequest(BaseModel):

    report_type: ReportType

    export_format: ExportFormat

    report_name: Optional[str] = None

    campaign_id: Optional[int] = None

    platform: Optional[str] = None

    content_type: Optional[str] = None

    start_date: Optional[datetime] = None

    end_date: Optional[datetime] = None


# ==========================================================
# Generated Report — Response (Download Center row)
# ==========================================================


class GeneratedReportResponse(BaseModel):

    id: int

    user_id: int

    campaign_id: Optional[int] = None

    report_name: str

    report_type: ReportType

    filters: Optional[Dict[str, Any]] = None

    export_format: ExportFormat

    status: ReportStatus

    file_path: Optional[str] = None

    download_count: int = 0

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==========================================================
# Generated Report List — Response (paginated, Download Center)
# ==========================================================


class GeneratedReportListResponse(BaseModel):

    total: int

    skip: int = 0

    limit: int = 20

    reports: List[GeneratedReportResponse]

    model_config = ConfigDict(from_attributes=True)


# ==========================================================
# Report Preview — Response
# (data used both for preview and as the export source)
# ==========================================================


class ReportPreviewResponse(BaseModel):

    report_type: ReportType

    title: str

    generated_at: datetime

    filters_applied: Dict[str, Any]

    summary: Dict[str, Any]

    tables: Dict[str, List[dict]] = Field(default_factory=dict)
