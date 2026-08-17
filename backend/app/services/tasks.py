from app.services.celery_app import app
from app.models.notification import Notification
from app.services.queue import (
    get_due_posts,
    remove_from_queue,
    update_status,
    add_to_queue,
)

from app.services.logger import logger

from app.core.database import SessionLocal
from app.core.security import decrypt_token, encrypt_token

from app.models.scheduled_post import ScheduledPost
from app.models.social_account import SocialAccount
from app.models.post_media import PostMedia
from app.models.publish_log import PublishLog

from app.services.social.linkedin import LinkedInService
from app.services.social.x import XService
from app.services.social.youtube import YouTubeService
from app.services.notification_service import NotificationService

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

            remove_from_queue(post_id)

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

            platform_post_id = None
            response = None

            # ==================================================
            # LINKEDIN
            # ==================================================

            if post.platform.lower() == "linkedin":

                linkedin = LinkedInService()

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

                platform_post_id = response.get("id")

                if not platform_post_id:
                    raise Exception("LinkedIn post id missing")

                post.published_url = (
                    "https://www.linkedin.com/feed/update/" f"{platform_post_id}"
                )

            # ==================================================
            # X (TWITTER)
            # ==================================================

            elif post.platform.lower() == "x":

                x_service = XService()

                media_files = post.media_files

                # ==================================================
                # TEXT POST
                # ==================================================

                if not media_files:

                    response = x_service.publish_post(
                        access_token,
                        post.caption,
                    )

                # ==================================================
                # MULTI-IMAGE POST (2-4 images/gif, X limit)
                # ==================================================

                elif len(media_files) > 1:

                    if len(media_files) > 4:
                        raise Exception("X supports a maximum of 4 images per post")

                    file_paths = []

                    for media in media_files:

                        if media.media_type not in ["image", "gif"]:
                            raise Exception(
                                "X multi-media posts only support images/gifs"
                            )

                        file_path = get_local_media_path(media)

                        if not Path(file_path).exists():
                            raise Exception(f"Media file not found: {file_path}")

                        file_paths.append(file_path)

                    logger.info(
                        f"[POST {post_id}] X uploading {len(file_paths)} images"
                    )

                    media_ids = x_service.upload_images(
                        access_token,
                        file_paths,
                    )

                    logger.info(f"[POST {post_id}] X images uploaded {media_ids}")

                    response = x_service.publish_multi_image_post(
                        access_token,
                        post.caption,
                        media_ids,
                    )

                # ==================================================
                # SINGLE MEDIA (image, gif, or video)
                # ==================================================

                else:

                    media = media_files[0]

                    file_path = get_local_media_path(media)

                    if not Path(file_path).exists():
                        raise Exception(f"Media file not found: {file_path}")

                    logger.info(f"[POST {post_id}] X media type {media.media_type}")

                    if media.media_type in ["image", "gif"]:

                        media_id = x_service.upload_image(
                            access_token,
                            file_path,
                            media.media_type,
                        )

                    elif media.media_type == "video":

                        media_id = x_service.upload_video(
                            access_token,
                            file_path,
                        )

                    else:

                        raise Exception(
                            f"X does not support media type {media.media_type}"
                        )

                    logger.info(f"[POST {post_id}] X media uploaded {media_id}")

                    response = x_service.publish_media_post(
                        access_token,
                        post.caption,
                        media_id,
                    )

                platform_post_id = response.get("data", {}).get("id")

                if not platform_post_id:
                    raise Exception("X post id missing")

                post.published_url = (
                    f"https://x.com/{account.account_name}/status/{platform_post_id}"
                )

            # ==================================================
            # YOUTUBE
            # ==================================================

            elif post.platform.lower() == "youtube":

                youtube_service = YouTubeService()

                media_files = post.media_files

                if not media_files:
                    raise Exception("YouTube requires a video file")

                media = media_files[0]

                if media.media_type != "video":
                    raise Exception("YouTube only supports video uploads")

                file_path = get_local_media_path(media)

                if not Path(file_path).exists():
                    raise Exception(f"Media file not found: {file_path}")

                logger.info(f"[POST {post_id}] Uploading video to YouTube")

                response = youtube_service.publish_video(
                    access_token,
                    file_path,
                    post.title,
                    post.caption,
                )

                platform_post_id = response.get("id")

                if not platform_post_id:
                    raise Exception("YouTube video id missing")

                post.published_url = f"https://youtube.com/watch?v={platform_post_id}"

            else:

                raise Exception(f"{post.platform} not supported")

            logger.info(f"[POST {post_id}] {post.platform} Response {response}")

            # ==================================================
            # SUCCESS
            # ==================================================

            post.status = "published"
            post.published_at = datetime.now()
            post.platform_post_id = platform_post_id

            db.commit()

            remove_from_queue(post_id)

            update_status(post_id, "published")

            NotificationService(db).create_notification(
                user_id=post.user_id,
                title="Post Published Successfully",
                description=(
                    f'Your post "{post.title}" was published '
                    f"successfully on {post.platform}"
                ),
                category="publishing",
                notification_type="post_published",
            )

            # --------------------------------------------------
            # Publish log — success
            # --------------------------------------------------

            db.add(
                PublishLog(
                    scheduled_post_id=post.id,
                    social_account_id=account.id,
                    platform=post.platform,
                    attempt_number=self.request.retries + 1,
                    status="success",
                    platform_post_id=platform_post_id,
                    published_url=post.published_url,
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

            # --------------------------------------------------
            # Publish log — failure (logged every attempt)
            # --------------------------------------------------

            db.add(
                PublishLog(
                    scheduled_post_id=post.id,
                    social_account_id=(
                        account.id if "account" in locals() and account else None
                    ),
                    platform=post.platform,
                    attempt_number=self.request.retries + 1,
                    status="failed",
                    error_message=str(e),
                )
            )

            db.commit()

            if self.request.retries >= self.max_retries:

                logger.error(f"[POST {post_id}] Max retries exceeded")

                remove_from_queue(post_id)

                NotificationService(db).create_notification(
                    user_id=post.user_id,
                    title="Post Publishing Failed",
                    description=(
                        f'Your post "{post.title}" failed to publish '
                        f"on {post.platform}: {e}"
                    ),
                    category="publishing",
                    notification_type="publishing_failed",
                )

            else:

                raise self.retry(exc=e, countdown=60)

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
# Automatic Token Refresh
# ==================================================


@app.task
def refresh_expiring_tokens():

    db = SessionLocal()

    try:

        expiry = datetime.now() + timedelta(hours=1)

        accounts = (
            db.query(SocialAccount)
            .filter(
                SocialAccount.token_expires_at != None,
                SocialAccount.token_expires_at <= expiry,
                SocialAccount.is_active == True,
            )
            .all()
        )

        logger.info(
            f"[TOKEN REFRESH] Found {len(accounts)} " f"account(s) requiring refresh"
        )

        for account in accounts:

            try:

                logger.info(
                    f"[TOKEN REFRESH] Refreshing "
                    f"{account.platform} account {account.id}"
                )

                # ----------------------------------------------
                # Supported platforms
                # ----------------------------------------------

                if account.platform.lower() not in ["linkedin", "x", "youtube"]:

                    logger.warning(
                        f"[TOKEN REFRESH] Unsupported platform: " f"{account.platform}"
                    )

                    continue

                # ----------------------------------------------
                # Check refresh token
                # ----------------------------------------------

                if not account.refresh_token:

                    logger.warning(
                        f"[TOKEN REFRESH] Account {account.id} " f"has no refresh token"
                    )

                    NotificationService(db).create_notification(
                        user_id=account.user_id,
                        title="Account Reconnection Required",
                        description=(
                            f"Your {account.platform} connection needs to be "
                            f"reconnected because no refresh token is available."
                        ),
                        category="account_activity",
                        notification_type="reauthorization_required",
                    )

                    continue

                # ----------------------------------------------
                # Use SocialIntegrationService
                # ----------------------------------------------

                from app.services.social_integration import (
                    SocialIntegrationService,
                )

                service = SocialIntegrationService(db)

                token_data = service.refresh_token(
                    platform=account.platform,
                    refresh_token=account.refresh_token,
                )

                new_access_token = token_data.get("access_token")
                new_refresh_token = token_data.get("refresh_token")
                new_expiry = token_data.get("expiry")

                if not new_access_token:

                    raise Exception(
                        f"No new access token returned from {account.platform}"
                    )

                account.access_token = encrypt_token(new_access_token)

                if new_refresh_token:

                    account.refresh_token = encrypt_token(new_refresh_token)

                if new_expiry:

                    account.token_expires_at = new_expiry

                account.is_active = True
                account.is_connected = True

                db.commit()

                logger.info(
                    f"[TOKEN REFRESH] Successfully refreshed " f"account {account.id}"
                )

                NotificationService(db).create_notification(
                    user_id=account.user_id,
                    title="Account Reconnected",
                    description=(
                        f"Your {account.platform} connection was refreshed successfully."
                    ),
                    category="account_activity",
                    notification_type="token_refreshed",
                )

            except Exception as e:

                db.rollback()

                logger.error(
                    f"[TOKEN REFRESH] Failed for account " f"{account.id}: {e}"
                )

                try:

                    NotificationService(db).create_notification(
                        user_id=account.user_id,
                        title="Reconnection Failed",
                        description=(
                            f"Your {account.platform} connection could not be "
                            f"refreshed automatically. Please reconnect your account."
                        ),
                        category="account_activity",
                        notification_type="token_expired",
                    )

                except Exception as notification_error:

                    db.rollback()

                    logger.error(
                        f"[TOKEN REFRESH] Failed to create "
                        f"notification: {notification_error}"
                    )

    except Exception as e:

        logger.error(f"[TOKEN REFRESH] ERROR {e}")

        db.rollback()

        raise

    finally:

        db.close()
