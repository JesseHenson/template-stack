# Template Stack Conventions

## Naming Rules

### Backend
- **Files**: snake_case (e.g., `item_service.py`, `clerk_auth.py`)
- **Classes**: PascalCase (e.g., `ItemCreate`, `ItemResponse`)
- **Functions**: snake_case (e.g., `get_user_id_from_clerk_id`)
- **Variables**: snake_case
- **Routes**: kebab-case in URLs, snake_case in Python (e.g., `/api/v1/items`, `list_items`)
- **Models**: `{Resource}Create`, `{Resource}Update`, `{Resource}Response`
- **Services**: `{resource}_service.py` with functions like `list_{resources}`, `get_{resource}`, `create_{resource}`

### Frontend
- **Files**: PascalCase for components (e.g., `DashboardPage.tsx`), camelCase for utilities (e.g., `queryClient.ts`)
- **Hooks**: `use{Resources}.ts` (e.g., `useItems.ts`)
- **Types**: PascalCase interfaces (e.g., `Item`, `ItemCreate`)
- **Components**: PascalCase (e.g., `AppShell`, `Sidebar`)
- **Pages**: `{Resource}Page.tsx` or `{Action}Page.tsx`

### Database
- **Tables**: snake_case, plural (e.g., `items`, `users`)
- **Columns**: snake_case (e.g., `user_id`, `created_at`)
- **Indexes**: `idx_{table}_{column}` (e.g., `idx_items_user_id`)
- **Triggers**: `{table}_updated_at`

## File Patterns

### Adding a New Resource
1. **Migration**: `supabase/migrations/{timestamp}_{description}.sql`
2. **Model**: `backend/app/models/{resource}.py` — Create, Update, Response
3. **Service**: `backend/app/services/{resource}_service.py` — CRUD with ownership
4. **Route**: `backend/app/api/{resource}s.py` — REST endpoints
5. **Router**: Wire in `backend/app/api/router.py`
6. **Types**: Add to `frontend/src/types/index.ts`
7. **Hook**: `frontend/src/hooks/use{Resources}.ts`
8. **Page**: `frontend/src/pages/{Resource}Page.tsx`
9. **Routes**: Add to `frontend/src/App.tsx`
10. **Sidebar**: Add link in `frontend/src/components/layout/Sidebar.tsx`

## Code Conventions

### Backend
- All config via pydantic-settings in `app/config.py`
- All DB access via `get_supabase_client()` singleton
- Auth via `CurrentUserId` dependency (returns clerk_id string)
- Services map clerk_id → user_id via `get_user_id_from_clerk_id()`
- Services enforce ownership on all read/write operations
- Use `model_dump(exclude_none=True)` for partial updates

### Frontend
- Provider order: StrictMode > ClerkProvider > QueryClientProvider > App
- AuthSetup bridges Clerk token to axios interceptor
- All API calls via `api` from `@/api/client`
- TanStack Query for server state (30s stale time)
- Pages wrapped in `<AppShell>` for consistent layout
- Tailwind: gray-50 backgrounds, white cards, gray-200 borders
- `cn()` helper for conditional class merging

### Infrastructure
- uv for Python package management (never pip)
- npm for frontend (not yarn or pnpm)
- Docker multi-stage: Node build → Python serve
- All secrets via environment variables (Doppler in prod)
- CI: lint-frontend → test-backend → deploy (on main only)
