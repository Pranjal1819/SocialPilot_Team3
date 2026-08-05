from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.models.user import User
from app.models.scheduled_post import ScheduledPost
from app.models.social_account import SocialAccount

from app.schemas.scheduled_post import (
    ScheduledPostCreate,
    ScheduledPostUpdate,
    ScheduledPostResponse,
)

from app.services.queue import (
    add_to_queue,
    remove_from_queue,
)

router = APIRouter(prefix="/api/posts", tags=["Posts"])


# =================================================
# CREATE SCHEDULED POST
# =================================================


@router.post("/", response_model=ScheduledPostResponse)
def create_post(
    post: ScheduledPostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    # ---------------------------------------------
    # Validate Social Account
    # ---------------------------------------------

    account = (
        db.query(SocialAccount)
        .filter(
            SocialAccount.id == post.social_account_id,
            SocialAccount.user_id == current_user.id,
            SocialAccount.is_active == True,
        )
        .first()
    )

    if not account:

        raise HTTPException(
            status_code=400, detail="Invalid or inactive social account"
        )

    # ---------------------------------------------
    # Create Post
    # ---------------------------------------------

    db_post = ScheduledPost(**post.dict(), user_id=current_user.id, status="scheduled")

    db.add(db_post)

    db.commit()

    db.refresh(db_post)

    # ---------------------------------------------
    # Add Redis Queue
    # ---------------------------------------------

    if db_post.scheduled_time:

        add_to_queue(db_post.id, db_post.scheduled_time.timestamp())

    return db_post


# =================================================
# GET ALL POSTS
# =================================================


@router.get("/", response_model=List[ScheduledPostResponse])
def get_posts(
    status: Optional[str] = None,
    platform: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    query = db.query(ScheduledPost).filter(ScheduledPost.user_id == current_user.id)

    if status:

        query = query.filter(ScheduledPost.status == status)

    if platform:

        query = query.filter(ScheduledPost.platform == platform)

    return query.offset(skip).limit(limit).all()


# =================================================
# CALENDAR VIEW
# =================================================


@router.get("/calendar")
def get_calendar(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    query = db.query(ScheduledPost).filter(ScheduledPost.user_id == current_user.id)

    if start_date:

        query = query.filter(ScheduledPost.scheduled_time >= start_date)

    if end_date:

        query = query.filter(ScheduledPost.scheduled_time <= end_date)

    posts = query.all()

    calendar_data = {}

    for post in posts:

        if post.scheduled_time:

            date_key = post.scheduled_time.strftime("%Y-%m-%d")

            if date_key not in calendar_data:

                calendar_data[date_key] = []

            calendar_data[date_key].append(
                {
                    "id": post.id,
                    "content": post.caption[:50] if post.caption else "",
                    "platform": post.platform,
                    "status": post.status,
                    "social_account_id": post.social_account_id,
                    "scheduled_time": post.scheduled_time,
                }
            )

    return calendar_data


# =================================================
# UPDATE POST
# =================================================


@router.put("/{post_id}", response_model=ScheduledPostResponse)
def update_post(
    post_id: int,
    post_update: ScheduledPostUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    db_post = (
        db.query(ScheduledPost)
        .filter(ScheduledPost.id == post_id, ScheduledPost.user_id == current_user.id)
        .first()
    )

    if not db_post:

        raise HTTPException(status_code=404, detail="Post not found")

    if db_post.status == "published":

        raise HTTPException(status_code=400, detail="Cannot update published post")

    update_data = post_update.dict(exclude_unset=True)

    # ---------------------------------------------
    # Validate new social account
    # ---------------------------------------------

    if "social_account_id" in update_data:

        account = (
            db.query(SocialAccount)
            .filter(
                SocialAccount.id == update_data["social_account_id"],
                SocialAccount.user_id == current_user.id,
                SocialAccount.is_active == True,
            )
            .first()
        )

        if not account:

            raise HTTPException(status_code=400, detail="Invalid social account")

    # ---------------------------------------------
    # Update values
    # ---------------------------------------------

    for key, value in update_data.items():

        setattr(db_post, key, value)

    db.commit()

    db.refresh(db_post)

    # ---------------------------------------------
    # Update Redis if time changed
    # ---------------------------------------------

    if "scheduled_time" in update_data:

        add_to_queue(db_post.id, db_post.scheduled_time.timestamp())

    return db_post


# =================================================
# DELETE POST
# =================================================


@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    db_post = (
        db.query(ScheduledPost)
        .filter(ScheduledPost.id == post_id, ScheduledPost.user_id == current_user.id)
        .first()
    )

    if not db_post:

        raise HTTPException(status_code=404, detail="Post not found")

    if db_post.status == "published":

        raise HTTPException(status_code=400, detail="Cannot delete published post")

    # Remove Redis queue

    remove_from_queue(db_post.id)

    db.delete(db_post)

    db.commit()

    return {"message": "Post deleted successfully"}
