# FastMCP — MCP Server for Agent Tools

## Dependencies
```bash
cd backend && uv add fastmcp
```

## Doppler Secrets
None required — MCP servers are typically accessed locally or via stdio.

## Config Fields
No additional config fields needed.

## Files to Create

### `backend/app/mcp/__init__.py`
Empty file.

### `backend/app/mcp/server.py`
```python
"""MCP server exposing application tools to AI agents."""

from fastmcp import FastMCP

from app.services.supabase_client import get_supabase_client

mcp = FastMCP("template-stack")


@mcp.tool()
def list_items(user_id: str) -> list[dict]:
    """List all items for a user."""
    db = get_supabase_client()
    result = db.table("items").select("*").eq("user_id", user_id).execute()
    return result.data


@mcp.tool()
def search_items(query: str, user_id: str) -> list[dict]:
    """Search items by name for a user."""
    db = get_supabase_client()
    result = (
        db.table("items")
        .select("*")
        .eq("user_id", user_id)
        .ilike("name", f"%{query}%")
        .execute()
    )
    return result.data
```

## Wiring Changes
Add to `backend/app/main.py` if serving MCP over SSE:
```python
# MCP server (optional — for SSE transport)
try:
    from app.mcp.server import mcp
    mcp.mount(app, prefix="/mcp")
except Exception:
    logger.info("MCP server not configured, skipping")
```

## Migration SQL
No migration needed.

## Usage
Run standalone: `uv run fastmcp run app.mcp.server:mcp`
Or access via the mounted SSE endpoint at `/mcp`.
