from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.models.user import User
from app.models.notification import Notification
from app.models.notification_preference import NotificationPreference

from app.schemas.notification import (
    NotificationResponse,
    NotificationListResponse,
    NotificationPreferenceResponse,
    NotificationPreferenceUpdate,
    EmailPreferenceUpdate,
)

router = APIRouter(prefix="/api/notifications", tags=["Notifications"])


# ---------------------------------------------------------
# Get All Notifications (with search/filter/unread, paginated)
# ---------------------------------------------------------


@router.get("", response_model=NotificationListResponse)
def get_notifications(
    category: Optional[str] = Query(None),
    unread_only: bool = Query(False),
    search: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    query = db.query(Notification).filter(Notification.user_id == current_user.id)

    if category and category.lower() != "all":
        query = query.filter(Notification.category == category.lower())

    if unread_only:
        query = query.filter(Notification.is_read == False)

    if search:
        query = query.filter(
            or_(
                Notification.title.ilike(f"%{search}%"),
                Notification.message.ilike(f"%{search}%"),
            )
        )

    if start_date:
        query = query.filter(Notification.created_at >= start_date)

    if end_date:
        query = query.filter(Notification.created_at <= end_date)

    total = query.count()

    notifications = (
        query.order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()
    )

    return NotificationListResponse(
        total=total,
        skip=skip,
        limit=limit,
        notifications=notifications,
    )


# ---------------------------------------------------------
# Get Single Notification
# ---------------------------------------------------------


@router.get("/{notification_id}", response_model=NotificationResponse)
def get_notification(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    notification = (
        db.query(Notification)
        .filter(
            Notification.id == notification_id,
            Notification.user_id == current_user.id,
        )
        .first()
    )

    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    return notification


# ---------------------------------------------------------
# Mark Single Notification as Read
# ---------------------------------------------------------


@router.patch("/{notification_id}/read", response_model=NotificationResponse)
def mark_as_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    notification = (
        db.query(Notification)
        .filter(
            Notification.id == notification_id,
            Notification.user_id == current_user.id,
        )
        .first()
    )

    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    notification.is_read = True
    notification.read_at = datetime.utcnow()

    db.commit()
    db.refresh(notification)

    return notification


# ---------------------------------------------------------
# Mark All Notifications as Read
# ---------------------------------------------------------


@router.patch("/read-all")
def mark_all_as_read(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    updated = (
        db.query(Notification)
        .filter(
            Notification.user_id == current_user.id,
            Notification.is_read == False,
        )
        .update(
            {"is_read": True, "read_at": datetime.utcnow()},
            synchronize_session=False,
        )
    )

    db.commit()

    return {"message": f"{updated} notification(s) marked as read"}


# ---------------------------------------------------------
# Delete Notification
# ---------------------------------------------------------


@router.delete("/{notification_id}")
def delete_notification(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    notification = (
        db.query(Notification)
        .filter(
            Notification.id == notification_id,
            Notification.user_id == current_user.id,
        )
        .first()
    )

    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    db.delete(notification)
    db.commit()

    return {"message": "Notification deleted"}


# ---------------------------------------------------------
# Get Notification Settings (preferences)
# ---------------------------------------------------------


@router.get("/settings/preferences", response_model=NotificationPreferenceResponse)
def get_preferences(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    prefs = (
        db.query(NotificationPreference)
        .filter(NotificationPreference.user_id == current_user.id)
        .first()
    )

    if not prefs:

        prefs = NotificationPreference(user_id=current_user.id)

        db.add(prefs)
        db.commit()
        db.refresh(prefs)

    return prefs


# ---------------------------------------------------------
# Update Notification Settings (category + channel toggles)
# ---------------------------------------------------------


@router.put("/settings/preferences", response_model=NotificationPreferenceResponse)
def update_preferences(
    update_data: NotificationPreferenceUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    prefs = (
        db.query(NotificationPreference)
        .filter(NotificationPreference.user_id == current_user.id)
        .first()
    )

    if not prefs:
        prefs = NotificationPreference(user_id=current_user.id)
        db.add(prefs)

    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(prefs, key, value)

    db.commit()
    db.refresh(prefs)

    return prefs


# ---------------------------------------------------------
# Get Email Preferences
# ---------------------------------------------------------


@router.get("/settings/email", response_model=NotificationPreferenceResponse)
def get_email_preferences(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    prefs = (
        db.query(NotificationPreference)
        .filter(NotificationPreference.user_id == current_user.id)
        .first()
    )

    if not prefs:
        prefs = NotificationPreference(user_id=current_user.id)
        db.add(prefs)
        db.commit()
        db.refresh(prefs)

    return prefs


# ---------------------------------------------------------
# Update Email Preferences
# ---------------------------------------------------------


@router.put("/settings/email", response_model=NotificationPreferenceResponse)
def update_email_preferences(
    update_data: EmailPreferenceUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    prefs = (
        db.query(NotificationPreference)
        .filter(NotificationPreference.user_id == current_user.id)
        .first()
    )

    if not prefs:
        prefs = NotificationPreference(user_id=current_user.id)
        db.add(prefs)

    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(prefs, key, value)

    db.commit()
    db.refresh(prefs)

    return prefs
