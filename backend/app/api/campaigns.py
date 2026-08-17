from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, or_
from datetime import datetime, timedelta
from typing import Optional

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.models.user import User
from app.models.campaign import Campaign
from app.models.scheduled_post import ScheduledPost
from app.models.analytics import PostAnalytics

from app.schemas.campaign import (
    CampaignCreate,
    CampaignUpdate,
    CampaignResponse,
    CampaignDetailResponse,
    CampaignAnalytics,
    CampaignListResponse,
    CampaignStatusUpdate,
    CampaignPerformanceMetrics,
)

from app.services.notification_service import NotificationService

router = APIRouter(prefix="/api/campaigns", tags=["Campaigns"])


# ==========================================================
# Helper — build a CampaignResponse with post/engagement metrics
# ==========================================================


def _build_campaign_response(db: Session, campaign: Campaign) -> CampaignResponse:

    posts = (
        db.query(ScheduledPost).filter(ScheduledPost.campaign_id == campaign.id).all()
    )

    analytics = (
        db.query(PostAnalytics).filter(PostAnalytics.campaign_id == campaign.id).all()
    )

    published = len([p for p in posts if p.status == "published"])
    failed = len([p for p in posts if p.status == "failed"])
    drafts = len([p for p in posts if p.status == "draft"])

    likes = sum(a.likes for a in analytics)
    shares = sum(a.shares for a in analytics)
    comments = sum(a.comments for a in analytics)
    views = sum(a.views for a in analytics)

    engagement = likes + shares + comments

    return CampaignResponse(
        id=campaign.id,
        name=campaign.name,
        description=campaign.description,
        platform=campaign.platform,
        start_date=campaign.start_date,
        end_date=campaign.end_date,
        status=campaign.status,
        user_id=campaign.user_id,
        created_at=campaign.created_at,
        total_posts=len(posts),
        published_posts=published,
        failed_posts=failed,
        draft_posts=drafts,
        likes=likes,
        shares=shares,
        comments=comments,
        views=views,
        total_engagement=engagement,
        engagement_rate=(engagement / views * 100 if views > 0 else 0),
        engagement_metrics={
            "likes": likes,
            "shares": shares,
            "comments": comments,
            "views": views,
        },
    )


# ==========================================================
# Helper — fire the right notification for a status transition
# ==========================================================


def _notify_status_change(
    db: Session, user_id: int, campaign: Campaign, previous_status: str
):

    new_status = campaign.status

    if new_status == previous_status:
        return

    if new_status == "active":

        NotificationService(db).create_notification(
            user_id=user_id,
            title="Campaign Started",
            description=f'Your campaign "{campaign.name}" has started.',
            category="campaigns",
            notification_type="campaign_started",
        )

    elif new_status == "completed":

        NotificationService(db).create_notification(
            user_id=user_id,
            title="Campaign Completed",
            description=f'Your campaign "{campaign.name}" has been completed.',
            category="campaigns",
            notification_type="campaign_completed",
        )


# ==========================================================
# CREATE CAMPAIGN
# ==========================================================


@router.post("/", response_model=CampaignResponse, status_code=status.HTTP_201_CREATED)
def create_campaign(
    campaign: CampaignCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    if campaign.start_date >= campaign.end_date:
        raise HTTPException(
            status_code=400, detail="Start date must be before end date"
        )

    existing = (
        db.query(Campaign)
        .filter(Campaign.user_id == current_user.id, Campaign.name == campaign.name)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400, detail="Campaign with this name already exists"
        )

    db_campaign = Campaign(
        name=campaign.name,
        description=campaign.description,
        platform=campaign.platform,
        start_date=campaign.start_date,
        end_date=campaign.end_date,
        status="active",
        user_id=current_user.id,
    )

    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)

    NotificationService(db).create_notification(
        user_id=current_user.id,
        title="Campaign Created",
        description=f'Your campaign "{db_campaign.name}" was created successfully.',
        category="campaigns",
        notification_type="campaign_created",
    )

    return db_campaign


# ==========================================================
# UPDATE CAMPAIGN
# ==========================================================


@router.put("/{campaign_id}", response_model=CampaignResponse)
def update_campaign(
    campaign_id: int,
    update_data: CampaignUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    campaign = (
        db.query(Campaign)
        .filter(Campaign.id == campaign_id, Campaign.user_id == current_user.id)
        .first()
    )

    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    update_fields = update_data.dict(exclude_unset=True)

    if "start_date" in update_fields or "end_date" in update_fields:

        new_start = update_fields.get("start_date", campaign.start_date)
        new_end = update_fields.get("end_date", campaign.end_date)

        if new_start >= new_end:
            raise HTTPException(
                status_code=400, detail="Start date must be before end date"
            )

    if update_data.name and update_data.name != campaign.name:

        existing = (
            db.query(Campaign)
            .filter(
                Campaign.user_id == current_user.id,
                Campaign.name == update_data.name,
                Campaign.id != campaign_id,
            )
            .first()
        )

        if existing:
            raise HTTPException(
                status_code=400, detail="Campaign with this name already exists"
            )

    previous_status = campaign.status

    # --------------------------------------------------
    # Track marketing_team_id BEFORE it gets overwritten,
    # so we know if this update is a fresh assignment
    # --------------------------------------------------

    previous_marketing_team_id = campaign.marketing_team_id

    for key, value in update_fields.items():

        # CampaignStatus is an Enum — store its .value on the
        # plain string column
        if key == "status" and value is not None:
            setattr(campaign, key, value.value if hasattr(value, "value") else value)
        else:
            setattr(campaign, key, value)

    db.commit()
    db.refresh(campaign)

    NotificationService(db).create_notification(
        user_id=current_user.id,
        title="Campaign Updated",
        description=f'Your campaign "{campaign.name}" was updated.',
        category="campaigns",
        notification_type="campaign_updated",
    )

    if "status" in update_fields:
        _notify_status_change(db, current_user.id, campaign, previous_status)

    # --------------------------------------------------
    # Campaign Assigned — fires when marketing_team_id is
    # newly set (was empty/different, now has a value)
    # --------------------------------------------------

    if (
        "marketing_team_id" in update_fields
        and campaign.marketing_team_id is not None
        and campaign.marketing_team_id != previous_marketing_team_id
    ):

        NotificationService(db).create_notification(
            user_id=campaign.marketing_team_id,
            title="Campaign Assigned",
            description=f'You were assigned to campaign "{campaign.name}".',
            category="campaigns",
            notification_type="campaign_assigned",
        )

    return _build_campaign_response(db, campaign)


# ==========================================================
# UPDATE CAMPAIGN STATUS
# ==========================================================


@router.patch("/{campaign_id}/status", response_model=CampaignResponse)
def update_campaign_status(
    campaign_id: int,
    status_data: CampaignStatusUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    campaign = (
        db.query(Campaign)
        .filter(Campaign.id == campaign_id, Campaign.user_id == current_user.id)
        .first()
    )

    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    previous_status = campaign.status

    campaign.status = status_data.status.value

    db.commit()
    db.refresh(campaign)

    _notify_status_change(db, current_user.id, campaign, previous_status)

    return _build_campaign_response(db, campaign)


# ==========================================================
# DELETE CAMPAIGN
# ==========================================================


@router.delete("/{campaign_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_campaign(
    campaign_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    campaign = (
        db.query(Campaign)
        .filter(Campaign.id == campaign_id, Campaign.user_id == current_user.id)
        .first()
    )

    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    db.delete(campaign)
    db.commit()

    return None


# ==========================================================
# GET SINGLE CAMPAIGN
# ==========================================================


@router.get("/{campaign_id}", response_model=CampaignResponse)
def get_campaign(
    campaign_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    campaign = (
        db.query(Campaign)
        .filter(Campaign.id == campaign_id, Campaign.user_id == current_user.id)
        .first()
    )

    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    return _build_campaign_response(db, campaign)


# ==========================================================
# GET ALL CAMPAIGNS
# ==========================================================


@router.get("/", response_model=CampaignListResponse)
def get_campaigns(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    platform: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
):

    query = db.query(Campaign).filter(Campaign.user_id == current_user.id)

    if status:
        query = query.filter(Campaign.status == status)

    if platform:
        query = query.filter(Campaign.platform == platform)

    if search:

        term = f"%{search}%"

        query = query.filter(
            or_(Campaign.name.ilike(term), Campaign.description.ilike(term))
        )

    sort_column = getattr(Campaign, sort_by, Campaign.created_at)

    if sort_order == "asc":
        query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc(sort_column))

    total = query.count()

    campaigns = query.offset(skip).limit(limit).all()

    result = [_build_campaign_response(db, campaign) for campaign in campaigns]

    return CampaignListResponse(total=total, skip=skip, limit=limit, campaigns=result)


# ==========================================================
# CAMPAIGN ANALYTICS
# ==========================================================


@router.get("/{campaign_id}/analytics", response_model=CampaignAnalytics)
def get_campaign_analytics(
    campaign_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    days: int = Query(30, ge=1, le=365),
):

    campaign = (
        db.query(Campaign)
        .filter(Campaign.id == campaign_id, Campaign.user_id == current_user.id)
        .first()
    )

    if not campaign:

        raise HTTPException(status_code=404, detail="Campaign not found")

    start_date = datetime.now() - timedelta(days=days)

    posts = (
        db.query(ScheduledPost).filter(ScheduledPost.campaign_id == campaign_id).all()
    )

    analytics = (
        db.query(PostAnalytics).filter(PostAnalytics.campaign_id == campaign_id).all()
    )

    total_posts = len(posts)

    published_posts = len([p for p in posts if p.status == "published"])

    scheduled_posts = len([p for p in posts if p.status == "scheduled"])

    failed_posts = len([p for p in posts if p.status == "failed"])

    draft_posts = len([p for p in posts if p.status == "draft"])

    likes = sum(a.likes for a in analytics)

    shares = sum(a.shares for a in analytics)

    comments = sum(a.comments for a in analytics)

    views = sum(a.views for a in analytics)

    engagement = likes + shares + comments

    return CampaignAnalytics(
        campaign_id=campaign.id,
        campaign_name=campaign.name,
        platform=campaign.platform,
        start_date=campaign.start_date,
        end_date=campaign.end_date,
        status=campaign.status,
        total_posts=total_posts,
        published_posts=published_posts,
        scheduled_posts=scheduled_posts,
        failed_posts=failed_posts,
        draft_posts=draft_posts,
        likes=likes,
        shares=shares,
        comments=comments,
        views=views,
        total_engagement=engagement,
        engagement_rate=(engagement / views * 100 if views > 0 else 0),
        daily_performance=[],
        platform_breakdown=[
            {
                "platform": campaign.platform,
                "total_posts": total_posts,
                "published_posts": published_posts,
            }
        ],
        period_days=days,
    )


# ==========================================================
# GET POSTS UNDER CAMPAIGN
# ==========================================================


@router.get("/{campaign_id}/posts")
def get_campaign_posts(
    campaign_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    status: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
):

    campaign = (
        db.query(Campaign)
        .filter(Campaign.id == campaign_id, Campaign.user_id == current_user.id)
        .first()
    )

    if not campaign:

        raise HTTPException(status_code=404, detail="Campaign not found")

    query = db.query(ScheduledPost).filter(ScheduledPost.campaign_id == campaign_id)

    if status:

        query = query.filter(ScheduledPost.status == status)

    total = query.count()

    posts = query.offset(skip).limit(limit).all()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "posts": [
            {
                "id": post.id,
                "title": post.title,
                "platform": post.platform,
                "status": post.status,
                "scheduled_time": post.scheduled_time,
                "published_at": post.published_at,
                "created_at": post.created_at,
            }
            for post in posts
        ],
    }


# ==========================================================
# ALL CAMPAIGN ANALYTICS OVERVIEW
# ==========================================================


@router.get("/analytics/overview")
def get_all_campaigns_analytics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    days: int = Query(30),
):

    campaigns = db.query(Campaign).filter(Campaign.user_id == current_user.id).all()

    result = []

    for campaign in campaigns:

        posts = (
            db.query(ScheduledPost)
            .filter(ScheduledPost.campaign_id == campaign.id)
            .count()
        )

        analytics = (
            db.query(PostAnalytics)
            .filter(PostAnalytics.campaign_id == campaign.id)
            .all()
        )

        likes = sum(a.likes for a in analytics)

        shares = sum(a.shares for a in analytics)

        comments = sum(a.comments for a in analytics)

        views = sum(a.views for a in analytics)

        result.append(
            {
                "campaign_id": campaign.id,
                "campaign_name": campaign.name,
                "platform": campaign.platform,
                "status": campaign.status,
                "total_posts": posts,
                "likes": likes,
                "shares": shares,
                "comments": comments,
                "views": views,
                "engagement": likes + shares + comments,
            }
        )

    return {
        "total_campaigns": len(result),
        "active_campaigns": len([c for c in result if c["status"] == "active"]),
        "campaigns": result,
        "period_days": days,
    }


# ==========================================================
# CAMPAIGN PERFORMANCE STATS
# ==========================================================


@router.get("/stats/performance", response_model=CampaignPerformanceMetrics)
def get_campaign_performance_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    days: int = Query(30),
):

    campaigns = db.query(Campaign).filter(Campaign.user_id == current_user.id).all()

    total_likes = 0

    total_shares = 0

    total_comments = 0

    total_views = 0

    best_campaign = None

    highest_engagement = 0

    for campaign in campaigns:

        analytics = (
            db.query(PostAnalytics)
            .filter(PostAnalytics.campaign_id == campaign.id)
            .all()
        )

        likes = sum(a.likes for a in analytics)

        shares = sum(a.shares for a in analytics)

        comments = sum(a.comments for a in analytics)

        views = sum(a.views for a in analytics)

        engagement = likes + shares + comments

        total_likes += likes

        total_shares += shares

        total_comments += comments

        total_views += views

        if engagement > highest_engagement:

            highest_engagement = engagement

            best_campaign = {
                "campaign_id": campaign.id,
                "name": campaign.name,
                "engagement": engagement,
            }

    return CampaignPerformanceMetrics(
        total_campaigns=len(campaigns),
        active_campaigns=len([c for c in campaigns if c.status == "active"]),
        completed_campaigns=len([c for c in campaigns if c.status == "completed"]),
        paused_campaigns=len([c for c in campaigns if c.status == "paused"]),
        cancelled_campaigns=len([c for c in campaigns if c.status == "cancelled"]),
        total_likes=total_likes,
        total_shares=total_shares,
        total_comments=total_comments,
        total_views=total_views,
        total_engagement=total_likes + total_shares + total_comments,
        average_engagement_per_campaign=(
            (total_likes + total_shares + total_comments) / len(campaigns)
            if campaigns
            else 0
        ),
        best_performing_campaign=best_campaign,
        period_days=days,
    )
