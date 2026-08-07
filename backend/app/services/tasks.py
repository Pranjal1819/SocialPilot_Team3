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
from app.models.post_media import PostMedia

from app.services.social.linkedin import LinkedInService

from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse

from PIL import Image

# ==================================================
# Convert media URL to local path
# ==================================================


def get_local_media_path(media):

    if media.file_path:
        return media.file_path

    parsed = urlparse(media.media_url)

    local_path = Path("app/static") / parsed.path.lstrip("/")

    return str(local_path)


# ==================================================
# TASK 1
# Check Redis queue
# ==================================================


@app.task
def check_and_publish():

    due_posts = get_due_posts()

    logger.info(f"[QUEUE] Found {len(due_posts)} posts")

    for post_id in due_posts:

        publish_post.delay(int(post_id))


# ==================================================
# TASK 2
# Publish Scheduled Post
# ==================================================


@app.task(bind=True, max_retries=3)
def publish_post(self, post_id: int):

    db = SessionLocal()

    try:

        post = db.query(ScheduledPost).filter(ScheduledPost.id == post_id).first()

        if not post:

            logger.warning(f"[POST {post_id}] Not found")

            remove_from_queue(post_id)

            return

        try:

            # --------------------------
            # Check schedule
            # --------------------------

            if post.scheduled_time > datetime.now():

                logger.info(f"[POST {post_id}] Not due")

                return

            # --------------------------
            # PROCESSING
            # --------------------------

            post.status = "processing"
            db.commit()

            update_status(post_id, "processing")

            account = (
                db.query(SocialAccount)
                .filter(
                    SocialAccount.id == post.social_account_id,
                    SocialAccount.is_active == True,
                )
                .first()
            )

            if not account:
                raise Exception("Social account inactive")

            access_token = decrypt_token(account.access_token)

            linkedin = LinkedInService()

            platform_post_id = None
            response = None

            # ==================================================
            # LINKEDIN
            # ==================================================

            if post.platform.lower() == "linkedin":

                media_files = post.media_files

                # ==================================================
                # TEXT POST
                # ==================================================

                if not media_files:

                    response = linkedin.publish_post(
                        access_token,
                        account.account_id,
                        post.caption,
                    )

                # ==================================================
                # CAROUSEL POST
                # LinkedIn Carousel = PDF Document Carousel
                # ==================================================

                elif post.content_type == "carousel":

                    logger.info(f"[POST {post_id}] Carousel processing started")

                    if len(media_files) < 2:
                        raise Exception("Carousel requires minimum 2 media files")

                    carousel_images = []

                    temp_pdf = Path("app/static") / f"carousel_{post_id}.pdf"

                    try:

                        # ------------------------------------------
                        # Convert uploaded images into PDF
                        # ------------------------------------------

                        for media in media_files:

                            if media.media_type not in ["image", "gif"]:
                                raise Exception(
                                    "LinkedIn carousel supports only images"
                                )

                            file_path = get_local_media_path(media)

                            if not Path(file_path).exists():
                                raise Exception(f"Media file not found: {file_path}")

                            img = Image.open(file_path)

                            if img.mode != "RGB":
                                img = img.convert("RGB")

                            carousel_images.append(img)

                        if not carousel_images:
                            raise Exception("No valid carousel images found")

                        first_image = carousel_images[0]
                        remaining_images = carousel_images[1:]

                        first_image.save(
                            temp_pdf,
                            save_all=True,
                            append_images=remaining_images,
                        )

                        logger.info(f"[POST {post_id}] Carousel PDF created {temp_pdf}")

                        # ------------------------------------------
                        # Upload PDF to LinkedIn
                        # ------------------------------------------

                        upload_response = linkedin.register_media(
                            access_token,
                            account.account_id,
                            "document",
                        )

                        upload_url = upload_response["value"]["uploadMechanism"][
                            "com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"
                        ]["uploadUrl"]

                        asset = upload_response["value"]["asset"]

                        linkedin.upload_media_file(
                            access_token,
                            upload_url,
                            str(temp_pdf),
                        )

                        logger.info(f"[POST {post_id}] Carousel PDF uploaded {asset}")

                        response = linkedin.publish_carousel_post(
                            access_token,
                            account.account_id,
                            post.caption,
                            asset,
                        )

                    finally:

                        # cleanup generated PDF
                        if temp_pdf.exists():
                            temp_pdf.unlink()

                    logger.info(f"[POST {post_id}] Carousel upload complete")

                # ==================================================
                # SINGLE MEDIA
                # ==================================================

                else:

                    media = media_files[0]

                    supported_types = [
                        "image",
                        "gif",
                        "video",
                        "document",
                        "audio",
                    ]

                    if media.media_type not in supported_types:
                        raise Exception(f"Unsupported media type {media.media_type}")

                    file_path = get_local_media_path(media)

                    if not Path(file_path).exists():
                        raise Exception(f"Media file not found: {file_path}")

                    logger.info(f"[POST {post_id}] Media type {media.media_type}")

                    upload_response = linkedin.register_media(
                        access_token,
                        account.account_id,
                        media.media_type,
                    )

                    upload_url = upload_response["value"]["uploadMechanism"][
                        "com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"
                    ]["uploadUrl"]

                    asset = upload_response["value"]["asset"]

                    linkedin.upload_media_file(
                        access_token,
                        upload_url,
                        file_path,
                    )

                    response = linkedin.publish_media_post(
                        access_token,
                        account.account_id,
                        post.caption,
                        asset,
                        media.media_type,
                    )

            else:

                raise Exception(f"{post.platform} not supported")

            logger.info(f"[POST {post_id}] LinkedIn Response {response}")

            platform_post_id = response.get("id")

            if not platform_post_id:
                raise Exception("LinkedIn post id missing")

            # ==================================================
            # SUCCESS
            # ==================================================

            post.status = "published"
            post.published_at = datetime.now()
            post.platform_post_id = platform_post_id

            post.published_url = (
                "https://www.linkedin.com/feed/update/" f"{platform_post_id}"
            )

            db.commit()

            remove_from_queue(post_id)

            update_status(post_id, "published")

            db.add(
                Notification(
                    user_id=post.user_id,
                    message=(
                        f'Your post "{post.title}" '
                        f"was published successfully on "
                        f"{post.platform}"
                    ),
                    type="post_published",
                )
            )

            db.commit()

            logger.info(f"[POST {post_id}] PUBLISHED")

        except Exception as e:

            logger.error(f"[POST {post_id}] ERROR {e}")

            db.rollback()

            post.status = "failed"
            db.commit()

            update_status(post_id, "failed")

            db.add(
                Notification(
                    user_id=post.user_id,
                    message=(
                        f'Your post "{post.title}" '
                        f"failed to publish on {post.platform}: {e}"
                    ),
                    type="post_failed",
                )
            )

            db.commit()

            try:
                raise self.retry(exc=e, countdown=60)
            except self.MaxRetriesExceededError:
                logger.error(f"[POST {post_id}] Max retries exceeded")
                remove_from_queue(post_id)

    finally:

        db.close()


# ==================================================
# TASK 3
# Recurring Posts
# ==================================================


@app.task
def process_recurring_posts():

    db = SessionLocal()

    try:

        now = datetime.now()

        posts = (
            db.query(ScheduledPost)
            .filter(
                ScheduledPost.is_recurring == True,
                ScheduledPost.next_run_time <= now,
            )
            .all()
        )

        for post in posts:

            new_post = ScheduledPost(
                user_id=post.user_id,
                campaign_id=post.campaign_id,
                social_account_id=post.social_account_id,
                title=post.title,
                caption=post.caption,
                content_type=post.content_type,
                platform=post.platform,
                scheduled_time=post.next_run_time,
                status="scheduled",
                is_recurring=True,
                recurrence_type=post.recurrence_type,
                recurrence_interval=post.recurrence_interval,
            )

            db.add(new_post)
            db.flush()

            # Copy media files
            for media in post.media_files:

                db.add(
                    PostMedia(
                        post_id=new_post.id,
                        media_url=media.media_url,
                        file_path=media.file_path,
                        media_type=media.media_type,
                        thumbnail_url=media.thumbnail_url,
                        mime_type=media.mime_type,
                        file_size=media.file_size,
                        duration=media.duration,
                        display_order=media.display_order,
                    )
                )

            db.commit()

            add_to_queue(new_post.id, new_post.scheduled_time.timestamp())

            logger.info(f"[RECURRING] Created post {new_post.id}")

    except Exception as e:

        logger.error(f"[RECURRING] ERROR {e}")

        db.rollback()

        raise

    finally:

        db.close()


# ==================================================
# TASK 4
# Token Expiry Notification
# ==================================================


@app.task
def refresh_expiring_tokens():

    db = SessionLocal()

    try:

        expiry = datetime.now() + timedelta(hours=1)

        accounts = (
            db.query(SocialAccount)
            .filter(
                SocialAccount.token_expires_at <= expiry,
                SocialAccount.is_active == True,
            )
            .all()
        )

        for account in accounts:

            db.add(
                Notification(
                    user_id=account.user_id,
                    message=(f"Your {account.platform} " "connection needs attention."),
                    type="token_expired",
                )
            )

        db.commit()

    except Exception as e:

        logger.error(f"[TOKEN REFRESH] ERROR {e}")

        db.rollback()

        raise

    finally:

        db.close()
