from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.scheduled_post import ScheduledPost
from app.models.social_account import SocialAccount
from app.models.publish_log import PublishLog
from app.models.business_assignment import BusinessAssignment

from app.services.queue import add_to_queue
from app.services.tasks import publish_post

router = APIRouter(prefix="/api/publishing", tags=["Publishing"])


# ==================================================
# Helper — verify the current user may act on a post
# belonging to a business user.
#
# Allowed:
#   - the business user who owns the post
#   - a marketing team assigned to that business user
#   - the administrator
# ==================================================


def _can_manage_post(db: Session, current_user: User, post: ScheduledPost) -> bool:
    if current_user.role == "administrator":
        return True

    if current_user.id == post.user_id:
        return True

    if current_user.role == "marketing_team":
        assignment = (
            db.query(BusinessAssignment)
            .filter(
                BusinessAssignment.marketing_team_id == current_user.id,
                BusinessAssignment.business_user_id == post.user_id,
            )
            .first()
        )
        return assignment is not None

    return False


# ==================================================
# GET platform-results for a scheduled post
# (all publish attempts logged for it)
# ==================================================


@router.get("/logs/{post_id}")
def get_publish_logs(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    post = db.query(ScheduledPost).filter(ScheduledPost.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Scheduled post not found")

    if not _can_manage_post(db, current_user, post):
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to view these publish logs",
        )

    logs = (
        db.query(PublishLog)
        .filter(PublishLog.scheduled_post_id == post_id)
        .order_by(PublishLog.attempt_number.asc())
        .all()
    )

    return {
        "post_id": post.id,
        "status": post.status,
        "logs": [
            {
                "id": log.id,
                "attempt_number": log.attempt_number,
                "status": log.status,
                "platform": log.platform,
                "error_message": log.error_message,
                "platform_post_id": log.platform_post_id,
                "published_url": log.published_url,
                "created_at": log.created_at,
            }
            for log in logs
        ],
    }


# ==================================================
# POST retry a failed post
# ==================================================


@router.post("/retry/{post_id}")
def retry_publish(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    post = db.query(ScheduledPost).filter(ScheduledPost.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Scheduled post not found")

    if not _can_manage_post(db, current_user, post):
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to retry this post",
        )

    if post.status != "failed":
        raise HTTPException(
            status_code=400,
            detail=f"Only 'failed' posts can be retried (current status: {post.status})",
        )

    post.status = "scheduled"
    db.commit()

    # Put it back on the Redis queue exactly the way check_and_publish
    # expects to find it, then fire the same task the queue would
    add_to_queue(post.id, datetime.now().timestamp())
    publish_post.delay(post.id)

    return {"status": "queued", "post_id": post.id}


# ==================================================
# POST publish a draft/scheduled post immediately
# ==================================================

ALLOWED_PUBLISH_NOW_STATUSES = {"draft", "scheduled"}


@router.post("/publish/{post_id}")
def publish(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    post = db.query(ScheduledPost).filter(ScheduledPost.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Scheduled post not found")

    # Server-side assignment check: a Marketing Team may only publish
    # posts for Business Users assigned to them. The business user who
    # owns the post and the administrator are also allowed.
    if not _can_manage_post(db, current_user, post):
        raise HTTPException(
            status_code=403,
            detail="You are not assigned to this client and cannot publish this post",
        )

    if post.status not in ALLOWED_PUBLISH_NOW_STATUSES:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Cannot publish now from status '{post.status}'. "
                f"Only draft or scheduled posts can be published immediately."
            ),
        )

    # The social account belongs to the business user (post.user_id).
    # The access token is retrieved server-side and never exposed to
    # the marketing team.
    account = (
        db.query(SocialAccount)
        .filter(
            SocialAccount.id == post.social_account_id,
            SocialAccount.user_id == post.user_id,
            SocialAccount.is_active == True,
        )
        .first()
    )

    if not account:
        raise HTTPException(
            status_code=400, detail="Social account not found or inactive"
        )

    if not account.is_connected:
        raise HTTPException(status_code=400, detail="Social account is not connected")

    if not account.access_token:
        raise HTTPException(
            status_code=400, detail="Social account has no access token"
        )

    # publish_post returns early as "not due" if scheduled_time is in
    # the future -- pull it forward so the task actually runs instead
    # of silently no-oping.
    post.scheduled_time = datetime.now()
    post.status = "processing"
    db.commit()

    publish_post.delay(post.id)

    return {
        "status": "queued",
        "post_id": post.id,
        "message": "Post queued for immediate publishing",
    }