"""Clerk webhook handler for user sync."""

import logging

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import delete
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db.models import User
from app.db.session import get_db

logger = logging.getLogger(__name__)

router = APIRouter()


def _verify_webhook(headers: dict, body: bytes) -> None:
    """Verify Clerk webhook signature via svix. Skips when secret is empty (local dev)."""
    if not settings.clerk_webhook_secret:
        return

    from svix.webhooks import Webhook, WebhookVerificationError

    try:
        wh = Webhook(settings.clerk_webhook_secret)
        wh.verify(body, headers)
    except WebhookVerificationError:
        raise HTTPException(status_code=400, detail="Invalid webhook signature")


@router.post("/clerk")
async def clerk_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    """Handle Clerk webhook events to sync users to the database."""
    body = await request.body()
    _verify_webhook(
        {
            "svix-id": request.headers.get("svix-id", ""),
            "svix-timestamp": request.headers.get("svix-timestamp", ""),
            "svix-signature": request.headers.get("svix-signature", ""),
        },
        body,
    )

    import json

    payload = json.loads(body)
    event_type = payload.get("type")
    data = payload.get("data", {})

    if event_type in ("user.created", "user.updated"):
        clerk_id = data.get("id")
        email = ""
        if data.get("email_addresses"):
            primary_id = data.get("primary_email_address_id")
            for ea in data["email_addresses"]:
                if ea["id"] == primary_id:
                    email = ea["email_address"]
                    break
            if not email:
                email = data["email_addresses"][0]["email_address"]

        name = f"{data.get('first_name', '') or ''} {data.get('last_name', '') or ''}".strip()
        if not name:
            name = email.split("@")[0] if email else "User"

        avatar_url = data.get("image_url")

        stmt = pg_insert(User).values(
            clerk_id=clerk_id,
            email=email,
            name=name,
            avatar_url=avatar_url,
        )
        stmt = stmt.on_conflict_do_update(
            index_elements=["clerk_id"],
            set_={"email": email, "name": name, "avatar_url": avatar_url},
        )
        await db.execute(stmt)
        logger.info("Synced user %s (%s)", clerk_id, email)

    elif event_type == "user.deleted":
        clerk_id = data.get("id")
        if clerk_id:
            await db.execute(delete(User).where(User.clerk_id == clerk_id))
            logger.info("Deleted user %s", clerk_id)

    return {"status": "ok"}
