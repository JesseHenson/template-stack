# PostHog — Feature Flags + Analytics

## Dependencies
```bash
cd backend && uv add posthog
cd frontend && npm install posthog-js
```

## Doppler Secrets
- `POSTHOG_API_KEY` — PostHog project API key
- `POSTHOG_HOST` — PostHog instance URL (default: `https://app.posthog.com`)
- `VITE_POSTHOG_KEY` — Same API key for frontend
- `VITE_POSTHOG_HOST` — Same host for frontend

## Config Fields
Add to `backend/app/config.py`:
```python
# PostHog
posthog_api_key: str = ""
posthog_host: str = "https://app.posthog.com"
```

## Files to Create

### `backend/app/services/posthog_client.py`
```python
"""PostHog analytics and feature flags."""

import posthog

from app.config import settings


def init_posthog():
    """Initialize PostHog SDK."""
    if settings.posthog_api_key:
        posthog.project_api_key = settings.posthog_api_key
        posthog.host = settings.posthog_host


def capture_event(distinct_id: str, event: str, properties: dict | None = None):
    """Track an analytics event."""
    posthog.capture(distinct_id, event, properties or {})


def is_feature_enabled(flag: str, distinct_id: str) -> bool:
    """Check if a feature flag is enabled for a user."""
    return posthog.feature_enabled(flag, distinct_id)
```

### `frontend/src/lib/posthog.ts`
```typescript
import posthog from "posthog-js";

export function initPostHog() {
  const key = import.meta.env.VITE_POSTHOG_KEY;
  const host = import.meta.env.VITE_POSTHOG_HOST || "https://app.posthog.com";

  if (key) {
    posthog.init(key, {
      api_host: host,
      capture_pageview: true,
      capture_pageleave: true,
    });
  }
}

export { posthog };
```

## Wiring Changes

### Backend — `backend/app/main.py`
Add to lifespan startup:
```python
from app.services.posthog_client import init_posthog
init_posthog()
```

### Frontend — `frontend/src/main.tsx`
Add before `createRoot`:
```typescript
import { initPostHog } from "@/lib/posthog";
initPostHog();
```

## Migration SQL
No migration needed.
