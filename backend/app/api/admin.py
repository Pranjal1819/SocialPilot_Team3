from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException

from app.core.database import get_db
from app.core.dependencies import get_current_admin

from app.models.user import User
from app.models.campaign import Campaign
from app.models.scheduled_post import ScheduledPost
from app.models.social_account import SocialAccount
from app.models.analytics import PostAnalytics

router = APIRouter(
    prefix="/api/admin",
    tags=["Admin"],
)


# ==========================================================
# ADMIN DASHBOARD
# ==========================================================

@router.get("/dashboard")
def admin_dashboard(
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):

    total_users = db.query(User).count()

    total_campaigns = db.query(Campaign).count()

    total_posts = db.query(ScheduledPost).count()

    published_posts = (
        db.query(ScheduledPost)
        .filter(ScheduledPost.status == "published")
        .count()
    )

    scheduled_posts = (
        db.query(ScheduledPost)
        .filter(ScheduledPost.status == "scheduled")
        .count()
    )

    failed_posts = (
        db.query(ScheduledPost)
        .filter(ScheduledPost.status == "failed")
        .count()
    )

    draft_posts = (
        db.query(ScheduledPost)
        .filter(ScheduledPost.status == "draft")
        .count()
    )

    return {
        "admin": current_admin.name,
        "total_users": total_users,
        "total_campaigns": total_campaigns,
        "total_posts": total_posts,
        "published_posts": published_posts,
        "scheduled_posts": scheduled_posts,
        "failed_posts": failed_posts,
        "draft_posts": draft_posts,
    }


# ==========================================================
# GET ALL USERS
# ==========================================================

@router.get("/users")
def get_all_users(
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),

    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),

    search: str | None = None,
    role: str | None = None,
    is_active: bool | None = None,
):
    """
    Admin - List all users
    """

    query = db.query(User)

    if search:
        query = query.filter(
            or_(
                User.name.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%")
            )
        )

    if role:
        query = query.filter(User.role == role)

    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    total = query.count()

    users = (
        query
        .offset(skip)
        .limit(limit)
        .all()
    )

    result = []

    for user in users:

        campaign_count = (
            db.query(Campaign)
            .filter(Campaign.user_id == user.id)
            .count()
        )

        post_count = (
            db.query(ScheduledPost)
            .filter(ScheduledPost.user_id == user.id)
            .count()
        )

        published_posts = (
            db.query(ScheduledPost)
            .filter(
                ScheduledPost.user_id == user.id,
                ScheduledPost.status == "published",
            )
            .count()
        )

        scheduled_posts = (
            db.query(ScheduledPost)
            .filter(
                ScheduledPost.user_id == user.id,
                ScheduledPost.status == "scheduled",
            )
            .count()
        )

        draft_posts = (
            db.query(ScheduledPost)
            .filter(
                ScheduledPost.user_id == user.id,
                ScheduledPost.status == "draft",
            )
            .count()
        )

        failed_posts = (
            db.query(ScheduledPost)
            .filter(
                ScheduledPost.user_id == user.id,
                ScheduledPost.status == "failed",
            )
            .count()
        )

        result.append(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "is_active": user.is_active,
                "campaigns": campaign_count,
                "posts": post_count,
                "published_posts": published_posts,
                "scheduled_posts": scheduled_posts,
                "draft_posts": draft_posts,
                "failed_posts": failed_posts,
                "connected_accounts": db.query(SocialAccount).filter(SocialAccount.user_id == user.id).count(),
            }
        )

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "users": result,
    }
@router.get("/users/{user_id}")
def get_user_details(
    user_id: int,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """
    Admin - View one user's complete details
    """

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    campaigns = (
        db.query(Campaign)
        .filter(Campaign.user_id == user.id)
        .all()
    )

    posts = (
        db.query(ScheduledPost)
        .filter(ScheduledPost.user_id == user.id)
        .all()
    )

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active,

        "campaigns": [
            {
                "id": campaign.id,
                "name": campaign.name,
                "platform": campaign.platform,
                "status": campaign.status,
                "start_date": campaign.start_date,
                "end_date": campaign.end_date,
            }
            for campaign in campaigns
        ],

        "posts": [
            {
                "id": post.id,
                "title": post.title,
                "platform": post.platform,
                "status": post.status,
                "scheduled_time": post.scheduled_time,
                "published_at": post.published_at,
                "campaign_id": post.campaign_id,
            }
            for post in posts
        ]
    }


# ==========================================================
# ACTIVATE / DEACTIVATE USER
# ==========================================================

@router.patch("/users/{user_id}/status")
def update_user_status(
    user_id: int,
    is_active: bool,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """
    Admin - Activate / Deactivate a user
    """

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user.role == "administrator":
        raise HTTPException(
            status_code=400,
            detail="Admin account cannot be disabled"
        )

    user.is_active = is_active

    db.commit()
    db.refresh(user)

    return {
        "message": "User status updated successfully",
        "user_id": user.id,
        "is_active": user.is_active,
    }


@router.get("/analytics")
def admin_analytics(
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
    user_id: int | None = Query(None, ge=1),
):
    """Return database-backed platform metrics for all users or one user."""
    users_query = db.query(User)
    if user_id is not None:
        users_query = users_query.filter(User.id == user_id)
    users = users_query.all()
    user_ids = [user.id for user in users]

    posts = db.query(ScheduledPost).filter(ScheduledPost.user_id.in_(user_ids)).all() if user_ids else []
    analytics = db.query(PostAnalytics).filter(PostAnalytics.user_id.in_(user_ids)).all() if user_ids else []
    by_user = []
    by_platform = {}
    for row in analytics:
        platform = (row.platform or "unknown").lower()
        metric = by_platform.setdefault(platform, {"platform": platform, "posts": 0, "engagement": 0, "reach": 0, "impressions": 0})
        metric["posts"] += 1
        metric["engagement"] += (row.likes or 0) + (row.comments or 0) + (row.shares or 0)
        metric["reach"] += row.reach or 0
        metric["impressions"] += row.impressions or 0
    for user in users:
        user_posts = [post for post in posts if post.user_id == user.id]
        user_analytics = [row for row in analytics if row.user_id == user.id]
        by_user.append({
            "user_id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "total_posts": len(user_posts),
            "published_posts": sum(post.status == "published" for post in user_posts),
            "scheduled_posts": sum(post.status == "scheduled" for post in user_posts),
            "draft_posts": sum(post.status == "draft" for post in user_posts),
            "total_engagement": sum((row.likes or 0) + (row.comments or 0) + (row.shares or 0) for row in user_analytics),
            "reach": sum(row.reach or 0 for row in user_analytics),
            "impressions": sum(row.impressions or 0 for row in user_analytics),
        })

    return {
        "totals": {
            "total_users": len(users),
            "business_owners": sum(user.role in ("business_owner", "business_user") for user in users),
            "marketing_teams": sum(user.role == "marketing_team" for user in users),
            "content_creators": sum(user.role == "content_creator" for user in users),
            "active_users": sum(bool(user.is_active) for user in users),
            "suspended_users": sum(not user.is_active for user in users),
            "total_posts": len(posts),
            "total_engagement": sum((row.likes or 0) + (row.comments or 0) + (row.shares or 0) for row in analytics),
        },
        "users": by_user,
        "platforms": list(by_platform.values()),
    }


# ==========================================================
# DELETE USER
# ==========================================================

@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """
    Admin - Delete a user
    """

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user.role == "administrator":
        raise HTTPException(
            status_code=400,
            detail="Administrator cannot be deleted"
        )

    db.delete(user)
    db.commit()

    return {
        "message": "User deleted successfully"
    }