from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException

from app.core.database import get_db
from app.core.dependencies import get_current_admin

from app.models.user import User
from app.models.campaign import Campaign
from app.models.scheduled_post import ScheduledPost

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

    if user.role == "admin":
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

    if user.role == "admin":
        raise HTTPException(
            status_code=400,
            detail="Administrator cannot be deleted"
        )

    db.delete(user)
    db.commit()

    return {
        "message": "User deleted successfully"
    }