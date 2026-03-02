# Resend — Transactional Email

## Dependencies
```bash
cd backend && uv add resend
```

## Doppler Secrets
- `RESEND_API_KEY` — Resend API key
- `RESEND_FROM_EMAIL` — Verified sender email (e.g., `noreply@yourdomain.com`)

## Config Fields
Add to `backend/app/config.py`:
```python
# Resend
resend_api_key: str = ""
resend_from_email: str = ""
```

## Files to Create

### `backend/app/services/email_client.py`
```python
"""Resend email client."""

import resend

from app.config import settings


def init_resend():
    """Initialize Resend with API key."""
    resend.api_key = settings.resend_api_key


def send_email(
    to: str | list[str],
    subject: str,
    html: str,
    from_email: str | None = None,
) -> dict:
    """Send a transactional email."""
    params = {
        "from": from_email or settings.resend_from_email,
        "to": to if isinstance(to, list) else [to],
        "subject": subject,
        "html": html,
    }
    return resend.Emails.send(params)


def send_welcome_email(to: str, name: str) -> dict:
    """Send a welcome email to a new user."""
    return send_email(
        to=to,
        subject="Welcome!",
        html=f"<h1>Welcome, {name}!</h1><p>Thanks for signing up.</p>",
    )
```

## Wiring Changes

### Backend — `backend/app/main.py`
Add to lifespan startup:
```python
from app.services.email_client import init_resend
init_resend()
```

### Webhook integration (optional)
In `backend/app/api/webhooks.py`, after user creation:
```python
from app.services.email_client import send_welcome_email
send_welcome_email(to=email, name=name)
```

## Migration SQL
No migration needed.
