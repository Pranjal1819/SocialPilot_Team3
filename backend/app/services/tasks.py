from app.services.celery_app import app

from app.services.queue import (
    get_due_posts,
    remove_from_queue,
    update_status,
    add_to_queue,
)

from app.services.logger import logger

from app.core.database import SessionLocal
from app.core.security import decrypt_token

from app.models.scheduled_post import ScheduledPost
from app.models.notification import Notification
from app.models.social_account import SocialAccount

from app.services.social.linkedin import LinkedInService

from datetime import datetime, timedelta

# ==================================================
# TASK 1:
# Check Redis queue and publish due posts
# ==================================================


@app.task
def check_and_publish():

    due_posts = get_due_posts()

    logger.info(f"[QUEUE] Found {len(due_posts)} posts due for publishing")

    for post_id in due_posts:

        publish_post.delay(int(post_id))


# ==================================================
# TASK 2:
# Publish Scheduled Post
#
# scheduled
#      ↓
# processing
#      ↓
# published / failed
# ==================================================


@app.task(bind=True, max_retries=3)
def publish_post(self, post_id: int):

    db = SessionLocal()

    access_token = None

    try:

        post = db.query(ScheduledPost).filter(ScheduledPost.id == post_id).first()

        if not post:

            logger.warning(f"[POST {post_id}] Post not found")

            remove_from_queue(post_id)

            return

        try:

            # --------------------------------
            # CHECK SCHEDULE TIME
            # --------------------------------

            if post.scheduled_time > datetime.now():

                logger.info(f"[POST {post_id}] Scheduled time not reached")

                return

            # --------------------------------
            # PROCESSING STATUS
            # --------------------------------

            post.status = "processing"

            db.commit()

            update_status(post_id, "processing")

            logger.info(f"[POST {post_id}] STATUS: PROCESSING")

            # --------------------------------
            # GET EXACT SOCIAL ACCOUNT
            # --------------------------------

            account = (
                db.query(SocialAccount)
                .filter(
                    SocialAccount.id == post.social_account_id,
                    SocialAccount.is_active == True,
                )
                .first()
            )

            if not account:

                raise Exception("Social account not found or inactive")

            logger.info(f"[POST {post_id}] " f"Using account {account.account_name}")

            # --------------------------------
            # DECRYPT TOKEN
            # --------------------------------

            access_token = decrypt_token(account.access_token)

            logger.info(f"[POST {post_id}] Token decrypted")

            # --------------------------------
            # PLATFORM PUBLISHING
            # --------------------------------

            platform_post_id = None

            if post.platform.lower() == "linkedin":

                linkedin_service = LinkedInService()

                response = linkedin_service.publish_post(
                    access_token=access_token,
                    author_id=account.account_id,
                    text=post.caption,
                )

                logger.info(f"[POST {post_id}] " f"LinkedIn Response: {response}")

                if not response:

                    raise Exception("LinkedIn returned empty response")

                platform_post_id = response.get("id")

                if not platform_post_id:

                    raise Exception("LinkedIn post id missing")

            else:

                raise Exception(f"{post.platform} not supported")

            # --------------------------------
            # SUCCESS UPDATE
            # --------------------------------

            post.status = "published"

            post.published_at = datetime.now()

            # Save LinkedIn details

            post.platform_post_id = platform_post_id

            post.published_url = (
                f"https://www.linkedin.com/feed/update/{platform_post_id}"
            )

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

                logger.warning(f"[POST {post_id}] " f"Retry {post.retry_count}/3")

                raise self.retry(exc=e, countdown=60)

            # FINAL FAILURE

            post.status = "failed"

            post.failure_reason = str(e)

            db.commit()

            update_status(post_id, "failed")

            notification = Notification(
                user_id=post.user_id,
                message=(
                    f'Your post "{post.title}" '
                    f"failed on {post.platform}. "
                    f"Reason: {str(e)}"
                ),
                type="post_failed",
            )

            db.add(notification)

            db.commit()

            logger.error(f"[POST {post_id}] STATUS: FAILED")

    finally:

        access_token = None

        db.close()


# ==================================================
# TASK 3:
# Recurring Posts
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
                social_account_id=post.social_account_id,
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
            )

            db.add(new_post)

            if post.recurrence_type == "daily":

                post.next_run_time += timedelta(days=post.recurrence_interval)

            elif post.recurrence_type == "weekly":

                post.next_run_time += timedelta(weeks=post.recurrence_interval)

            elif post.recurrence_type == "monthly":

                post.next_run_time += timedelta(days=30 * post.recurrence_interval)

            db.commit()

            add_to_queue(new_post.id, new_post.scheduled_time.timestamp())

            logger.info(f"Recurring post created {new_post.id}")

    finally:

        db.close()


# ==================================================
# TASK 4:
# Token Expiry Notification
# ==================================================


@app.task
def refresh_expiring_tokens():

    db = SessionLocal()

    try:

        expiry_threshold = datetime.now() + timedelta(hours=1)

        accounts = (
            db.query(SocialAccount)
            .filter(
                SocialAccount.token_expires_at <= expiry_threshold,
                SocialAccount.is_active == True,
            )
            .all()
        )

        logger.info(f"Tokens expiring: {len(accounts)}")

        for account in accounts:

            notification = Notification(
                user_id=account.user_id,
                message=(f"Your {account.platform} " f"connection needs attention."),
                type="token_expired",
            )

            db.add(notification)

            db.commit()

    finally:

        db.close()
