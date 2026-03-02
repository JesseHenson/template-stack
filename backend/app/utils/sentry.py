"""Sentry initialization."""

import logging

import sentry_sdk

from app.config import settings

logger = logging.getLogger(__name__)


def init_sentry():
    """Initialize Sentry SDK if DSN is configured."""
    if not settings.sentry_dsn:
        logger.info("Sentry DSN not set, skipping initialization")
        return

    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        send_default_pii=True,
        traces_sample_rate=0.1,
        profiles_sample_rate=0.1,
    )
    logger.info("Sentry initialized")
