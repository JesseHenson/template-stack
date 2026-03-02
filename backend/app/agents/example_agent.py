"""Example Claude SDK agent — replace with your product's agents."""

import anthropic

from app.config import settings

client = anthropic.Anthropic(api_key=settings.anthropic_api_key)


async def run_agent(prompt: str, system: str = "") -> str:
    """Run a simple Claude completion."""
    messages = [{"role": "user", "content": prompt}]

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=4096,
        system=system or "You are a helpful assistant.",
        messages=messages,
    )

    return response.content[0].text
