"""Example Inngest async functions — replace with your product's background jobs."""

import logging

import inngest

from app.inngest.client import inngest_client

logger = logging.getLogger(__name__)


@inngest_client.create_function(
    fn_id="example-background-job",
    trigger=inngest.TriggerEvent(event="app/example.requested"),
)
async def example_background_job(ctx: inngest.Context, step: inngest.Step) -> str:
    """Example async function triggered by an event."""
    event_data = ctx.event.data

    result = await step.run("process-data", lambda: f"Processed: {event_data}")

    logger.info("Background job completed: %s", result)
    return result


# Export all functions for registration
inngest_functions = [example_background_job]
