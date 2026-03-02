"""Inngest client configuration."""

import inngest

from app.config import settings

inngest_client = inngest.Inngest(
    app_id="template-stack",
    event_key=settings.inngest_event_key,
    signing_key=settings.inngest_signing_key,
)
