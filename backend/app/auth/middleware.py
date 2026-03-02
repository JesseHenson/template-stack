"""FastAPI dependencies for Clerk JWT auth."""

import logging
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config import settings

logger = logging.getLogger(__name__)

DEV_CLERK_ID = "dev_local_user"

security = HTTPBearer(auto_error=False)


def get_current_user_id(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
) -> str:
    """Extract and verify the clerk_user_id from the JWT Bearer token.

    When clerk_secret_key is empty (local dev), returns a dev user ID.
    """
    if not settings.clerk_secret_key:
        return DEV_CLERK_ID

    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    from app.auth.clerk_auth import verify_clerk_token

    token = credentials.credentials
    payload = verify_clerk_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    clerk_id = payload.get("sub")
    if not clerk_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: no subject",
        )

    return clerk_id


CurrentUserId = Annotated[str, Depends(get_current_user_id)]
