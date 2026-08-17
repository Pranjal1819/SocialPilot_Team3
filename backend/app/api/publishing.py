from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.scheduled_post import ScheduledPost
from app.models.publish_log import PublishLog

from app.services.queue import add_to_queue
from app.services.tasks import publish_post

router = APIRouter(prefix="/api/publishing", tags=["Publishing"])


# ==================================================
# GET platform-results for a scheduled post
# (all publish attempts logged for it)
# ==================================================

@router.get("/logs/{post_id}")
def get_publish_logs(post_id: int, db: Session = Depends(get_db)):

    post = db.query(ScheduledPost).filter(ScheduledPost.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Scheduled post not found")

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
def retry_publish(post_id: int, db: Session = Depends(get_db)):

    post = db.query(ScheduledPost).filter(ScheduledPost.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Scheduled post not found")

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