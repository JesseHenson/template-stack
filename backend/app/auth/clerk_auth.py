"""Verify Clerk-issued JWTs using JWKS public keys."""

import base64
import logging

import jwt as pyjwt
from jwt import PyJWKClient

from app.config import settings

logger = logging.getLogger(__name__)

_jwks_client: PyJWKClient | None = None


def _get_jwks_client() -> PyJWKClient:
    global _jwks_client
    if _jwks_client is None:
        # Derive Clerk Frontend API URL from publishable key
        key_part = settings.clerk_publishable_key.split("_", 2)[-1]
        padded = key_part + "=" * (4 - len(key_part) % 4)
        domain = base64.b64decode(padded).decode().rstrip("$")
        jwks_url = f"https://{domain}/.well-known/jwks.json"
        logger.info("Clerk JWKS URL: %s", jwks_url)
        _jwks_client = PyJWKClient(jwks_url, cache_keys=True)
    return _jwks_client


def verify_clerk_token(token: str) -> dict | None:
    """Verify a Clerk JWT and return the decoded payload, or None on failure."""
    try:
        client = _get_jwks_client()
        signing_key = client.get_signing_key_from_jwt(token)
        payload = pyjwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            options={"verify_aud": False},
        )
        return payload
    except Exception as e:
        logger.error("Clerk token verification failed: %s", e)
        return None
