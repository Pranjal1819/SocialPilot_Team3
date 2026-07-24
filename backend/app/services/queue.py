import time
import logging

from datetime import datetime

from app.services.redis_client import get_redis

# --------------------------------------------------
# Logger Configuration
# --------------------------------------------------

logger = logging.getLogger("queue_manager")

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
)


# Redis connection

r = get_redis()


# --------------------------------------------------
# Add post to publishing queue
# --------------------------------------------------


def add_to_queue(post_id: int, scheduled_timestamp: float):

    try:

        r.zadd("post_queue", {str(post_id): scheduled_timestamp})

        logger.info(
            f"[QUEUE] Post {post_id} added | " f"Scheduled time: {scheduled_timestamp}"
        )

    except Exception as e:

        logger.error(f"[QUEUE ERROR] Failed adding post {post_id}: {e}")

        raise e


# --------------------------------------------------
# Get posts ready for publishing
# --------------------------------------------------


def get_due_posts():

    try:

        current_time = time.time()

        posts = r.zrangebyscore("post_queue", 0, current_time)

        logger.info(f"[QUEUE CHECK] Found {len(posts)} due posts")

        return posts

    except Exception as e:

        logger.error(f"[QUEUE ERROR] Fetching due posts failed: {e}")

        return []


# --------------------------------------------------
# Remove published post from queue
# --------------------------------------------------


def remove_from_queue(post_id: int):

    try:

        r.zrem("post_queue", str(post_id))

        logger.info(f"[QUEUE] Post {post_id} removed from queue")

    except Exception as e:

        logger.error(f"[QUEUE ERROR] Removing post {post_id}: {e}")


# --------------------------------------------------
# Update Redis status
# --------------------------------------------------


def update_status(post_id: int, status: str):

    try:

        r.hset("post_status", str(post_id), status)

        logger.info(f"[STATUS] Post {post_id} -> {status}")

    except Exception as e:

        logger.error(f"[STATUS ERROR] Updating post {post_id}: {e}")


# --------------------------------------------------
# Get Redis status
# --------------------------------------------------


def get_status(post_id: int):

    try:

        status = r.hget("post_status", str(post_id))

        if status:

            return status.decode("utf-8")

        return None

    except Exception as e:

        logger.error(f"[STATUS ERROR] Reading post {post_id}: {e}")

        return None


# --------------------------------------------------
# Queue monitoring
# --------------------------------------------------


def queue_length():

    try:

        count = r.zcard("post_queue")

        logger.info(f"[QUEUE MONITOR] Pending posts: {count}")

        return count

    except Exception as e:

        logger.error(f"[QUEUE ERROR] Checking queue length: {e}")

        return 0


# --------------------------------------------------
# View pending queue items
# --------------------------------------------------


def get_pending_posts():

    try:

        posts = r.zrange("post_queue", 0, -1, withscores=True)

        result = []

        for post_id, timestamp in posts:

            result.append(
                {
                    "post_id": int(post_id),
                    "scheduled_time": datetime.fromtimestamp(timestamp),
                }
            )

        return result

    except Exception as e:

        logger.error(f"[QUEUE ERROR] Getting pending posts: {e}")

        return []


# --------------------------------------------------
# Clear Redis status after completion
# --------------------------------------------------


def clear_status(post_id: int):

    try:

        r.hdel("post_status", str(post_id))

        logger.info(f"[STATUS CLEANUP] Removed status for post {post_id}")

    except Exception as e:

        logger.error(f"[STATUS ERROR] Clearing post {post_id}: {e}")
