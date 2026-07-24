from celery import Celery

app = Celery(
    "socialpilot",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=["app.services.tasks"],
)


# Timezone

app.conf.timezone = "Asia/Kolkata"


# Celery Beat schedules

app.conf.beat_schedule = {
    # --------------------------------
    # Check scheduled posts
    # Every 60 seconds
    # --------------------------------
    "check-queue-every-minute": {
        "task": "app.services.tasks.check_and_publish",
        "schedule": 60.0,
    },
    # --------------------------------
    # Refresh social media tokens
    # Every 30 minutes
    # --------------------------------
    "refresh-tokens-every-30-minutes": {
        "task": "app.services.tasks.refresh_expiring_tokens",
        "schedule": 1800.0,
    },
    # --------------------------------
    # Process recurring posts
    # Every 5 minutes
    # --------------------------------
    "process-recurring-posts": {
        "task": "app.services.tasks.process_recurring_posts",
        "schedule": 300.0,
    },
}
