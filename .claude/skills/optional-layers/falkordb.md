# FalkorDB — Graph DB for Knowledge Graphs

## Dependencies
```bash
cd backend && uv add falkordb
```

## Doppler Secrets
- `FALKORDB_URL` — FalkorDB connection URL (e.g., `redis://localhost:6379`)

## Config Fields
Add to `backend/app/config.py`:
```python
# FalkorDB
falkordb_url: str = ""
```

## Files to Create

### `backend/app/services/falkordb_client.py`
```python
"""FalkorDB graph database client singleton."""

from falkordb import FalkorDB

from app.config import settings

_client: FalkorDB | None = None


def get_falkordb_client() -> FalkorDB:
    """Return a singleton FalkorDB client."""
    global _client
    if _client is None:
        _client = FalkorDB.from_url(settings.falkordb_url)
    return _client


def get_graph(name: str = "default"):
    """Get a named graph from FalkorDB."""
    client = get_falkordb_client()
    return client.select_graph(name)
```

## Wiring Changes
No changes to main.py needed — import the client where you use it in services.

## Migration SQL
No SQL migration needed — FalkorDB manages its own graph schema.

## Usage Pattern
```python
graph = get_graph("knowledge")

# Create nodes and relationships
graph.query("""
    CREATE (a:Entity {name: $name, type: $type})
""", params={"name": "Python", "type": "language"})

graph.query("""
    MATCH (a:Entity {name: $from}), (b:Entity {name: $to})
    CREATE (a)-[:RELATES_TO {weight: $weight}]->(b)
""", params={"from": "Python", "to": "FastAPI", "weight": 0.9})

# Query
result = graph.query("""
    MATCH (a:Entity)-[r:RELATES_TO]->(b:Entity)
    WHERE a.name = $name
    RETURN b.name, r.weight
""", params={"name": "Python"})
```
