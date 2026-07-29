from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate, PostResponse
from app.services.publishing import PublishingService

router = APIRouter(prefix="/api/posts", tags=["Posts"])

@router.post("/", response_model=PostResponse)
def create_post(
    post: PostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_post = Post(
        **post.dict(),
        user_id=current_user.id,
        status="scheduled"
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    
    # If scheduled time is within 5 minutes, publish immediately
    if (post.scheduled_time - datetime.now()).total_seconds() < 300:
        publishing_service = PublishingService(db)
        publishing_service.publish_post(db_post.id)
    
    return db_post

@router.get("/", response_model=List[PostResponse])
def get_posts(
    status: Optional[str] = None,
    platform: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Post).filter(Post.user_id == current_user.id)
    
    if status:
        query = query.filter(Post.status == status)
    if platform:
        query = query.filter(Post.platform == platform)
    
    return query.offset(skip).limit(limit).all()

@router.get("/calendar")
def get_calendar(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Post).filter(Post.user_id == current_user.id)
    
    if start_date:
        query = query.filter(Post.scheduled_time >= start_date)
    if end_date:
        query = query.filter(Post.scheduled_time <= end_date)
    
    posts = query.all()
    # Format for calendar view
    calendar_data = {}
    for post in posts:
        date_key = post.scheduled_time.strftime("%Y-%m-%d")
        if date_key not in calendar_data:
            calendar_data[date_key] = []
        calendar_data[date_key].append({
            "id": post.id,
            "content": post.content[:50],
            "platform": post.platform,
            "status": post.status
        })
    
    return calendar_data

@router.put("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    post_update: PostUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_post = db.query(Post).filter(
        Post.id == post_id,
        Post.user_id == current_user.id
    ).first()
    
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    for key, value in post_update.dict(exclude_unset=True).items():
        setattr(db_post, key, value)
    
    db.commit()
    db.refresh(db_post)
    return db_post

@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_post = db.query(Post).filter(
        Post.id == post_id,
        Post.user_id == current_user.id
    ).first()
    
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if db_post.status == "published":
        raise HTTPException(status_code=400, detail="Cannot delete published post")
    
    db.delete(db_post)
    db.commit()
    return {"message": "Post deleted successfully"}