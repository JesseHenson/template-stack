"""FastAPI application entry point."""

import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.utils.sentry import init_sentry

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan — init services on startup, cleanup on shutdown."""
    init_sentry()

    from app.services.litellm_client import init_litellm
    init_litellm()

    # Seed dev user when Clerk is not configured
    if not settings.clerk_secret_key:
        from sqlalchemy.dialects.postgresql import insert as pg_insert

        from app.auth.middleware import DEV_CLERK_ID
        from app.db.models import User
        from app.db.session import async_session_factory

        async with async_session_factory() as session:
            stmt = pg_insert(User).values(
                clerk_id=DEV_CLERK_ID,
                email="dev@localhost",
                name="Dev User",
            ).on_conflict_do_nothing(index_elements=["clerk_id"])
            await session.execute(stmt)
            await session.commit()
        logger.info("Dev user seeded (clerk_id=%s)", DEV_CLERK_ID)

    logger.info("Application started")
    yield

    # Dispose engine on shutdown
    from app.db.session import engine

    await engine.dispose()
    logger.info("Application shutting down")


app = FastAPI(
    title="Template Stack API",
    lifespan=lifespan,
    docs_url="/api/docs" if settings.debug else None,
    redoc_url=None,
)

# CORS
origins = [o.strip() for o in settings.cors_origins.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
from app.api.router import api_router  # noqa: E402

app.include_router(api_router, prefix="/api/v1")

# Inngest
try:
    import inngest.fast_api

    from app.inngest.client import inngest_client
    from app.inngest.functions import inngest_functions

    inngest.fast_api.serve(app, inngest_client, inngest_functions)
except Exception:
    logger.info("Inngest not configured, skipping")

# Serve frontend static files in production
static_dir = Path(__file__).parent.parent / "static"
if static_dir.is_dir():
    app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")
