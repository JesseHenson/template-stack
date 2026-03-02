# Stripe — Payments + Subscriptions

## Dependencies
```bash
cd backend && uv add stripe
```

## Doppler Secrets
- `STRIPE_SECRET_KEY` — Stripe secret key
- `STRIPE_WEBHOOK_SECRET` — Stripe webhook signing secret
- `STRIPE_PRICE_ID` — Default price ID for subscriptions
- `VITE_STRIPE_PUBLISHABLE_KEY` — Stripe publishable key for frontend

## Config Fields
Add to `backend/app/config.py`:
```python
# Stripe
stripe_secret_key: str = ""
stripe_webhook_secret: str = ""
stripe_price_id: str = ""
```

## Files to Create

### `backend/app/services/stripe_client.py`
```python
"""Stripe payment client."""

import stripe

from app.config import settings


def init_stripe():
    """Initialize Stripe with API key."""
    stripe.api_key = settings.stripe_secret_key


def create_checkout_session(
    customer_email: str,
    price_id: str | None = None,
    success_url: str = "/dashboard?checkout=success",
    cancel_url: str = "/dashboard?checkout=cancel",
) -> stripe.checkout.Session:
    """Create a Stripe Checkout session."""
    return stripe.checkout.Session.create(
        mode="subscription",
        customer_email=customer_email,
        line_items=[{"price": price_id or settings.stripe_price_id, "quantity": 1}],
        success_url=success_url,
        cancel_url=cancel_url,
    )


def create_portal_session(customer_id: str) -> stripe.billing_portal.Session:
    """Create a Stripe Customer Portal session."""
    return stripe.billing_portal.Session.create(
        customer=customer_id,
        return_url="/dashboard",
    )
```

### `backend/app/api/stripe.py`
```python
"""Stripe API endpoints."""

import stripe
from fastapi import APIRouter, HTTPException, Request

from app.auth.middleware import CurrentUserId
from app.config import settings
from app.services.stripe_client import create_checkout_session
from app.services.supabase_client import get_supabase_client

router = APIRouter()


@router.post("/create-checkout")
async def create_checkout(clerk_id: CurrentUserId):
    """Create a Stripe Checkout session for the current user."""
    db = get_supabase_client()
    user = db.table("users").select("email").eq("clerk_id", clerk_id).execute()
    if not user.data:
        raise HTTPException(status_code=404, detail="User not found")

    session = create_checkout_session(customer_email=user.data[0]["email"])
    return {"url": session.url}


@router.post("/webhook")
async def stripe_webhook(request: Request):
    """Handle Stripe webhook events."""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.stripe_webhook_secret
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        raise HTTPException(status_code=400, detail="Invalid webhook")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        customer_email = session.get("customer_email")
        customer_id = session.get("customer")
        subscription_id = session.get("subscription")

        db = get_supabase_client()
        db.table("users").update({
            "stripe_customer_id": customer_id,
            "stripe_subscription_id": subscription_id,
            "subscription_status": "active",
        }).eq("email", customer_email).execute()

    elif event["type"] == "customer.subscription.deleted":
        subscription = event["data"]["object"]
        customer_id = subscription.get("customer")

        db = get_supabase_client()
        db.table("users").update({
            "subscription_status": "cancelled",
        }).eq("stripe_customer_id", customer_id).execute()

    return {"status": "ok"}
```

## Wiring Changes

### Backend — `backend/app/main.py`
Add to lifespan startup:
```python
from app.services.stripe_client import init_stripe
init_stripe()
```

### Backend — `backend/app/api/router.py`
```python
from app.api.stripe import router as stripe_router
api_router.include_router(stripe_router, prefix="/stripe", tags=["stripe"])
```

## Migration SQL
```sql
alter table users add column if not exists stripe_customer_id text;
alter table users add column if not exists stripe_subscription_id text;
alter table users add column if not exists subscription_status text not null default 'free';
```
