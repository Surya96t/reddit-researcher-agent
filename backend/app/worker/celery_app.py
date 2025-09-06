from celery import Celery
from app.core.config import settings

# The Celery app instance is now configured directly from the settings object
celery = Celery(
    "tasks",
    broker=str(settings.REDIS_URL),
    backend=str(settings.REDIS_URL),
    include=["app.worker.tasks"]
)

# Optional: Add any other configurations here if needed
celery.conf.update(
    task_track_started=True,
)