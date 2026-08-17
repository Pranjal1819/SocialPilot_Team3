# app/services/report_generation.py

from typing import Optional
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.scheduled_post import ScheduledPost
from app.models.analytics import (
    PostAnalytics,
    AudienceAnalytics,
    CampaignAnalyticsSnapshot,
    PlatformAnalytics,
)
from app.models.campaign import Campaign
from app.schemas.generated_report import ReportType


def generate_report_data(
    db: Session,
    user_id: int,
    report_type: ReportType,
    campaign_id: Optional[int] = None,
    platform: Optional[str] = None,
    content_type: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
):

    if report_type == ReportType.ENGAGEMENT:
        return _generate_engagement_report(
            db, user_id, campaign_id, platform, content_type, start_date, end_date
        )

    if report_type == ReportType.CAMPAIGN:
        return _generate_campaign_report(db, user_id, campaign_id, start_date, end_date)

    if report_type == ReportType.AUDIENCE_GROWTH:
        return _generate_audience_growth_report(db, user_id, platform, start_date, end_date)

    if report_type == ReportType.PUBLISHING:
        return _generate_publishing_report(
            db, user_id, campaign_id, platform, start_date, end_date
        )

    if report_type == ReportType.PLATFORM_COMPARISON:
        return _generate_platform_comparison_report(db, user_id, start_date, end_date)

    raise NotImplementedError(
        f"Report type '{report_type.value}' is not yet implemented"
    )


# ==========================================================
# ENGAGEMENT REPORT
# ==========================================================


def _generate_engagement_report(
    db: Session,
    user_id: int,
    campaign_id: Optional[int],
    platform: Optional[str],
    content_type: Optional[str],
    start_date: Optional[datetime],
    end_date: Optional[datetime],
):

    query = db.query(PostAnalytics).filter(PostAnalytics.user_id == user_id)

    if campaign_id:
        query = query.filter(PostAnalytics.campaign_id == campaign_id)

    if platform:
        query = query.filter(PostAnalytics.platform == platform)

    if start_date:
        query = query.filter(PostAnalytics.recorded_at >= start_date)

    if end_date:
        query = query.filter(PostAnalytics.recorded_at <= end_date)

    analytics_rows = query.all()

    if content_type:

        post_ids = [a.post_id for a in analytics_rows if a.post_id]

        matching_post_ids = set(
            p.id
            for p in db.query(ScheduledPost.id)
            .filter(
                ScheduledPost.id.in_(post_ids),
                ScheduledPost.content_type == content_type,
            )
            .all()
        )

        analytics_rows = [a for a in analytics_rows if a.post_id in matching_post_ids]

    total_likes = sum(a.likes or 0 for a in analytics_rows)
    total_shares = sum(a.shares or 0 for a in analytics_rows)
    total_comments = sum(a.comments or 0 for a in analytics_rows)
    total_saves = sum(a.saves or 0 for a in analytics_rows)
    total_clicks = sum(a.clicks or 0 for a in analytics_rows)
    total_impressions = sum(a.impressions or 0 for a in analytics_rows)
    total_reach = sum(a.reach or 0 for a in analytics_rows)
    total_views = sum(a.views or 0 for a in analytics_rows)

    total_engagement = total_likes + total_shares + total_comments + total_saves

    engagement_rate = (
        (total_engagement / total_impressions * 100) if total_impressions > 0 else 0
    )

    post_ids = list({a.post_id for a in analytics_rows if a.post_id})

    posts_by_id = {
        p.id: p
        for p in db.query(ScheduledPost).filter(ScheduledPost.id.in_(post_ids)).all()
    }

    post_engagement = {}

    for a in analytics_rows:

        if not a.post_id:
            continue

        engagement = (a.likes or 0) + (a.shares or 0) + (a.comments or 0) + (a.saves or 0)

        post_engagement[a.post_id] = post_engagement.get(a.post_id, 0) + engagement

    top_posts = sorted(post_engagement.items(), key=lambda x: x[1], reverse=True)[:10]

    top_posts_table = []

    for post_id, engagement in top_posts:

        post = posts_by_id.get(post_id)

        if not post:
            continue

        top_posts_table.append(
            {
                "post_id": post_id,
                "title": post.title,
                "platform": post.platform,
                "content_type": post.content_type,
                "published_at": (
                    post.published_at.isoformat() if post.published_at else None
                ),
                "engagement": engagement,
            }
        )

    return {
        "summary": {
            "total_posts_analyzed": len(post_ids),
            "total_likes": total_likes,
            "total_shares": total_shares,
            "total_comments": total_comments,
            "total_saves": total_saves,
            "total_clicks": total_clicks,
            "total_impressions": total_impressions,
            "total_reach": total_reach,
            "total_views": total_views,
            "total_engagement": total_engagement,
            "engagement_rate": round(engagement_rate, 2),
        },
        "tables": {
            "top_performing_posts": top_posts_table,
        },
    }


# ==========================================================
# CAMPAIGN REPORT
# ==========================================================


def _generate_campaign_report(
    db: Session,
    user_id: int,
    campaign_id: Optional[int],
    start_date: Optional[datetime],
    end_date: Optional[datetime],
):

    query = db.query(Campaign).filter(Campaign.user_id == user_id)

    if campaign_id:
        query = query.filter(Campaign.id == campaign_id)

    campaigns = query.all()

    campaign_rows = []

    total_posts_all = 0
    total_engagement_all = 0
    total_reach_all = 0
    total_impressions_all = 0

    for campaign in campaigns:

        snapshot_query = db.query(CampaignAnalyticsSnapshot).filter(
            CampaignAnalyticsSnapshot.campaign_id == campaign.id
        )

        if start_date:
            snapshot_query = snapshot_query.filter(
                CampaignAnalyticsSnapshot.recorded_at >= start_date
            )

        if end_date:
            snapshot_query = snapshot_query.filter(
                CampaignAnalyticsSnapshot.recorded_at <= end_date
            )

        snapshots = snapshot_query.all()

        total_posts = max((s.total_posts or 0 for s in snapshots), default=0)
        reach = sum(s.reach or 0 for s in snapshots)
        impressions = sum(s.impressions or 0 for s in snapshots)
        engagement = sum(s.engagement or 0 for s in snapshots)
        clicks = sum(s.clicks or 0 for s in snapshots)
        likes = sum(s.likes or 0 for s in snapshots)
        completion = max((s.completion_percentage or 0 for s in snapshots), default=0)

        total_posts_all += total_posts
        total_engagement_all += engagement
        total_reach_all += reach
        total_impressions_all += impressions

        campaign_rows.append(
            {
                "campaign_id": campaign.id,
                "campaign_name": campaign.name,
                "status": campaign.status,
                "start_date": campaign.start_date.isoformat() if campaign.start_date else None,
                "end_date": campaign.end_date.isoformat() if campaign.end_date else None,
                "total_posts": total_posts,
                "reach": reach,
                "impressions": impressions,
                "engagement": engagement,
                "clicks": clicks,
                "likes": likes,
                "completion_percentage": completion,
            }
        )

    return {
        "summary": {
            "total_campaigns": len(campaigns),
            "active_campaigns": len([c for c in campaigns if c.status == "active"]),
            "completed_campaigns": len([c for c in campaigns if c.status == "completed"]),
            "total_posts": total_posts_all,
            "total_reach": total_reach_all,
            "total_impressions": total_impressions_all,
            "total_engagement": total_engagement_all,
        },
        "tables": {
            "campaigns": campaign_rows,
        },
    }


# ==========================================================
# AUDIENCE GROWTH REPORT
# ==========================================================


def _generate_audience_growth_report(
    db: Session,
    user_id: int,
    platform: Optional[str],
    start_date: Optional[datetime],
    end_date: Optional[datetime],
):

    query = db.query(AudienceAnalytics).filter(AudienceAnalytics.user_id == user_id)

    if platform:
        query = query.filter(AudienceAnalytics.platform == platform)

    if start_date:
        query = query.filter(AudienceAnalytics.recorded_at >= start_date)

    if end_date:
        query = query.filter(AudienceAnalytics.recorded_at <= end_date)

    rows = query.order_by(AudienceAnalytics.recorded_at.asc()).all()

    total_new = sum(r.new_followers or 0 for r in rows)
    total_lost = sum(r.lost_followers or 0 for r in rows)
    net_growth = sum(r.net_growth or 0 for r in rows)

    latest_total_followers = rows[-1].total_followers if rows else 0

    growth_table = [
        {
            "recorded_at": r.recorded_at.isoformat() if r.recorded_at else None,
            "platform": r.platform,
            "total_followers": r.total_followers,
            "new_followers": r.new_followers,
            "lost_followers": r.lost_followers,
            "net_growth": r.net_growth,
        }
        for r in rows
    ]

    return {
        "summary": {
            "current_total_followers": latest_total_followers,
            "total_new_followers": total_new,
            "total_lost_followers": total_lost,
            "net_growth": net_growth,
        },
        "tables": {
            "growth_over_time": growth_table,
        },
    }


# ==========================================================
# PUBLISHING REPORT
# ==========================================================


def _generate_publishing_report(
    db: Session,
    user_id: int,
    campaign_id: Optional[int],
    platform: Optional[str],
    start_date: Optional[datetime],
    end_date: Optional[datetime],
):

    query = db.query(ScheduledPost).filter(
        ScheduledPost.user_id == user_id,
        ScheduledPost.is_deleted == False,
    )

    if campaign_id:
        query = query.filter(ScheduledPost.campaign_id == campaign_id)

    if platform:
        query = query.filter(ScheduledPost.platform == platform)

    if start_date:
        query = query.filter(ScheduledPost.created_at >= start_date)

    if end_date:
        query = query.filter(ScheduledPost.created_at <= end_date)

    posts = query.all()

    scheduled = len([p for p in posts if p.status == "scheduled"])
    published = len([p for p in posts if p.status == "published"])
    failed = len([p for p in posts if p.status == "failed"])
    cancelled = len([p for p in posts if p.status == "cancelled"])
    total_retries = sum(p.retry_count or 0 for p in posts)

    success_rate = (published / len(posts) * 100) if posts else 0

    failed_table = [
        {
            "post_id": p.id,
            "title": p.title,
            "platform": p.platform,
            "failure_reason": p.failure_reason,
            "retry_count": p.retry_count,
            "created_at": p.created_at.isoformat() if p.created_at else None,
        }
        for p in posts
        if p.status == "failed"
    ]

    return {
        "summary": {
            "total_posts": len(posts),
            "scheduled_posts": scheduled,
            "published_posts": published,
            "failed_posts": failed,
            "cancelled_posts": cancelled,
            "success_rate": round(success_rate, 2),
            "total_retry_attempts": total_retries,
        },
        "tables": {
            "failed_posts": failed_table,
        },
    }


# ==========================================================
# PLATFORM COMPARISON REPORT
# ==========================================================


def _generate_platform_comparison_report(
    db: Session,
    user_id: int,
    start_date: Optional[datetime],
    end_date: Optional[datetime],
):

    query = db.query(PlatformAnalytics).filter(PlatformAnalytics.user_id == user_id)

    if start_date:
        query = query.filter(PlatformAnalytics.recorded_at >= start_date)

    if end_date:
        query = query.filter(PlatformAnalytics.recorded_at <= end_date)

    rows = query.all()

    by_platform = {}

    for r in rows:

        p = by_platform.setdefault(
            r.platform_name,
            {
                "platform": r.platform_name,
                "followers": 0,
                "reach": 0,
                "engagement": 0,
                "impressions": 0,
                "clicks": 0,
            },
        )

        p["followers"] += r.followers or 0
        p["reach"] += r.reach or 0
        p["engagement"] += r.engagement or 0
        p["impressions"] += r.impressions or 0
        p["clicks"] += r.clicks or 0

    platform_table = sorted(
        by_platform.values(), key=lambda x: x["engagement"], reverse=True
    )

    best_platform = platform_table[0]["platform"] if platform_table else None

    return {
        "summary": {
            "platforms_compared": len(platform_table),
            "best_performing_platform": best_platform,
        },
        "tables": {
            "platform_comparison": platform_table,
        },
    }