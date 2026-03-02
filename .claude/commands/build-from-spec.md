# Build From Spec

Read SPEC.md and scaffold the full application from the template stack.

## Steps

1. Read SPEC.md from the project root
2. Parse the data model section and generate:
   - Supabase migration SQL in `supabase/migrations/` (following foundation.sql patterns)
   - Pydantic models in `backend/app/models/` (Create, Update, Response for each entity)
   - CRUD services in `backend/app/services/` (using clerk_id → user_id ownership pattern)
   - API routes in `backend/app/api/` (with CurrentUserId dependency)
   - Wire new routers into `backend/app/api/router.py`
3. Parse the pages & components section and generate:
   - TypeScript types in `frontend/src/types/index.ts`
   - TanStack Query hooks in `frontend/src/hooks/`
   - Page components in `frontend/src/pages/`
   - Layout/UI components in `frontend/src/components/`
   - Update routes in `frontend/src/App.tsx`
   - Update sidebar links in `frontend/src/components/layout/Sidebar.tsx`
4. Parse optional layers and run the appropriate drop-in guides from `.claude/skills/optional-layers/`
5. Remove example item files (items.py, item.py, item_service.py, useItems.ts) since real models replace them
6. Update CLAUDE.md with product-specific details

## Conventions
- Follow existing patterns exactly (see CLAUDE.md)
- Tables: uuid PK, created_at, updated_at, user_id FK with cascade
- Services: get_user_id_from_clerk_id() ownership pattern
- Frontend: one hook file per resource, one page per route
