# Ayrshare — Social Media API

## Dependencies
```bash
cd backend && uv add httpx
```
(Ayrshare uses a REST API — no dedicated SDK needed, use httpx)

## Doppler Secrets
- `AYRSHARE_API_KEY` — Ayrshare API key

## Config Fields
Add to `backend/app/config.py`:
```python
# Ayrshare
ayrshare_api_key: str = ""
```

## Files to Create

### `backend/app/services/ayrshare_client.py`
```python
"""Ayrshare social media API client."""

import httpx

from app.config import settings

AYRSHARE_BASE_URL = "https://app.ayrshare.com/api"


def _headers() -> dict:
    return {
        "Authorization": f"Bearer {settings.ayrshare_api_key}",
        "Content-Type": "application/json",
    }


async def post_to_social(
    post: str,
    platforms: list[str],
    media_urls: list[str] | None = None,
) -> dict:
    """Post content to social media platforms."""
    payload = {
        "post": post,
        "platforms": platforms,
    }
    if media_urls:
        payload["mediaUrls"] = media_urls

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{AYRSHARE_BASE_URL}/post",
            json=payload,
            headers=_headers(),
        )
        response.raise_for_status()
        return response.json()


async def get_post_history(platform: str | None = None) -> dict:
    """Get post history, optionally filtered by platform."""
    params = {}
    if platform:
        params["platform"] = platform

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{AYRSHARE_BASE_URL}/history",
            params=params,
            headers=_headers(),
        )
        response.raise_for_status()
        return response.json()


async def delete_post(post_id: str) -> dict:
    """Delete a social media post."""
    async with httpx.AsyncClient() as client:
        response = await client.delete(
            f"{AYRSHARE_BASE_URL}/post/{post_id}",
            headers=_headers(),
        )
        response.raise_for_status()
        return response.json()
```

## Wiring Changes
No changes to main.py needed — import the client where you use it in services or routes.

## Migration SQL
No migration needed. If you need to track post history locally, add a table:
```sql
create table social_posts (
    id uuid primary key default uuid_generate_v4(),
    user_id uuid not null references users(id) on delete cascade,
    ayrshare_id text,
    content text not null,
    platforms text[] not null,
    status text not null default 'posted',
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create index idx_social_posts_user_id on social_posts(user_id);

create trigger social_posts_updated_at
    before update on social_posts
    for each row execute function update_updated_at();
```
