# app/services/publishing.py

from datetime import datetime
from sqlalchemy.orm import Session

from app.models.scheduled_post import ScheduledPost


class PublishingService:
    """
    Handles publishing scheduled posts.

    Currently:
    - Updates publishing status
    - Simulates successful publishing

    Later:
    - Add LinkedIn API
    - Add Instagram API
    - Add Facebook API
    """


    def __init__(self, db: Session):
        self.db = db



    def publish_post(self, post_id: int):
        """
        Publish a scheduled post.

        Args:
            post_id: ID of ScheduledPost

        Returns:
            True if published successfully
            False if failed
        """


        # Fetch post from database

        post = (
            self.db.query(ScheduledPost)
            .filter(
                ScheduledPost.id == post_id
            )
            .first()
        )


        if not post:
            return False



        try:

            # ----------------------------------
            # Publishing Logic
            # ----------------------------------
            #
            # Currently simulated.
            #
            # Later:
            #
            # if post.platform == "linkedin":
            #       LinkedIn API call
            #
            # if post.platform == "instagram":
            #       Instagram API call
            #
            # ----------------------------------


            print(
                f"Publishing post {post.id} to {post.platform}"
            )


            # Update status

            post.status = "published"

            post.published_at = datetime.now()


            # Remove failure message if retry succeeds

            post.failure_reason = None



            self.db.commit()

            self.db.refresh(post)


            return True



        except Exception as e:


            # If publishing fails

            post.status = "failed"

            post.failure_reason = str(e)


            self.db.commit()


            return False