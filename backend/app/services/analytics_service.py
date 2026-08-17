# app/services/analytics_service.py
#
# Real queries to replace the placeholder-zero responses in
# app/api/analytics.py. Written against your actual models:
#   - ScheduledPost (status, approval_status, published_at, platform)
#   - PostAnalytics (likes, shares, comments, views, reach, impressions,
#     clicks, saves — keyed by post_id/user_id/campaign_id/platform)
#   - AudienceAnalytics (total_followers, new_followers, lost_followers,
#     net_growth — keyed by user_id/social_account_id/platform)
#   - Campaign (unchanged from your file)
#
# Drop these functions into a new app/services/analytics_service.py and
# call them from your existing endpoint handlers in app/api/analytics.py.

from datetime import datetime, timedelta
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.scheduled_post import ScheduledPost
from app.models.analytics import PostAnalytics, AudienceAnalytics


def get_analytics_overview(db: Session, user_id: int, days: int = 30) -> dict:
    """Backs GET /api/analytics/overview. Matches the response shape you
    already showed in Swagger (total_posts, published_posts, etc.)."""

    since = datetime.utcnow() - timedelta(days=days)

    # Post counts grouped by status
    status_rows = (
        db.query(ScheduledPost.status, func.count(ScheduledPost.id))
        .filter(
            ScheduledPost.user_id == user_id,
            ScheduledPost.is_deleted == False,  # noqa: E712
            ScheduledPost.created_at >= since,
        )
        .group_by(ScheduledPost.status)
        .all()
    )
    counts = {status: count for status, count in status_rows}
    total_posts = sum(counts.values())

    # "pending" isn't a post status in your model — it lives on
    # approval_status instead, so count it separately
    pending_posts = (
        db.query(func.count(ScheduledPost.id))
        .filter(
            ScheduledPost.user_id == user_id,
            ScheduledPost.approval_status == "pending",
            ScheduledPost.is_deleted == False,  # noqa: E712
        )
        .scalar()
    ) or 0

    # Engagement sums from PostAnalytics
    metrics = (
        db.query(
            func.coalesce(func.sum(PostAnalytics.likes), 0),
            func.coalesce(func.sum(PostAnalytics.shares), 0),
            func.coalesce(func.sum(PostAnalytics.comments), 0),
            func.coalesce(func.sum(PostAnalytics.views), 0),
            func.coalesce(func.sum(PostAnalytics.reach), 0),
            func.coalesce(func.sum(PostAnalytics.impressions), 0),
            func.coalesce(func.sum(PostAnalytics.clicks), 0),
            func.coalesce(func.sum(PostAnalytics.saves), 0),
        )
        .filter(
            PostAnalytics.user_id == user_id,
            PostAnalytics.recorded_at >= since,
        )
        .first()
    )
    likes, shares, comments, views, reach, impressions, clicks, saves = metrics
    total_engagement = likes + shares + comments
    engagement_rate = (
        round((total_engagement / impressions) * 100, 2) if impressions else 0.0
    )

    return {
        "total_posts": total_posts,
        "published_posts": counts.get("published", 0),
        "scheduled_posts": counts.get("scheduled", 0),
        "draft_posts": counts.get("draft", 0),
        "failed_posts": counts.get("failed", 0),
        "cancelled_posts": counts.get("cancelled", 0),
        "pending_posts": pending_posts,
        "total_engagement": total_engagement,
        "total_likes": likes,
        "total_shares": shares,
        "total_comments": comments,
        "total_views": views,
        "total_reach": reach,
        "total_impressions": impressions,
        "total_clicks": clicks,
        "total_saves": saves,
        "engagement_rate": engagement_rate,
    }


def get_top_performing_posts(
    db: Session, user_id: int, days: int = 30, limit: int = 5, lowest: bool = False
) -> list[dict]:
    """Backs the missing 'top/lowest performing posts' endpoint from the
    mentor brief. Set lowest=True to get worst performers instead."""

    since = datetime.utcnow() - timedelta(days=days)
    engagement_total = (
        func.coalesce(func.sum(PostAnalytics.likes), 0)
        + func.coalesce(func.sum(PostAnalytics.shares), 0)
        + func.coalesce(func.sum(PostAnalytics.comments), 0)
    )

    query = (
        db.query(
            ScheduledPost.id,
            ScheduledPost.title,
            ScheduledPost.platform,
            ScheduledPost.published_at,
            func.coalesce(func.sum(PostAnalytics.likes), 0).label("likes"),
            func.coalesce(func.sum(PostAnalytics.shares), 0).label("shares"),
            func.coalesce(func.sum(PostAnalytics.comments), 0).label("comments"),
            engagement_total.label("total_engagement"),
        )
        .join(PostAnalytics, PostAnalytics.post_id == ScheduledPost.id)
        .filter(
            ScheduledPost.user_id == user_id,
            ScheduledPost.status == "published",
            ScheduledPost.published_at.isnot(None),
            ScheduledPost.published_at >= since,
        )
        .group_by(ScheduledPost.id)
    )

    query = query.order_by(
        engagement_total.asc() if lowest else engagement_total.desc()
    )

    return [
        {
            "post_id": r.id,
            "title": r.title,
            "platform": r.platform,
            "published_at": r.published_at,
            "likes": r.likes,
            "shares": r.shares,
            "comments": r.comments,
            "total_engagement": r.total_engagement,
        }
        for r in query.limit(limit).all()
    ]


def get_platform_comparison(db: Session, user_id: int, days: int = 30) -> list[dict]:
    """Backs the Platform Comparison Dashboard. Aggregates PostAnalytics
    by platform — no separate PlatformAnalytics population step needed
    for this one since it's derived straight from post-level data."""

    since = datetime.utcnow() - timedelta(days=days)

    rows = (
        db.query(
            PostAnalytics.platform,
            func.coalesce(func.sum(PostAnalytics.likes), 0).label("likes"),
            func.coalesce(func.sum(PostAnalytics.shares), 0).label("shares"),
            func.coalesce(func.sum(PostAnalytics.comments), 0).label("comments"),
            func.coalesce(func.sum(PostAnalytics.reach), 0).label("reach"),
            func.coalesce(func.sum(PostAnalytics.impressions), 0).label("impressions"),
            func.coalesce(func.sum(PostAnalytics.clicks), 0).label("clicks"),
        )
        .filter(
            PostAnalytics.user_id == user_id,
            PostAnalytics.recorded_at >= since,
        )
        .group_by(PostAnalytics.platform)
        .all()
    )

    return [
        {
            "platform": r.platform,
            "likes": r.likes,
            "shares": r.shares,
            "comments": r.comments,
            "reach": r.reach,
            "impressions": r.impressions,
            "clicks": r.clicks,
            "engagement": r.likes + r.shares + r.comments,
        }
        for r in rows
    ]


def get_follower_growth(db: Session, user_id: int, days: int = 30) -> list[dict]:
    """Backs the Followers Growth chart. Returns a time series from
    AudienceAnalytics snapshots.

    IMPORTANT: this table only has data if something is actually writing
    snapshot rows over time (e.g. a daily job pulling follower counts
    from each connected platform's API and inserting a new
    AudienceAnalytics row). If nothing populates this table yet, this
    endpoint will correctly return an empty list rather than fake data —
    that's a separate task (a scheduled job, likely alongside your
    Module 5 publishing worker) before this chart has anything to show.
    """

    since = datetime.utcnow() - timedelta(days=days)

    rows = (
        db.query(AudienceAnalytics)
        .filter(
            AudienceAnalytics.user_id == user_id,
            AudienceAnalytics.recorded_at >= since,
        )
        .order_by(AudienceAnalytics.recorded_at.asc())
        .all()
    )

    return [
        {
            "platform": r.platform,
            "date": r.recorded_at,
            "total_followers": r.total_followers,
            "new_followers": r.new_followers,
            "lost_followers": r.lost_followers,
            "net_growth": r.net_growth,
        }
        for r in rows
    ]
