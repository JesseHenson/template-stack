"""Application configuration via pydantic-settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # --- App ---
    debug: bool = False
    cors_origins: str = "http://localhost:5173"

    # --- Database ---
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/template_stack"

    @property
    def database_url_sync(self) -> str:
        """Sync URL for Alembic (strips +asyncpg)."""
        return self.database_url.replace("+asyncpg", "")

    # --- Clerk ---
    clerk_secret_key: str = ""
    clerk_publishable_key: str = ""
    clerk_webhook_secret: str = ""

    # --- Anthropic ---
    anthropic_api_key: str = ""

    # --- LiteLLM ---
    litellm_api_key: str = ""
    litellm_api_base: str = ""

    # --- Inngest ---
    inngest_event_key: str = ""
    inngest_signing_key: str = ""

    # --- Redis (Upstash) ---
    upstash_redis_url: str = ""
    upstash_redis_token: str = ""

    # --- Sentry ---
    sentry_dsn: str = ""

    # --- LangSmith ---
    langsmith_api_key: str = ""
    langsmith_project: str = ""


settings = Settings()
