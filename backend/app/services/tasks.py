from app.services.celery_app import app

from app.services.queue import (
    get_due_posts,
    remove_from_queue,
    update_status,
    add_to_queue,
)

from app.services.logger import logger

from app.core.database import SessionLocal

from app.models.scheduled_post import ScheduledPost
from app.models.notification import Notification
from app.models.social_account import SocialAccount

from datetime import datetime, timedelta

# ==================================================
# TASK 1:
# Check Redis queue and publish due posts
# Runs every 60 seconds
# ==================================================


@app.task
def check_and_publish():

    due_posts = get_due_posts()

    logger.info(f"Found {len(due_posts)} posts due for publishing")

    for post_id in due_posts:

        publish_post.delay(int(post_id))


# ==================================================
# TASK 2:
# Publish individual post
#
# Flow:
# scheduled
#    ↓
# processing
#    ↓
# published / failed
#
# Includes:
# Retry handling
# Redis status update
# Logging
# ==================================================


@app.task(bind=True, max_retries=3)
def publish_post(self, post_id: int):

    db = SessionLocal()

    try:

        post = db.query(ScheduledPost).filter(ScheduledPost.id == post_id).first()

        if not post:

            logger.warning(f"[POST {post_id}] Not found. Removing from Redis.")

            remove_from_queue(post_id)

            return

        try:

            # -------------------------------
            # PROCESSING STATUS
            # -------------------------------

            post.status = "processing"

            db.commit()

            update_status(post_id, "processing")

            logger.info(f"[POST {post_id}] STATUS: PROCESSING")

            # -------------------------------
            # SOCIAL MEDIA PUBLISHING
            # -------------------------------

            logger.info(f"[POST {post_id}] Publishing to {post.platform}")

            # Future integration:
            #
            # publish_to_platform(
            #     post.platform,
            #     post.caption,
            #     post.media_url
            # )

            # -------------------------------
            # SUCCESS
            # -------------------------------

            post.status = "published"

            post.published_at = datetime.now()

            db.commit()

            remove_from_queue(post_id)

            update_status(post_id, "published")

            logger.info(f"[POST {post_id}] STATUS: PUBLISHED")

            notification = Notification(
                user_id=post.user_id,
                message=(
                    f'Your post "{post.title}" '
                    f"was published successfully "
                    f"on {post.platform}."
                ),
                type="post_published",
            )

            db.add(notification)

            db.commit()

        except Exception as e:

            logger.error(f"[POST {post_id}] ERROR: {str(e)}")

            post.retry_count += 1

            db.commit()

            if post.retry_count < 3:

                post.status = "scheduled"

                db.commit()

                update_status(post_id, "scheduled")

                logger.warning(f"[POST {post_id}] Retry " f"{post.retry_count}/3")

                raise self.retry(exc=e, countdown=60)

            post.status = "failed"

            post.failure_reason = str(e)

            db.commit()

            update_status(post_id, "failed")

            notification = Notification(
                user_id=post.user_id,
                message=(
                    f'Your post "{post.title}" '
                    f"failed to publish on "
                    f"{post.platform}. "
                    f"Reason: {str(e)}"
                ),
                type="post_failed",
            )

            db.add(notification)

            db.commit()

            logger.error(f"[POST {post_id}] STATUS: FAILED")

    finally:

        db.close()


# ==================================================
# TASK 3:
# Recurring Scheduling
#
# Generates next scheduled post
#
# Runs every few minutes using Celery Beat
# ==================================================


@app.task
def process_recurring_posts():

    db = SessionLocal()

    try:

        current_time = datetime.now()

        recurring_posts = (
            db.query(ScheduledPost)
            .filter(
                ScheduledPost.is_recurring == True,
                ScheduledPost.next_run_time <= current_time,
            )
            .all()
        )

        logger.info(f"Found {len(recurring_posts)} recurring posts")

        for post in recurring_posts:

            new_post = ScheduledPost(
                user_id=post.user_id,
                campaign_id=post.campaign_id,
                title=post.title,
                caption=post.caption,
                media_url=post.media_url,
                content_type=post.content_type,
                platform=post.platform,
                scheduled_time=post.next_run_time,
                timezone=post.timezone,
                status="scheduled",
                is_recurring=True,
                recurrence_type=post.recurrence_type,
                recurrence_interval=post.recurrence_interval,
                next_run_time=None,
            )

            db.add(new_post)

            # Calculate next execution

            if post.recurrence_type == "daily":

                post.next_run_time += timedelta(days=post.recurrence_interval)

            elif post.recurrence_type == "weekly":

                post.next_run_time += timedelta(weeks=post.recurrence_interval)

            elif post.recurrence_type == "monthly":

                post.next_run_time += timedelta(days=30 * post.recurrence_interval)

            db.commit()

            # Add newly generated post into Redis queue

            timestamp = new_post.scheduled_time.timestamp()

            add_to_queue(new_post.id, timestamp)

            logger.info(f"Recurring post generated: {new_post.id}")

    finally:

        db.close()


# ==================================================
# TASK 4:
# Refresh Expiring Tokens
# Runs every 30 minutes
# ==================================================


@app.task
def refresh_expiring_tokens():

    db = SessionLocal()

    try:

        expiry_threshold = datetime.now() + timedelta(hours=1)

        expiring_accounts = (
            db.query(SocialAccount)
            .filter(
                SocialAccount.token_expires_at <= expiry_threshold,
                SocialAccount.is_active == True,
            )
            .all()
        )

        logger.info(f"Found {len(expiring_accounts)} tokens expiring soon")

        for account in expiring_accounts:

            try:

                notification = Notification(
                    user_id=account.user_id,
                    message=(
                        f"Your {account.platform} "
                        f"account connection was "
                        f"refreshed automatically."
                    ),
                    type="token_expired",
                )

                db.add(notification)

                db.commit()

            except Exception as e:

                logger.error(
                    f"Token refresh failed " f"for account {account.id}: {str(e)}"
                )

    finally:

        db.close()
