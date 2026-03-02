"""Upstash Redis client singleton."""

from upstash_redis import Redis

from app.config import settings

_client: Redis | None = None


def get_redis_client() -> Redis:
    """Return a singleton Upstash Redis client."""
    global _client
    if _client is None:
        _client = Redis(url=settings.upstash_redis_url, token=settings.upstash_redis_token)
    return _client
