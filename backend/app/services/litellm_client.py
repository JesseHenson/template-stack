"""LiteLLM client with LangSmith callback integration."""

import litellm

from app.config import settings


def init_litellm():
    """Configure LiteLLM with API keys and callbacks."""
    if settings.litellm_api_key:
        litellm.api_key = settings.litellm_api_key
    if settings.litellm_api_base:
        litellm.api_base = settings.litellm_api_base

    # Enable LangSmith tracing if configured
    if settings.langsmith_api_key:
        litellm.success_callback = ["langsmith"]
        litellm.failure_callback = ["langsmith"]


async def completion(model: str, messages: list[dict], **kwargs) -> dict:
    """Call LiteLLM completion with configured defaults."""
    response = await litellm.acompletion(model=model, messages=messages, **kwargs)
    return response
