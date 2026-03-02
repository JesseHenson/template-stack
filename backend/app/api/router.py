"""Central API router."""

from fastapi import APIRouter

from app.api.health import router as health_router
from app.api.items import router as items_router
from app.api.webhooks import router as webhooks_router

api_router = APIRouter()

api_router.include_router(health_router, tags=["health"])
api_router.include_router(items_router, prefix="/items", tags=["items"])
api_router.include_router(webhooks_router, prefix="/webhooks", tags=["webhooks"])
