# Qdrant — Vector DB for RAG

## Dependencies
```bash
cd backend && uv add qdrant-client
```

## Doppler Secrets
- `QDRANT_URL` — Qdrant Cloud or self-hosted URL (e.g., `https://xxx.qdrant.io:6333`)
- `QDRANT_API_KEY` — API key for Qdrant Cloud

## Config Fields
Add to `backend/app/config.py`:
```python
# Qdrant
qdrant_url: str = ""
qdrant_api_key: str = ""
```

## Files to Create

### `backend/app/services/qdrant_client.py`
```python
"""Qdrant vector DB client singleton."""

from qdrant_client import QdrantClient

from app.config import settings

_client: QdrantClient | None = None


def get_qdrant_client() -> QdrantClient:
    """Return a singleton Qdrant client."""
    global _client
    if _client is None:
        _client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
        )
    return _client
```

### `backend/app/services/embeddings.py`
```python
"""Embedding generation for RAG."""

import litellm


async def get_embeddings(texts: list[str]) -> list[list[float]]:
    """Generate embeddings via LiteLLM."""
    response = await litellm.aembedding(
        model="text-embedding-3-small",
        input=texts,
    )
    return [item["embedding"] for item in response.data]
```

## Wiring Changes
No changes to main.py needed — import the client where you use it in services.

## Migration SQL
No SQL migration needed — Qdrant manages its own collections.

## Usage Pattern
```python
from qdrant_client.models import Distance, VectorParams, PointStruct

client = get_qdrant_client()

# Create collection
client.create_collection(
    collection_name="documents",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
)

# Upsert vectors
client.upsert(
    collection_name="documents",
    points=[
        PointStruct(id=1, vector=[0.1, ...], payload={"text": "..."}),
    ],
)

# Search
results = client.search(
    collection_name="documents",
    query_vector=[0.1, ...],
    limit=5,
)
```
