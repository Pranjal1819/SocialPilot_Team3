from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime
from pathlib import Path
from typing import Optional

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.models.user import User
from app.models.generated_report import GeneratedReport
from app.models.analytics import PostAnalytics
from app.models.scheduled_post import ScheduledPost
from app.models.campaign import Campaign
from app.models.social_account import SocialAccount
from app.models.publish_log import PublishLog

from app.schemas.generated_report import (
    ReportGenerateRequest,
    GeneratedReportResponse,
    GeneratedReportListResponse,
    ReportPreviewResponse,
    ReportType,
)

router = APIRouter(prefix="/api/reports", tags=["Reports"])

REPORTS_DIR = Path(__file__).resolve().parents[1] / "static" / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def _report_scope_user(current_user: User, requested_user_id: Optional[int], db: Session) -> int:
    if requested_user_id is None:
        return current_user.id
    if current_user.role != "administrator" and requested_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only access your own reports")
    if not db.query(User).filter(User.id == requested_user_id).first():
        raise HTTPException(status_code=404, detail="User not found")
    return requested_user_id


# ==========================================================
# Helper — apply shared filters (campaign, platform,
# content_type, date range) to a PostAnalytics query joined
# with ScheduledPost
# ==========================================================


def _filtered_analytics_query(
    db: Session,
    user_id: int,
    campaign_id: Optional[int],
    platform: Optional[str],
    content_type: Optional[str],
    start_date: Optional[datetime],
    end_date: Optional[datetime],
):

    query = (
        db.query(PostAnalytics)
        .join(ScheduledPost, PostAnalytics.post_id == ScheduledPost.id)
        .filter(PostAnalytics.user_id == user_id)
    )

    if campaign_id:
        query = query.filter(PostAnalytics.campaign_id == campaign_id)

    if platform:
        query = query.filter(PostAnalytics.platform == platform)

    if content_type:
        query = query.filter(ScheduledPost.content_type == content_type)

    if start_date:
        query = query.filter(PostAnalytics.recorded_at >= start_date)

    if end_date:
        query = query.filter(PostAnalytics.recorded_at <= end_date)

    return query


def _engagement_rate(likes: int, comments: int, shares: int, reach: int) -> float:

    total = likes + comments + shares

    return round((total / reach) * 100, 1) if reach > 0 else 0


# ==========================================================
# REPORT BUILDER — Engagement
# ==========================================================


def _build_engagement_report(
    db, user_id, campaign_id, platform, content_type, start_date, end_date
) -> dict:

    rows = _filtered_analytics_query(
        db, user_id, campaign_id, platform, content_type, start_date, end_date
    ).all()

    total_likes = sum(r.likes for r in rows)
    total_comments = sum(r.comments for r in rows)
    total_shares = sum(r.shares for r in rows)
    total_saves = sum(r.saves for r in rows)
    total_clicks = sum(r.clicks for r in rows)
    total_impressions = sum(r.impressions for r in rows)
    total_reach = sum(r.reach for r in rows)

    total_engagement = total_likes + total_comments + total_shares

    engagement_rate = _engagement_rate(
        total_likes, total_comments, total_shares, total_reach
    )

    scored = sorted(
        rows, key=lambda r: (r.likes + r.comments + r.shares), reverse=True
    )[:10]

    top_posts = []

    for r in scored:

        post = db.query(ScheduledPost).filter(ScheduledPost.id == r.post_id).first()

        top_posts.append(
            {
                "post_id": r.post_id,
                "title": post.title if post else None,
                "platform": r.platform,
                "likes": r.likes,
                "comments": r.comments,
                "shares": r.shares,
                "reach": r.reach,
                "impressions": r.impressions,
                "engagement_rate": _engagement_rate(
                    r.likes, r.comments, r.shares, r.reach
                ),
            }
        )

    return {
        "summary": {
            "total_posts": len(rows),
            "likes": total_likes,
            "comments": total_comments,
            "shares": total_shares,
            "saves": total_saves,
            "clicks": total_clicks,
            "impressions": total_impressions,
            "reach": total_reach,
            "total_engagement": total_engagement,
            "engagement_rate": engagement_rate,
        },
        "tables": {"top_performing_posts": top_posts},
    }


# ==========================================================
# REPORT BUILDER — Campaign
# ==========================================================


def _build_campaign_report(
    db, user_id, campaign_id, platform, content_type, start_date, end_date
) -> dict:

    if not campaign_id:
        raise HTTPException(
            status_code=400, detail="campaign_id is required for a Campaign Report"
        )

    campaign = (
        db.query(Campaign)
        .filter(Campaign.id == campaign_id, Campaign.user_id == user_id)
        .first()
    )

    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    posts = (
        db.query(ScheduledPost)
        .filter(
            ScheduledPost.campaign_id == campaign_id,
            ScheduledPost.user_id == user_id,
        )
        .all()
    )

    rows = _filtered_analytics_query(
        db, user_id, campaign_id, platform, content_type, start_date, end_date
    ).all()

    total_likes = sum(r.likes for r in rows)
    total_comments = sum(r.comments for r in rows)
    total_shares = sum(r.shares for r in rows)
    total_impressions = sum(r.impressions for r in rows)
    total_reach = sum(r.reach for r in rows)

    total_engagement = total_likes + total_comments + total_shares

    published = len([p for p in posts if p.status == "published"])
    failed = len([p for p in posts if p.status == "failed"])
    scheduled = len([p for p in posts if p.status == "scheduled"])

    total_days = (campaign.end_date - campaign.start_date).days or 1

    elapsed_days = max(0, min((datetime.now() - campaign.start_date).days, total_days))

    completion_percentage = round((elapsed_days / total_days) * 100, 1)

    return {
        "summary": {
            "campaign_id": campaign.id,
            "campaign_name": campaign.name,
            "platform": campaign.platform,
            "description": campaign.description or "",
            "status": campaign.status,
            "start_date": campaign.start_date.isoformat(),
            "end_date": campaign.end_date.isoformat(),
            "total_posts": len(posts),
            "published_posts": published,
            "failed_posts": failed,
            "scheduled_posts": scheduled,
            "likes": total_likes,
            "comments": total_comments,
            "shares": total_shares,
            "impressions": total_impressions,
            "reach": total_reach,
            "total_engagement": total_engagement,
            "engagement_rate": _engagement_rate(
                total_likes, total_comments, total_shares, total_reach
            ),
            "completion_percentage": completion_percentage,
        },
        "tables": {
            "posts": [
                {
                    "post_id": p.id,
                    "title": p.title,
                    "platform": p.platform,
                    "status": p.status,
                    "scheduled_time": (
                        p.scheduled_time.isoformat() if p.scheduled_time else None
                    ),
                    "published_at": (
                        p.published_at.isoformat() if p.published_at else None
                    ),
                }
                for p in posts
            ]
        },
    }


# ==========================================================
# REPORT BUILDER — Audience Growth
# (No historical audience_analytics data exists yet — this
# reports CURRENT follower snapshots per platform from
# SocialAccount, not growth-over-time.)
# ==========================================================


def _build_audience_growth_report(db, user_id, platform) -> dict:

    query = db.query(SocialAccount).filter(
        SocialAccount.user_id == user_id, SocialAccount.is_active == True
    )

    if platform:
        query = query.filter(SocialAccount.platform == platform)

    accounts = query.all()

    total_followers = sum(a.followers_count for a in accounts)
    total_following = sum(a.following_count for a in accounts)

    return {
        "summary": {
            "total_accounts": len(accounts),
            "total_followers": total_followers,
            "total_following": total_following,
        },
        "tables": {
            "accounts": [
                {
                    "platform": a.platform,
                    "account_name": a.account_name,
                    "followers": a.followers_count,
                    "following": a.following_count,
                    "total_posts": a.total_posts,
                }
                for a in accounts
            ]
        },
    }


# ==========================================================
# REPORT BUILDER — Publishing
# ==========================================================


def _build_publishing_report(
    db, user_id, campaign_id, platform, content_type, start_date, end_date
) -> dict:

    query = db.query(ScheduledPost).filter(ScheduledPost.user_id == user_id)

    if campaign_id:
        query = query.filter(ScheduledPost.campaign_id == campaign_id)

    if platform:
        query = query.filter(ScheduledPost.platform == platform)

    if content_type:
        query = query.filter(ScheduledPost.content_type == content_type)

    if start_date:
        query = query.filter(ScheduledPost.created_at >= start_date)

    if end_date:
        query = query.filter(ScheduledPost.created_at <= end_date)

    posts = query.all()

    scheduled = len([p for p in posts if p.status == "scheduled"])
    published = len([p for p in posts if p.status == "published"])
    failed = len([p for p in posts if p.status == "failed"])
    cancelled = len([p for p in posts if p.status == "cancelled"])

    total_attempts = published + failed

    success_rate = (
        round((published / total_attempts) * 100, 1) if total_attempts > 0 else 0
    )

    total_retries = sum(p.retry_count or 0 for p in posts)

    post_ids = [p.id for p in posts]

    logs = (
        db.query(PublishLog)
        .filter(PublishLog.scheduled_post_id.in_(post_ids))
        .order_by(desc(PublishLog.id))
        .limit(50)
        .all()
        if post_ids
        else []
    )

    return {
        "summary": {
            "total_posts": len(posts),
            "scheduled_posts": scheduled,
            "published_posts": published,
            "failed_posts": failed,
            "cancelled_posts": cancelled,
            "publishing_success_rate": success_rate,
            "total_retry_attempts": total_retries,
        },
        "tables": {
            "publish_logs": [
                {
                    "post_id": log.scheduled_post_id,
                    "platform": log.platform,
                    "attempt_number": log.attempt_number,
                    "status": log.status,
                    "error_message": log.error_message,
                }
                for log in logs
            ]
        },
    }


# ==========================================================
# REPORT BUILDER — Platform Comparison
# (Follower Growth shown as current follower count — no
# historical audience_analytics data exists yet to compute
# true growth.)
# ==========================================================


def _build_platform_comparison_report(db, user_id, start_date, end_date) -> dict:

    query = db.query(PostAnalytics).filter(PostAnalytics.user_id == user_id)

    if start_date:
        query = query.filter(PostAnalytics.recorded_at >= start_date)

    if end_date:
        query = query.filter(PostAnalytics.recorded_at <= end_date)

    rows = query.all()

    accounts = (
        db.query(SocialAccount)
        .filter(SocialAccount.user_id == user_id, SocialAccount.is_active == True)
        .all()
    )

    followers_by_platform = {}
    for account in accounts:
        platform_name = (account.platform or "").lower()
        followers_by_platform[platform_name] = followers_by_platform.get(platform_name, 0) + (account.followers_count or 0)

    platforms = {}

    for r in rows:

        platform_name = (r.platform or "").lower()
        p = platforms.setdefault(
            platform_name,
            {
                "platform": platform_name,
                "reach": 0,
                "impressions": 0,
                "likes": 0,
                "comments": 0,
                "shares": 0,
                "clicks": 0,
            },
        )

        p["reach"] += r.reach
        p["impressions"] += r.impressions
        p["likes"] += r.likes
        p["comments"] += r.comments
        p["shares"] += r.shares
        p["clicks"] += r.clicks

    comparison = []

    for platform_name, p in platforms.items():

        engagement = p["likes"] + p["comments"] + p["shares"]

        comparison.append(
            {
                **p,
                "engagement": engagement,
                "engagement_rate": _engagement_rate(
                    p["likes"], p["comments"], p["shares"], p["reach"]
                ),
                "followers": followers_by_platform.get(platform_name, 0),
            }
        )

    comparison.sort(key=lambda p: p["engagement"], reverse=True)

    best_platform = comparison[0]["platform"] if comparison else None

    return {
        "summary": {
            "platforms_compared": len(comparison),
            "best_performing_platform": best_platform,
        },
        "tables": {"platform_comparison": comparison},
    }


# ==========================================================
# Dispatch — routes a request to the right report builder
# ==========================================================


def _build_report_data(
    db: Session, user_id: int, request: ReportGenerateRequest
) -> dict:

    if request.report_type == ReportType.ENGAGEMENT:

        return _build_engagement_report(
            db,
            user_id,
            request.campaign_id,
            request.platform,
            request.content_type,
            request.start_date,
            request.end_date,
        )

    if request.report_type == ReportType.CAMPAIGN:

        return _build_campaign_report(
            db,
            user_id,
            request.campaign_id,
            request.platform,
            request.content_type,
            request.start_date,
            request.end_date,
        )

    if request.report_type == ReportType.AUDIENCE_GROWTH:

        return _build_audience_growth_report(db, user_id, request.platform)

    if request.report_type == ReportType.PUBLISHING:

        return _build_publishing_report(
            db,
            user_id,
            request.campaign_id,
            request.platform,
            request.content_type,
            request.start_date,
            request.end_date,
        )

    if request.report_type == ReportType.PLATFORM_COMPARISON:

        return _build_platform_comparison_report(
            db, user_id, request.start_date, request.end_date
        )

    raise HTTPException(status_code=400, detail="Unsupported report type")


def _default_report_name(report_type: ReportType) -> str:

    label = report_type.value.replace("_", " ").title()

    return f"{label} Report - {datetime.now().strftime('%Y-%m-%d')}"


# ==========================================================
# PREVIEW REPORT
# ==========================================================


@router.post("/preview", response_model=ReportPreviewResponse)
def preview_report(
    request: ReportGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    user_id: Optional[int] = Query(None, ge=1),
):

    data = _build_report_data(db, _report_scope_user(current_user, user_id, db), request)

    title = request.report_name or _default_report_name(request.report_type)

    return ReportPreviewResponse(
        report_type=request.report_type,
        title=title,
        generated_at=datetime.now(),
        filters_applied=request.dict(
            exclude={"report_type", "export_format", "report_name"},
            exclude_none=True,
        ),
        summary=data["summary"],
        tables=data["tables"],
    )


# ==========================================================
# GENERATE REPORT (synchronous)
# ==========================================================


@router.post(
    "/generate",
    response_model=GeneratedReportResponse,
    status_code=status.HTTP_201_CREATED,
)
def generate_report(
    request: ReportGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    user_id: Optional[int] = Query(None, ge=1),
):

    report_user_id = _report_scope_user(current_user, user_id, db)

    report_name = request.report_name or _default_report_name(request.report_type)

    filters = jsonable_encoder(request.dict(
        exclude={"report_type", "export_format", "report_name"}, exclude_none=True
    ))

    db_report = GeneratedReport(
        user_id=report_user_id,
        campaign_id=request.campaign_id,
        report_name=report_name,
        report_type=request.report_type.value,
        filters=filters,
        export_format=request.export_format.value,
        status="processing",
    )

    db.add(db_report)
    db.commit()
    db.refresh(db_report)

    try:

        data = _build_report_data(db, report_user_id, request)

        if request.export_format.value == "excel":

            file_path = _export_excel(db_report.id, report_name, data)

        else:

            file_path = _export_pdf(db_report.id, report_name, data)

        db_report.status = "completed"
        db_report.file_path = str(file_path)

    except HTTPException:

        db.delete(db_report)
        db.commit()

        raise

    except Exception as e:

        db_report.status = "failed"
        db.commit()

        raise HTTPException(status_code=500, detail=f"Report generation failed: {e}")

    db.commit()
    db.refresh(db_report)

    return db_report


# ==========================================================
# LIST GENERATED REPORTS (Download Center)
# ==========================================================


@router.get("/", response_model=GeneratedReportListResponse)
def get_reports(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    report_type: Optional[str] = None,
    search: Optional[str] = None,
    user_id: Optional[int] = Query(None, ge=1),
):

    if current_user.role == "administrator" and user_id is None:
        query = db.query(GeneratedReport)
    else:
        scope_user_id = _report_scope_user(current_user, user_id, db)
        query = db.query(GeneratedReport).filter(GeneratedReport.user_id == scope_user_id)

    if report_type:
        query = query.filter(GeneratedReport.report_type == report_type)

    if search:
        query = query.filter(GeneratedReport.report_name.ilike(f"%{search}%"))

    query = query.order_by(desc(GeneratedReport.created_at))

    total = query.count()

    reports = query.offset(skip).limit(limit).all()

    return GeneratedReportListResponse(
        total=total, skip=skip, limit=limit, reports=reports
    )


# ==========================================================
# DOWNLOAD REPORT
# ==========================================================


@router.get("/{report_id}/download")
def download_report(
    report_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    report_query = db.query(GeneratedReport).filter(GeneratedReport.id == report_id)
    if current_user.role != "administrator":
        report_query = report_query.filter(GeneratedReport.user_id == current_user.id)
    report = report_query.first()

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    if report.status != "completed" or not report.file_path:
        raise HTTPException(status_code=400, detail="Report is not ready for download")

    file_path = Path(report.file_path)
    if not file_path.is_absolute():
        file_path = Path(__file__).resolve().parents[1] / "static" / "reports" / file_path.name

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Report file missing on disk")

    report.download_count = (report.download_count or 0) + 1
    db.commit()

    media_type = (
        "application/pdf"
        if report.export_format == "pdf"
        else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    return FileResponse(
        path=file_path,
        media_type=media_type,
        filename=file_path.name,
    )

@router.get("/{report_id}", response_model=ReportPreviewResponse)
def get_report(
    report_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return the full preview data for a saved report."""
    report_query = db.query(GeneratedReport).filter(GeneratedReport.id == report_id)
    if current_user.role != "administrator":
        report_query = report_query.filter(GeneratedReport.user_id == current_user.id)
    report = report_query.first()

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    filters = report.filters or {}
    request = ReportGenerateRequest(
        report_type=report.report_type,
        export_format=report.export_format,
        campaign_id=filters.get("campaign_id"),
        platform=filters.get("platform"),
        content_type=filters.get("content_type"),
        start_date=filters.get("start_date"),
        end_date=filters.get("end_date"),
        report_name=report.report_name,
    )
    data = _build_report_data(db, report.user_id, request)
    return ReportPreviewResponse(
        report_type=request.report_type,
        title=report.report_name,
        generated_at=report.created_at,
        filters_applied=filters,
        summary=data["summary"],
        tables=data["tables"],
    )


# ==========================================================
# DELETE REPORT
# ==========================================================


@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_report(
    report_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    report_query = db.query(GeneratedReport).filter(GeneratedReport.id == report_id)
    if current_user.role != "administrator":
        report_query = report_query.filter(GeneratedReport.user_id == current_user.id)
    report = report_query.first()

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    if report.file_path:

        file_path = Path(report.file_path)
        if not file_path.is_absolute():
            file_path = Path(__file__).resolve().parents[1] / "static" / "reports" / file_path.name

        if file_path.exists():
            file_path.unlink()

    db.delete(report)
    db.commit()

    return None


# ==========================================================
# Export — PDF (reportlab) — generic, works for any report
# type since summary/tables are already flat dicts/lists
# ==========================================================


def _export_pdf(report_id: int, title: str, data: dict) -> Path:

    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import (
        SimpleDocTemplate,
        Table,
        TableStyle,
        Paragraph,
        Spacer,
    )

    file_path = REPORTS_DIR / f"report_{report_id}.pdf"

    LEFT_MARGIN = RIGHT_MARGIN = 40

    doc = SimpleDocTemplate(
        str(file_path),
        pagesize=letter,
        leftMargin=LEFT_MARGIN,
        rightMargin=RIGHT_MARGIN,
    )

    # Full usable width between the two margins — every table is
    # stretched to fill this so nothing looks squeezed to one side.
    PAGE_WIDTH = letter[0] - LEFT_MARGIN - RIGHT_MARGIN

    styles = getSampleStyleSheet()

    # Word-wrapping cell style — plain strings in a Table never wrap,
    # so every cell is rendered as a Paragraph instead, which wraps
    # automatically and grows the row height to fit.
    cell_style = ParagraphStyle("Cell", parent=styles["Normal"], fontSize=8, leading=10)

    header_cell_style = ParagraphStyle(
        "HeaderCell",
        parent=styles["Normal"],
        fontSize=8,
        leading=10,
        textColor=colors.white,
        fontName="Helvetica-Bold",
    )

    elements = []

    elements.append(Paragraph(title, styles["Title"]))
    elements.append(
        Paragraph(
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            styles["Normal"],
        )
    )
    elements.append(Spacer(1, 20))

    header_style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4F46E5")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]
    )

    def _build_table(headers: list, rows: list) -> Table:
        """
        Builds a table stretched to the full page width, with every
        cell as a wrapping Paragraph so long text grows the row
        instead of overflowing or getting truncated.
        """

        col_width = PAGE_WIDTH / len(headers)

        wrapped_header = [Paragraph(str(h), header_cell_style) for h in headers]

        wrapped_rows = [wrapped_header]

        for row in rows:

            wrapped_rows.append([Paragraph(str(cell), cell_style) for cell in row])

        table = Table(
            wrapped_rows,
            colWidths=[col_width] * len(headers),
            hAlign="LEFT",
        )

        table.setStyle(header_style)

        return table

    # --------------------------------------------------
    # Summary table (flat key/value dict, any report type)
    # --------------------------------------------------

    summary_rows = [
        [str(key).replace("_", " ").title(), str(value)]
        for key, value in data["summary"].items()
    ]

    elements.append(Paragraph("Summary", styles["Heading2"]))
    elements.append(_build_table(["Metric", "Value"], summary_rows))
    elements.append(Spacer(1, 20))

    # --------------------------------------------------
    # Any table sections (list of dicts, any report type)
    # --------------------------------------------------

    for table_name, table_rows in data["tables"].items():

        if not table_rows:
            continue

        headers = list(table_rows[0].keys())

        rows = [[row.get(h, "") for h in headers] for row in table_rows]

        elements.append(
            Paragraph(table_name.replace("_", " ").title(), styles["Heading2"])
        )
        elements.append(_build_table(headers, rows))
        elements.append(Spacer(1, 20))

    doc.build(elements)

    return file_path


# ==========================================================
# Export — Excel (openpyxl) — generic, works for any report
# type: Summary sheet + one sheet per table section
# ==========================================================


def _autofit_sheet(sheet, header_row: int = 1, chars_per_line: int = 22):
    """
    openpyxl has no built-in "autofit" — Excel only auto-sizes columns
    /rows when a human resizes them once by hand. This approximates
    that: column width from the longest value seen (capped so one long
    cell can't blow out the whole sheet), wrap_text turned on for
    every cell, and each row's height computed from how many wrapped
    lines its tallest cell will need at that column width.
    """

    from openpyxl.styles import Alignment

    wrap_alignment = Alignment(wrap_text=True, vertical="top")

    # --------------------------------------------------
    # Column widths — based on longest cell text per column
    # --------------------------------------------------

    col_widths = {}

    for row in sheet.iter_rows():

        for cell in row:

            if cell.value is None:
                continue

            length = len(str(cell.value))

            col_widths[cell.column_letter] = max(
                col_widths.get(cell.column_letter, 10), min(length + 2, 50)
            )

    for col_letter, width in col_widths.items():
        sheet.column_dimensions[col_letter].width = width

    # --------------------------------------------------
    # Wrap text on every populated cell, and compute a row
    # height that fits the tallest wrapped cell in that row
    # --------------------------------------------------

    for row in sheet.iter_rows():

        max_lines = 1

        for cell in row:

            if cell.value is None:
                continue

            cell.alignment = wrap_alignment

            col_width = col_widths.get(cell.column_letter, chars_per_line)

            lines_needed = max(1, -(-len(str(cell.value)) // max(int(col_width), 1)))

            max_lines = max(max_lines, lines_needed)

        if max_lines > 1:
            sheet.row_dimensions[row[0].row].height = 15 * max_lines


def _export_excel(report_id: int, title: str, data: dict) -> Path:

    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill

    file_path = REPORTS_DIR / f"report_{report_id}.xlsx"

    wb = Workbook()

    header_fill = PatternFill(
        start_color="4F46E5", end_color="4F46E5", fill_type="solid"
    )
    header_font = Font(color="FFFFFF", bold=True)

    # --------------------------------------------------
    # Summary sheet
    # --------------------------------------------------

    summary_sheet = wb.active
    summary_sheet.title = "Summary"

    summary_sheet.append([title])
    summary_sheet.append([f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}"])
    summary_sheet.append([])

    summary_sheet.append(["Metric", "Value"])

    for cell in summary_sheet[4]:
        cell.fill = header_fill
        cell.font = header_font

    for key, value in data["summary"].items():
        summary_sheet.append([str(key).replace("_", " ").title(), value])

    _autofit_sheet(summary_sheet)

    # Keep every detailed table in one predictable worksheet so exported
    # files always have the required Summary and Detailed Report sheets.
    detail_sheet = wb.create_sheet("Detailed Report")
    detail_sheet.append(["Section", "Field", "Value"])
    for cell in detail_sheet[1]:
        cell.fill = header_fill
        cell.font = header_font

    for table_name, table_rows in data["tables"].items():
        for row in table_rows:
            for key, value in row.items():
                detail_sheet.append([table_name.replace("_", " ").title(), key, value])

    _autofit_sheet(detail_sheet)

    wb.save(str(file_path))

    return file_path
