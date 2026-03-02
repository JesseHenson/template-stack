# Add Optional Layer

Add an optional technology layer to the project.

## Usage
Specify the layer name as an argument: $ARGUMENTS

Available layers: qdrant, falkordb, fastmcp, posthog, ayrshare, resend, stripe, nextjs, supabase-storage, litellm-gateway

## Steps

1. Read the corresponding guide from `.claude/skills/optional-layers/{layer}.md`
2. Follow the guide step by step:
   - Add dependencies (uv add / npm install)
   - Add config fields to `backend/app/config.py`
   - Create new service/client files
   - Wire into existing code (main.py, router.py, etc.)
   - Add migration SQL if needed
3. Update `.env.example` with new env vars
4. Update CLAUDE.md with the new layer details
