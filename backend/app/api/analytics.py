# app/api/analytics.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, and_, desc, asc
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from decimal import Decimal

import random

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.scheduled_post import ScheduledPost
from app.models.campaign import Campaign
from app.models.social_account import SocialAccount
from app.models.analytics import PostAnalytics
from app.models.business_assignment import BusinessAssignment
from app.schemas.analytics import (
    AnalyticsOverview,
    AudienceAnalytics,
    PlatformAnalytics,
    PostPerformanceMetrics,
    PostAnalyticsResponse,
    PostAnalyticsCreate,
    CampaignAnalyticsResponse,
    AnalyticsSummary,
    EngagementTrend,
)

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


# ==========================================================
# Helper — resolve the effective business-user scope
# ==========================================================


def _resolve_business_scope(
    db: Session,
    current_user: User,
    business_owner_id: int | None,
) -> int:
    if current_user.role in {"business_user", "content_creator"}:
        return current_user.id

    if current_user.role == "administrator":
        if business_owner_id is None:
            raise HTTPException(
                status_code=400,
                detail="business_owner_id is required for administrator access",
            )
        return business_owner_id

    if current_user.role == "marketing_team":
        if business_owner_id is None:
            raise HTTPException(
                status_code=400,
                detail="business_owner_id is required for marketing team access",
            )
        assignment = (
            db.query(BusinessAssignment)
            .filter(
                BusinessAssignment.marketing_team_id == current_user.id,
                BusinessAssignment.business_user_id == business_owner_id,
            )
            .first()
        )
        if not assignment:
            raise HTTPException(
                status_code=403,
                detail="You are not assigned to this business user",
            )
        return business_owner_id

    raise HTTPException(
        status_code=403,
        detail="You do not have permission to access analytics",
    )


@router.get("/overview", response_model=AnalyticsOverview)
def get_analytics_overview(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    days: Optional[int] = Query(
        30, ge=1, le=365, description="Number of days to analyze"
    ),
    business_owner_id: Optional[int] = Query(None, description="Business user id (marketing team / admin)"),
):
    scope_user_id = _resolve_business_scope(db, current_user, business_owner_id)
    """
    Get real analytics overview for the current user.

    Uses:
    - ScheduledPost for post/status counts
    - Latest PostAnalytics snapshot for each post
    """

    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    # ==========================================================
    # 1. GET POSTS FOR THE SELECTED PERIOD
    # ==========================================================

    posts = (
        db.query(ScheduledPost)
        .filter(
            ScheduledPost.user_id == scope_user_id,
            ScheduledPost.created_at >= start_date,
            ScheduledPost.created_at <= end_date,
        )
        .all()
    )

    # ==========================================================
    # 2. POST STATUS COUNTS
    # ==========================================================

    total_posts = len(posts)

    published_posts = sum(1 for post in posts if post.status == "published")

    scheduled_posts = sum(1 for post in posts if post.status == "scheduled")

    failed_posts = sum(1 for post in posts if post.status == "failed")

    draft_posts = sum(1 for post in posts if post.status == "draft")

    pending_posts = sum(1 for post in posts if post.status == "pending_approval")

    # ==========================================================
    # 3. GET LATEST ANALYTICS SNAPSHOT FOR EACH POST
    # ==========================================================

    post_ids = [post.id for post in posts]

    latest_analytics = []

    if post_ids:
        analytics_records = (
            db.query(PostAnalytics)
            .filter(
                PostAnalytics.user_id == scope_user_id,
                PostAnalytics.post_id.in_(post_ids),
                PostAnalytics.recorded_at >= start_date,
                PostAnalytics.recorded_at <= end_date,
            )
            .order_by(PostAnalytics.post_id, desc(PostAnalytics.recorded_at))
            .all()
        )

        # Keep only the newest snapshot for each post
        seen_posts = set()

        for record in analytics_records:
            if record.post_id not in seen_posts:
                latest_analytics.append(record)
                seen_posts.add(record.post_id)

    # ==========================================================
    # 4. AGGREGATE REAL ANALYTICS
    # ==========================================================

    total_likes = sum(record.likes or 0 for record in latest_analytics)

    total_shares = sum(record.shares or 0 for record in latest_analytics)

    total_comments = sum(record.comments or 0 for record in latest_analytics)

    total_views = sum(record.views or 0 for record in latest_analytics)

    total_reach = sum(record.reach or 0 for record in latest_analytics)

    total_impressions = sum(record.impressions or 0 for record in latest_analytics)

    total_engagement = total_likes + total_shares + total_comments

    # ==========================================================
    # 5. ENGAGEMENT RATE
    # ==========================================================

    engagement_rate = (total_engagement / total_views) * 100 if total_views > 0 else 0

    # Average based on posts that actually have analytics
    analytics_post_count = len(latest_analytics)

    average_engagement_per_post = (
        total_engagement / analytics_post_count if analytics_post_count > 0 else 0
    )

    # ==========================================================
    # 6. PLATFORM BREAKDOWN
    # ==========================================================

    platform_stats = {}

    for post in posts:
        # Normalize casing — a data inconsistency in ScheduledPost.platform
        # (e.g. "Youtube" vs "youtube" on different rows) was splitting the
        # same platform into two separate breakdown entries. Grouping by
        # lowercase key fixes the count without needing to touch the
        # underlying stored value on each row.
        platform_key = (post.platform or "unknown").lower()

        if platform_key not in platform_stats:
            platform_stats[platform_key] = 0

        if post.status == "published":
            platform_stats[platform_key] += 1

    # ==========================================================
    # 7. RETURN EXISTING RESPONSE SHAPE
    # ==========================================================

    return AnalyticsOverview(
        total_posts=total_posts,
        published_posts=published_posts,
        scheduled_posts=scheduled_posts,
        draft_posts=draft_posts,
        failed_posts=failed_posts,
        pending_posts=pending_posts,
        total_engagement=total_engagement,
        total_likes=total_likes,
        total_shares=total_shares,
        total_comments=total_comments,
        total_views=total_views,
        average_engagement_per_post=average_engagement_per_post,
        engagement_rate=engagement_rate,
        # IMPORTANT:
        # Use actual reach instead of views.
        total_reach=total_reach,
        total_impressions=total_impressions,
        period_days=days,
        platform_breakdown=platform_stats,
    )


@router.get("/audience", response_model=AudienceAnalytics)
def get_audience_analytics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    days: Optional[int] = Query(30, ge=1, le=365),
):
    """
    Get audience analytics data
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    posts = (
        db.query(ScheduledPost)
        .filter(
            ScheduledPost.user_id == current_user.id,
            ScheduledPost.published_at >= start_date,
            ScheduledPost.published_at <= end_date,
            ScheduledPost.status == "published",
        )
        .all()
    )

    post_ids = [p.id for p in posts]
    analytics = (
        db.query(PostAnalytics)
        .filter(
            PostAnalytics.post_id.in_(post_ids) if post_ids else False,
            PostAnalytics.recorded_at >= start_date,
        )
        .all()
    )

    total_likes = sum([a.likes for a in analytics])
    total_shares = sum([a.shares for a in analytics])
    total_comments = sum([a.comments for a in analytics])
    total_views = sum([a.views for a in analytics])
    total_engagement = total_likes + total_shares + total_comments

    # NOTE: demographics/geographic_distribution below are still
    # simulated placeholder values — no per-platform demographic data
    # source exists to mock those against. total_followers and
    # follower_growth now anchor to SocialAccount.followers_count
    # (populated via seed-mock-account-stats) instead of an unrelated
    # made-up formula, so this endpoint and the Reports module show
    # consistent follower numbers for the same user.
    total_followers = (
        db.query(func.sum(SocialAccount.followers_count))
        .filter(
            SocialAccount.user_id == current_user.id,
            SocialAccount.is_active == True,
        )
        .scalar()
        or 0
    )

    follower_growth = []
    for i in range(days):
        date = start_date + timedelta(days=i)
        # Backfill a plausible growth curve ending at the real
        # (mocked) current total, rather than a fixed base/rate that
        # has no relationship to the actual follower count.
        progress = (i + 1) / days
        followers_on_date = int(total_followers * progress)
        follower_growth.append(
            {
                "date": date.strftime("%Y-%m-%d"),
                "followers": followers_on_date,
                "new_followers": (
                    followers_on_date - follower_growth[-1]["followers"]
                    if follower_growth
                    else 0
                ),
            }
        )

    return AudienceAnalytics(
        total_followers=total_followers,
        follower_growth=follower_growth,
        demographics={
            "age_18_24": 30,
            "age_25_34": 45,
            "age_35_44": 20,
            "age_45_plus": 5,
            "age_unknown": 0,
        },
        geographic_distribution={"US": 40, "UK": 20, "India": 25, "Other": 15},
        total_likes=total_likes,
        total_shares=total_shares,
        total_comments=total_comments,
        total_views=total_views,
        total_engagement=total_engagement,
        engagement_rate=(
            (total_engagement / total_views * 100) if total_views > 0 else 0
        ),
        period_days=days,
        total_posts=len(posts),
    )


@router.get("/platforms", response_model=List[PlatformAnalytics])
def get_platform_analytics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    days: Optional[int] = Query(30, ge=1, le=365),
):
    """
    Get analytics breakdown by platform
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    posts = (
        db.query(ScheduledPost)
        .filter(
            ScheduledPost.user_id == current_user.id,
            ScheduledPost.created_at >= start_date,
        )
        .all()
    )

    platforms_dict = {}
    for post in posts:
        # Same normalization as get_analytics_overview above — group by
        # lowercase platform so casing inconsistencies in stored data
        # don't split one platform into two entries.
        platform_key = (post.platform or "unknown").lower()

        if platform_key not in platforms_dict:
            platforms_dict[platform_key] = {
                "platform": platform_key,
                "total_posts": 0,
                "published_posts": 0,
                "scheduled_posts": 0,
                "failed_posts": 0,
                "draft_posts": 0,
                "post_ids": [],
            }

        platforms_dict[platform_key]["total_posts"] += 1
        if post.status == "published":
            platforms_dict[platform_key]["published_posts"] += 1
        elif post.status == "scheduled":
            platforms_dict[platform_key]["scheduled_posts"] += 1
        elif post.status == "failed":
            platforms_dict[platform_key]["failed_posts"] += 1
        elif post.status == "draft":
            platforms_dict[platform_key]["draft_posts"] += 1

        platforms_dict[platform_key]["post_ids"].append(post.id)

    results = []
    for platform, data in platforms_dict.items():
        if data["post_ids"]:
            analytics = (
                db.query(PostAnalytics)
                .filter(
                    PostAnalytics.post_id.in_(data["post_ids"]),
                    PostAnalytics.recorded_at >= start_date,
                )
                .all()
            )

            likes = sum([a.likes for a in analytics])
            shares = sum([a.shares for a in analytics])
            comments = sum([a.comments for a in analytics])
            views = sum([a.views for a in analytics])
            reach = sum([a.reach or 0 for a in analytics])
            impressions = sum([a.impressions or 0 for a in analytics])
            clicks = sum([a.clicks or 0 for a in analytics])
            total_engagement = likes + shares + comments

            latest_analytics = (
                db.query(PostAnalytics)
                .filter(PostAnalytics.post_id.in_(data["post_ids"]))
                .order_by(desc(PostAnalytics.recorded_at))
                .first()
            )
        else:
            likes = shares = comments = views = reach = impressions = clicks = total_engagement = 0
            latest_analytics = None

        followers = (
            db.query(func.coalesce(func.sum(SocialAccount.followers_count), 0))
            .filter(
                SocialAccount.user_id == current_user.id,
                SocialAccount.platform.ilike(platform),
                SocialAccount.is_active == True,
            )
            .scalar()
            or 0
        )

        results.append(
            PlatformAnalytics(
                platform=platform,
                total_posts=data["total_posts"],
                published_posts=data["published_posts"],
                scheduled_posts=data["scheduled_posts"],
                failed_posts=data["failed_posts"],
                draft_posts=data["draft_posts"],
                likes=likes,
                shares=shares,
                comments=comments,
                views=views,
                reach=reach,
                impressions=impressions,
                clicks=clicks,
                followers=followers,
                engagement=total_engagement,
                total_engagement=total_engagement,
                average_engagement=(
                    total_engagement / data["published_posts"]
                    if data["published_posts"] > 0
                    else 0
                ),
                engagement_rate=(total_engagement / views * 100) if views > 0 else 0,
            )
        )

    return results


@router.get("/posts", response_model=List[PostPerformanceMetrics])
def get_post_performance(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    platform: Optional[str] = Query(None, description="Filter by platform"),
    status: Optional[str] = Query(None, description="Filter by status"),
    days: Optional[int] = Query(30, ge=1, le=365),
    limit: Optional[int] = Query(50, ge=1, le=100),
    sort_by: Optional[str] = Query(
        "published_at", description="Sort by: published_at, engagement, likes, views"
    ),
    order: Optional[str] = Query("desc", description="Sort order: asc or desc"),
):
    """
    Get performance metrics for individual posts
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    query = db.query(ScheduledPost).filter(
        ScheduledPost.user_id == current_user.id, ScheduledPost.created_at >= start_date
    )

    if platform:
        query = query.filter(ScheduledPost.platform == platform)

    if status:
        query = query.filter(ScheduledPost.status == status)

    sort_column = getattr(ScheduledPost, sort_by, ScheduledPost.published_at)
    if order == "asc":
        query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc(sort_column))

    posts = query.limit(limit).all()

    results = []
    for post in posts:
        analytics = (
            db.query(PostAnalytics)
            .filter(PostAnalytics.post_id == post.id)
            .order_by(desc(PostAnalytics.recorded_at))
            .first()
        )

        if analytics:
            engagement = analytics.likes + analytics.shares + analytics.comments
            engagement_rate = (
                (engagement / analytics.views * 100) if analytics.views > 0 else 0
            )
        else:
            engagement = 0
            engagement_rate = 0
            analytics = None

        results.append(
            PostPerformanceMetrics(
                post_id=post.id,
                title=post.title,
                caption=post.caption,
                platform=post.platform,
                scheduled_time=post.scheduled_time,
                published_at=post.published_at,
                likes=analytics.likes if analytics else 0,
                shares=analytics.shares if analytics else 0,
                comments=analytics.comments if analytics else 0,
                views=analytics.views if analytics else 0,
                reach=(analytics.reach or 0) if analytics else 0,
                impressions=(analytics.impressions or 0) if analytics else 0,
                clicks=(analytics.clicks or 0) if analytics else 0,
                saves=(analytics.saves or 0) if analytics else 0,
                total_engagement=engagement,
                engagement_rate=engagement_rate,
                status=post.status,
                created_at=post.created_at,
            )
        )

    return results


# =================================================
# TOP / LOWEST PERFORMING POSTS
# =================================================
#
# NOTE: these two routes MUST stay above
# GET /posts/{post_id} below. FastAPI matches routes
# top-to-bottom, so /posts/top would otherwise be
# swallowed by /posts/{post_id} and fail trying to
# parse "top" as an integer post_id.


@router.get("/posts/top", response_model=List[PostPerformanceMetrics])
def get_top_performing_posts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    days: Optional[int] = Query(30, ge=1, le=365),
    limit: Optional[int] = Query(5, ge=1, le=50),
):
    """
    Get the top-performing published posts by engagement
    (likes + shares + comments), using each post's latest
    analytics snapshot.
    """
    return _get_ranked_posts(current_user, db, days, limit, lowest=False)


@router.get("/posts/lowest", response_model=List[PostPerformanceMetrics])
def get_lowest_performing_posts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    days: Optional[int] = Query(30, ge=1, le=365),
    limit: Optional[int] = Query(5, ge=1, le=50),
):
    """Same as above, sorted ascending instead of descending."""
    return _get_ranked_posts(current_user, db, days, limit, lowest=True)


def _get_ranked_posts(
    current_user: User,
    db: Session,
    days: int,
    limit: int,
    lowest: bool,
) -> List[PostPerformanceMetrics]:
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    posts = (
        db.query(ScheduledPost)
        .filter(
            ScheduledPost.user_id == current_user.id,
            ScheduledPost.status == "published",
            ScheduledPost.published_at >= start_date,
            ScheduledPost.published_at <= end_date,
        )
        .all()
    )

    scored = []
    for post in posts:
        analytics = (
            db.query(PostAnalytics)
            .filter(PostAnalytics.post_id == post.id)
            .order_by(desc(PostAnalytics.recorded_at))
            .first()
        )
        if not analytics:
            # No analytics recorded for this post yet — skip it rather
            # than showing it as a fake zero-engagement "worst" post
            continue

        engagement = analytics.likes + analytics.shares + analytics.comments
        engagement_rate = (
            (engagement / analytics.views * 100) if analytics.views > 0 else 0
        )

        scored.append(
            (
                engagement,
                PostPerformanceMetrics(
                    post_id=post.id,
                    title=post.title,
                    caption=post.caption,
                    platform=post.platform,
                    scheduled_time=post.scheduled_time,
                    published_at=post.published_at,
                    likes=analytics.likes,
                    shares=analytics.shares,
                    comments=analytics.comments,
                    views=analytics.views,
                    reach=analytics.reach or 0,
                    impressions=analytics.impressions or 0,
                    clicks=analytics.clicks or 0,
                    saves=analytics.saves or 0,
                    total_engagement=engagement,
                    engagement_rate=engagement_rate,
                    status=post.status,
                    created_at=post.created_at,
                ),
            )
        )

    scored.sort(key=lambda x: x[0], reverse=not lowest)
    return [p for _, p in scored[:limit]]


# =================================================
# RECORD POST ANALYTICS (manual insert — unchanged)
# =================================================


@router.post("/posts/{post_id}/record", response_model=PostAnalyticsResponse)
def record_post_analytics(
    post_id: int,
    data: PostAnalyticsCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Record a new analytics snapshot for a post.

    Called after syncing metrics from a platform API
    (e.g. Facebook Page Insights, Instagram Insights,
    LinkedIn Analytics, Pinterest Pin Analytics).

    Inserts a new row rather than updating an existing one,
    so /posts/{post_id} can show engagement_over_time as a
    history of snapshots.
    """

    post = (
        db.query(ScheduledPost)
        .filter(
            ScheduledPost.id == post_id,
            ScheduledPost.user_id == current_user.id,
        )
        .first()
    )

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    record = PostAnalytics(
        post_id=post_id,
        campaign_id=post.campaign_id,
        user_id=current_user.id,
        platform=data.platform,
        likes=data.likes,
        shares=data.shares,
        comments=data.comments,
        views=data.views,
        reach=data.reach,
        impressions=data.impressions,
        clicks=data.clicks,
        saves=data.saves,
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


# =================================================
# MOCK ANALYTICS DATA (per your decision — real API
# calls to Instagram/YouTube have been removed here.
# Test accounts have no real audience, so real numbers
# were all zero/empty anyway. This generates plausible-
# looking fake engagement instead, for demo purposes.)
# =================================================


def _generate_mock_analytics(platform: str) -> dict:
    """
    Generates randomized but internally-consistent fake engagement
    numbers (comments/shares/saves scaled off likes, likes scaled off
    reach, etc.) so the numbers look plausible together rather than
    being independently random. Not based on any real data source —
    purely for demo purposes.
    """

    reach = random.randint(50, 500)
    impressions = int(reach * random.uniform(1.1, 2.0))
    views = int(reach * random.uniform(0.8, 1.2))
    likes = int(reach * random.uniform(0.02, 0.10))
    comments = int(likes * random.uniform(0.05, 0.25))
    shares = int(likes * random.uniform(0.02, 0.15))
    saves = int(likes * random.uniform(0.05, 0.3))
    clicks = int(impressions * random.uniform(0.01, 0.06))

    return {
        "likes": likes,
        "shares": shares,
        "comments": comments,
        "views": views,
        "reach": reach,
        "impressions": impressions,
        "clicks": clicks,
        "saves": saves,
    }


@router.post("/posts/{post_id}/sync", response_model=PostAnalyticsResponse)
def sync_post_analytics(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Generate a mock analytics snapshot for a post and record it.
    Real platform API calls were removed here per your decision —
    test accounts have no real audience, so real numbers were
    consistently zero. Works for any platform, not just Instagram.
    """

    post = (
        db.query(ScheduledPost)
        .filter(ScheduledPost.id == post_id, ScheduledPost.user_id == current_user.id)
        .first()
    )

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.status != "published":
        raise HTTPException(
            status_code=400,
            detail=f"Post must be published to sync analytics (current status: {post.status})",
        )

    metrics = _generate_mock_analytics(post.platform)

    record = PostAnalytics(
        post_id=post.id,
        campaign_id=post.campaign_id,
        user_id=current_user.id,
        platform=(post.platform or "unknown").lower(),
        likes=metrics["likes"],
        shares=metrics["shares"],
        comments=metrics["comments"],
        views=metrics["views"],
        reach=metrics["reach"],
        impressions=metrics["impressions"],
        clicks=metrics["clicks"],
        saves=metrics["saves"],
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


@router.post("/seed-mock-data")
def seed_mock_analytics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    only_missing: bool = Query(
        True, description="Only seed posts that have no analytics rows yet"
    ),
):
    """
    Backfills a mock PostAnalytics snapshot for every published post
    belonging to the current user. Skips posts that already have at
    least one analytics row unless only_missing=false is passed.
    """

    posts = (
        db.query(ScheduledPost)
        .filter(
            ScheduledPost.user_id == current_user.id,
            ScheduledPost.status == "published",
        )
        .all()
    )

    seeded_post_ids = []
    skipped_post_ids = []

    for post in posts:

        if only_missing:
            existing = (
                db.query(PostAnalytics).filter(PostAnalytics.post_id == post.id).first()
            )
            if existing:
                skipped_post_ids.append(post.id)
                continue

        metrics = _generate_mock_analytics(post.platform)

        record = PostAnalytics(
            post_id=post.id,
            campaign_id=post.campaign_id,
            user_id=current_user.id,
            platform=(post.platform or "unknown").lower(),
            likes=metrics["likes"],
            shares=metrics["shares"],
            comments=metrics["comments"],
            views=metrics["views"],
            reach=metrics["reach"],
            impressions=metrics["impressions"],
            clicks=metrics["clicks"],
            saves=metrics["saves"],
        )

        db.add(record)
        seeded_post_ids.append(post.id)

    db.commit()

    return {
        "seeded_post_ids": seeded_post_ids,
        "skipped_post_ids": skipped_post_ids,
        "total_seeded": len(seeded_post_ids),
        "total_skipped": len(skipped_post_ids),
    }


# =================================================
# MOCK ACCOUNT-LEVEL STATS (followers/following/posts)
# =================================================
#
# SocialAccount.followers_count / following_count /
# total_posts are real DB columns but nothing populates
# them yet — they sit at 0. Reports' Audience Growth and
# Platform Comparison builders both read these directly,
# so without this they'd show 0 followers regardless of
# the PostAnalytics mock data above.


def _generate_mock_account_stats() -> dict:
    """
    Plausible fake follower/following/post counts. Not based on any
    real data source — for demo purposes only.
    """

    followers = random.randint(50, 500)
    following = random.randint(10, min(followers, 100))
    total_posts = random.randint(5, 50)

    return {
        "followers_count": followers,
        "following_count": following,
        "total_posts": total_posts,
    }


@router.post("/seed-mock-account-stats")
def seed_mock_account_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    only_missing: bool = Query(
        True, description="Only seed accounts currently at 0 followers"
    ),
):
    """
    Backfills mock followers_count/following_count/total_posts on
    every active SocialAccount for the current user.
    """

    accounts = (
        db.query(SocialAccount)
        .filter(
            SocialAccount.user_id == current_user.id,
            SocialAccount.is_active == True,
        )
        .all()
    )

    seeded_account_ids = []
    skipped_account_ids = []

    for account in accounts:

        if only_missing and (account.followers_count or 0) > 0:
            skipped_account_ids.append(account.id)
            continue

        stats = _generate_mock_account_stats()

        account.followers_count = stats["followers_count"]
        account.following_count = stats["following_count"]
        account.total_posts = stats["total_posts"]

        seeded_account_ids.append(account.id)

    db.commit()

    return {
        "seeded_account_ids": seeded_account_ids,
        "skipped_account_ids": skipped_account_ids,
        "total_seeded": len(seeded_account_ids),
        "total_skipped": len(skipped_account_ids),
    }


@router.get("/posts/{post_id}", response_model=PostAnalyticsResponse)
def get_post_analytics(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    days: Optional[int] = Query(30, ge=1, le=365),
):
    """
    Get detailed analytics for a specific post
    """
    post = (
        db.query(ScheduledPost)
        .filter(ScheduledPost.id == post_id, ScheduledPost.user_id == current_user.id)
        .first()
    )

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    analytics = (
        db.query(PostAnalytics)
        .filter(
            PostAnalytics.post_id == post_id, PostAnalytics.recorded_at >= start_date
        )
        .order_by(desc(PostAnalytics.recorded_at))
        .all()
    )

    if not analytics:
        return PostAnalyticsResponse(
            post_id=post_id,
            post_title=post.title,
            user_id=current_user.id,
            platform=post.platform,
            likes=0,
            shares=0,
            comments=0,
            views=0,
            total_engagement=0,
            engagement_rate=0,
            recorded_at=datetime.now(),
            engagement_over_time=[],
            period_days=days,
        )

    engagement_over_time = []
    for record in analytics:
        engagement = record.likes + record.shares + record.comments
        engagement_over_time.append(
            {
                "date": record.recorded_at.strftime("%Y-%m-%d"),
                "time": record.recorded_at.strftime("%H:%M"),
                "likes": record.likes,
                "shares": record.shares,
                "comments": record.comments,
                "views": record.views,
                "engagement": engagement,
            }
        )

    latest = analytics[0]
    total_engagement = latest.likes + latest.shares + latest.comments
    engagement_rate = (total_engagement / latest.views * 100) if latest.views > 0 else 0

    return PostAnalyticsResponse(
        post_id=post_id,
        post_title=post.title,
        user_id=current_user.id,
        platform=post.platform,
        likes=latest.likes,
        shares=latest.shares,
        comments=latest.comments,
        views=latest.views,
        total_engagement=total_engagement,
        engagement_rate=engagement_rate,
        recorded_at=latest.recorded_at,
        engagement_over_time=engagement_over_time,
        period_days=days,
        total_records=len(analytics),
    )


@router.get("/campaigns/{campaign_id}", response_model=CampaignAnalyticsResponse)
def get_campaign_analytics(
    campaign_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    days: Optional[int] = Query(30, ge=1, le=365),
):
    """
    Get analytics for a specific campaign
    """
    campaign = (
        db.query(Campaign)
        .filter(Campaign.id == campaign_id, Campaign.user_id == current_user.id)
        .first()
    )

    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    posts = (
        db.query(ScheduledPost)
        .filter(
            ScheduledPost.campaign_id == campaign_id,
            ScheduledPost.created_at >= start_date,
        )
        .all()
    )

    post_ids = [p.id for p in posts]
    analytics = (
        db.query(PostAnalytics)
        .filter(
            PostAnalytics.campaign_id == campaign_id,
            PostAnalytics.recorded_at >= start_date,
        )
        .all()
        if post_ids
        else []
    )

    total_posts = len(posts)
    published_posts = len([p for p in posts if p.status == "published"])
    scheduled_posts = len([p for p in posts if p.status == "scheduled"])
    failed_posts = len([p for p in posts if p.status == "failed"])
    draft_posts = len([p for p in posts if p.status == "draft"])

    likes = sum([a.likes for a in analytics])
    shares = sum([a.shares for a in analytics])
    comments = sum([a.comments for a in analytics])
    views = sum([a.views for a in analytics])
    total_engagement = likes + shares + comments

    engagement_rate = (total_engagement / views * 100) if views > 0 else 0

    post_performance = []
    for post in posts:
        post_analytics = (
            db.query(PostAnalytics)
            .filter(PostAnalytics.post_id == post.id)
            .order_by(desc(PostAnalytics.recorded_at))
            .first()
        )

        if post_analytics:
            post_performance.append(
                {
                    "post_id": post.id,
                    "title": post.title,
                    "likes": post_analytics.likes,
                    "shares": post_analytics.shares,
                    "comments": post_analytics.comments,
                    "views": post_analytics.views,
                    "engagement": post_analytics.likes
                    + post_analytics.shares
                    + post_analytics.comments,
                }
            )

    return CampaignAnalyticsResponse(
        campaign_id=campaign_id,
        campaign_name=campaign.name,
        platform=campaign.platform,
        description=campaign.description,
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
        total_engagement=total_engagement,
        engagement_rate=engagement_rate,
        post_performance=post_performance,
        period_days=days,
    )


@router.get("/summary", response_model=AnalyticsSummary)
def get_analytics_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    business_owner_id: Optional[int] = Query(None, description="Business user id (marketing team / admin)"),
):
    """
    Get quick summary of analytics for dashboard
    """
    scope_user_id = _resolve_business_scope(db, current_user, business_owner_id)

    total_posts = (
        db.query(ScheduledPost).filter(ScheduledPost.user_id == scope_user_id).count()
    )

    published_posts = (
        db.query(ScheduledPost)
        .filter(
            ScheduledPost.user_id == scope_user_id,
            ScheduledPost.status == "published",
        )
        .count()
    )

    scheduled_posts = (
        db.query(ScheduledPost)
        .filter(
            ScheduledPost.user_id == scope_user_id,
            ScheduledPost.status == "scheduled",
        )
        .count()
    )

    failed_posts = (
        db.query(ScheduledPost)
        .filter(
            ScheduledPost.user_id == scope_user_id, ScheduledPost.status == "failed"
        )
        .count()
    )

    today = datetime.now().date()
    today_posts = (
        db.query(ScheduledPost)
        .filter(
            ScheduledPost.user_id == scope_user_id,
            func.date(ScheduledPost.scheduled_time) == today,
        )
        .count()
    )

    analytics = (
        db.query(PostAnalytics).filter(PostAnalytics.user_id == scope_user_id).all()
    )

    total_engagement = sum([a.likes + a.shares + a.comments for a in analytics])

    recent_posts = (
        db.query(ScheduledPost)
        .filter(ScheduledPost.user_id == scope_user_id)
        .order_by(desc(ScheduledPost.created_at))
        .limit(5)
        .all()
    )

    recent_posts_data = []
    for post in recent_posts:
        recent_posts_data.append(
            {
                "id": post.id,
                "title": post.title,
                "platform": post.platform,
                "status": post.status,
                "scheduled_time": post.scheduled_time,
                "created_at": post.created_at,
            }
        )

    return AnalyticsSummary(
        total_posts=total_posts,
        published_posts=published_posts,
        scheduled_posts=scheduled_posts,
        failed_posts=failed_posts,
        today_posts=today_posts,
        total_engagement=total_engagement,
        active_campaigns=db.query(Campaign)
        .filter(Campaign.user_id == scope_user_id, Campaign.status == "active")
        .count(),
        connected_accounts=db.query(SocialAccount)
        .filter(
            SocialAccount.user_id == scope_user_id, SocialAccount.is_connected == True
        )
        .count(),
        recent_posts=recent_posts_data,
    )


@router.get("/engagement/trend", response_model=EngagementTrend)
def get_engagement_trend(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    days: Optional[int] = Query(30, ge=1, le=365),
):
    """
    Get engagement trend over time
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    results = (
        db.query(
            func.date(PostAnalytics.recorded_at).label("date"),
            func.sum(PostAnalytics.likes).label("likes"),
            func.sum(PostAnalytics.shares).label("shares"),
            func.sum(PostAnalytics.comments).label("comments"),
            func.sum(PostAnalytics.views).label("views"),
            func.sum(PostAnalytics.reach).label("reach"),
            func.sum(PostAnalytics.impressions).label("impressions"),
            func.sum(PostAnalytics.clicks).label("clicks"),
            func.count(PostAnalytics.id).label("count"),
        )
        .filter(
            PostAnalytics.user_id == current_user.id,
            PostAnalytics.recorded_at >= start_date,
        )
        .group_by(func.date(PostAnalytics.recorded_at))
        .order_by(asc(func.date(PostAnalytics.recorded_at)))
        .all()
    )

    trend_data = []
    for row in results:
        engagement = row.likes + row.shares + row.comments
        trend_data.append(
            {
                "date": row.date.strftime("%Y-%m-%d"),
                "likes": row.likes,
                "shares": row.shares,
                "comments": row.comments,
                "views": row.views,
                "reach": row.reach or 0,
                "impressions": row.impressions or 0,
                "clicks": row.clicks or 0,
                "engagement": engagement,
                "posts_count": row.count,
            }
        )

    if trend_data:
        avg_engagement = sum([d["engagement"] for d in trend_data]) / len(trend_data)
        avg_views = sum([d["views"] for d in trend_data]) / len(trend_data)
    else:
        avg_engagement = 0
        avg_views = 0

    return EngagementTrend(
        period_days=days,
        data=trend_data,
        average_daily_engagement=avg_engagement,
        average_daily_views=avg_views,
        total_engagement=sum([d["engagement"] for d in trend_data]),
        total_views=sum([d["views"] for d in trend_data]),
    )
