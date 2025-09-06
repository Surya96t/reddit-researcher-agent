"""
Reddit API client configuration.
"""
import praw
from app.core.config import settings


# Initialize the Reddit API client
reddit_client = praw.Reddit(
    client_id=settings.REDDIT_CLIENT_ID.get_secret_value(),
    client_secret=settings.REDDIT_CLIENT_SECRET.get_secret_value(),
    user_agent=settings.REDDIT_USER_AGENT,
    check_for_async=False  # Important for use in our sync Celery task
)
