# app/services/notification_service.py

from datetime import datetime

from sqlalchemy.orm import Session

from app.models.notification import Notification
from app.models.notification_preference import NotificationPreference
from app.services.logger import logger

CATEGORY_PREFERENCE_MAP = {
    "publishing": "publishing_enabled",
    "campaign": "campaign_enabled",
    "account_activity": "account_activity_enabled",
    "team_collaboration": "team_collaboration_enabled",
    "system": "system_enabled",
}


class NotificationService:

    def __init__(self, db: Session):
        self.db = db

    # --------------------------------------------------
    # Get or create preferences (so every user has a row
    # with sane defaults, even before they visit Settings)
    # --------------------------------------------------

    def get_or_create_preferences(self, user_id: int) -> NotificationPreference:

        prefs = (
            self.db.query(NotificationPreference)
            .filter(NotificationPreference.user_id == user_id)
            .first()
        )

        if prefs:
            return prefs

        prefs = NotificationPreference(user_id=user_id)

        self.db.add(prefs)
        self.db.commit()
        self.db.refresh(prefs)

        return prefs

    # --------------------------------------------------
    # Create Notification
    # --------------------------------------------------
    #
    # category: publishing / campaign / account_activity /
    #           team_collaboration / system
    #
    # notification_type: e.g. post_published, campaign_created,
    #           token_expired, task_assigned, etc.
    # --------------------------------------------------

    def create_notification(
        self,
        user_id: int,
        title: str,
        description: str,
        category: str,
        notification_type: str,
    ):

        prefs = self.get_or_create_preferences(user_id)

        category_field = CATEGORY_PREFERENCE_MAP.get(category)

        # If category is unrecognized, default to allowing it
        # rather than silently dropping a notification.

        category_enabled = getattr(prefs, category_field) if category_field else True

        if not category_enabled:

            logger.info(
                f"[NOTIFICATION] Skipped — user {user_id} has "
                f"{category} notifications disabled"
            )

            return None

        notification = None

        # ------------------------------------------
        # In-app notification
        # ------------------------------------------

        if prefs.in_app_enabled:

            notification = Notification(
                user_id=user_id,
                title=title,
                message=description,
                category=category,
                type=notification_type,
                delivery_channel="in_app",
                is_read=False,
            )

            self.db.add(notification)
            self.db.commit()
            self.db.refresh(notification)

            logger.info(
                f"[NOTIFICATION] Created in-app notification "
                f"{notification.id} for user {user_id}"
            )

        # ------------------------------------------
        # Simulated email (dev mode — logged only)
        # ------------------------------------------

        if prefs.email_enabled:

            self._simulate_email(user_id, title, description, prefs.email_frequency)

            # Also log a row so it shows up in Notification
            # History with delivery_channel = "email", even
            # if in-app was also created above.

            email_notification = Notification(
                user_id=user_id,
                title=title,
                message=description,
                category=category,
                type=notification_type,
                delivery_channel="email",
                is_read=False,
            )

            self.db.add(email_notification)
            self.db.commit()

        # ------------------------------------------
        # Push — future/disabled, no real delivery
        # ------------------------------------------

        if prefs.push_enabled:

            logger.info(
                f"[NOTIFICATION] Push enabled for user {user_id} "
                f"but push delivery is not implemented (dev mode)"
            )

        return notification

    # --------------------------------------------------
    # Simulated Email (dev mode)
    # --------------------------------------------------

    def _simulate_email(self, user_id, title, description, frequency):

        logger.info(
            f"[EMAIL SIMULATION] To user {user_id} | "
            f"Frequency: {frequency} | "
            f"Subject: {title} | Body: {description}"
        )

        # In a real deployment this is where an email
        # provider (SES, SendGrid, etc.) would be called.
        # For this internship's dev-mode requirement, logging
        # is sufficient — no production email is sent.
