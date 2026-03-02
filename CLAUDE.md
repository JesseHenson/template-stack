# Template Stack

Full-stack monorepo: FastAPI + React SPA + Clerk + Neon/Postgres + GCP Cloud Run.

## Stack

- **Backend**: FastAPI, SQLAlchemy (async), Alembic, pydantic-settings, PyJWT (Clerk JWKS)
- **Frontend**: React 19, Vite, Tailwind v4, Clerk React, TanStack Query, Axios
- **Database**: Neon (production) / Docker Postgres (local) — direct SQL via SQLAlchemy + asyncpg
- **Auth**: Clerk (frontend SDK + backend JWT verification). Optional for local dev — leave Clerk keys empty and a dev user is auto-seeded.
- **Deploy**: Docker multi-stage → GCP Cloud Run
- **Package management**: uv (backend), npm (frontend)

## Local Dev (Traefik)

Everything runs via `docker compose up -d` — backend, frontend, postgres, redis, inngest. Traefik routes subdomains automatically.

| URL | Service |
|-----|---------|
| `template-stack.localhost` | Frontend (Vite HMR) |
| `api.template-stack.localhost` | Backend (FastAPI reload) |
| `inngest.template-stack.localhost` | Inngest dev UI |

```bash
# Start everything
docker compose up -d

# Restart backend only
docker compose restart backend

# Rebuild after dependency changes
docker compose up -d --build backend

# View logs
docker compose logs -f backend
docker compose logs -f frontend

# Stop
docker compose down

# Tests
docker compose exec backend uv run pytest -v
```

Source is volume-mounted — edit files locally, hot reload works automatically.
Backend command runs `alembic upgrade head` before starting uvicorn.

### Host-native fallback

If you prefer running outside Docker, start Traefik + infra only, then run natively:
```bash
docker compose up -d postgres redis inngest
cd backend && uv run alembic upgrade head
cd backend && uv run uvicorn app.main:app --reload --port 8001
cd frontend && npm run dev
```

## Conventions

- Backend CRUD services use `clerk_id → user_id` ownership pattern
- All tables have `id uuid`, `created_at`, `updated_at` columns
- SQLAlchemy models in `app/db/models.py`, Pydantic schemas in `app/models/`
- Frontend hooks go in `src/hooks/`, pages in `src/pages/`
- API client auto-attaches Clerk JWT via interceptor
- Pydantic models: `*Create` (input), `*Update` (partial), `*Response` (output with `from_attributes=True`)
- Config: all secrets in `app/config.py` via pydantic-settings
- Migrations: Alembic in `backend/alembic/` — `uv run alembic revision --autogenerate -m "description"`

## Auth Flow

1. Frontend: Clerk `<SignedIn>` guard + `useAuth().getToken` → axios interceptor
2. Backend: `CurrentUserId` dependency extracts `clerk_id` from JWT
3. When `CLERK_SECRET_KEY` is empty (local dev): returns `dev_local_user` clerk_id, dev user auto-seeded on startup
4. Services: `get_user_id_from_clerk_id()` maps to internal UUID
5. Clerk webhook syncs users to `users` table on create/update/delete
