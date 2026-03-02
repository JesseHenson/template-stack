# Supabase Storage — File/Object Storage

## Dependencies
No additional dependencies — `supabase-py` already includes storage support.

## Doppler Secrets
No additional secrets — uses the existing Supabase service role key.

## Config Fields
No additional config fields needed.

## Files to Create

### `backend/app/services/storage_client.py`
```python
"""Supabase Storage client for file uploads."""

from app.services.supabase_client import get_supabase_client


def upload_file(
    bucket: str,
    path: str,
    file_data: bytes,
    content_type: str = "application/octet-stream",
) -> str:
    """Upload a file and return its public URL."""
    db = get_supabase_client()
    db.storage.from_(bucket).upload(path, file_data, {"content-type": content_type})
    return db.storage.from_(bucket).get_public_url(path)


def delete_file(bucket: str, path: str) -> None:
    """Delete a file from storage."""
    db = get_supabase_client()
    db.storage.from_(bucket).remove([path])


def get_signed_url(bucket: str, path: str, expires_in: int = 3600) -> str:
    """Get a signed URL for private file access."""
    db = get_supabase_client()
    result = db.storage.from_(bucket).create_signed_url(path, expires_in)
    return result["signedURL"]


def list_files(bucket: str, folder: str = "") -> list[dict]:
    """List files in a bucket/folder."""
    db = get_supabase_client()
    return db.storage.from_(bucket).list(folder)
```

### `backend/app/api/uploads.py`
```python
"""File upload endpoints."""

from fastapi import APIRouter, UploadFile

from app.auth.middleware import CurrentUserId
from app.services.storage_client import delete_file, upload_file

router = APIRouter()


@router.post("")
async def upload(clerk_id: CurrentUserId, file: UploadFile):
    """Upload a file for the current user."""
    path = f"{clerk_id}/{file.filename}"
    contents = await file.read()
    url = upload_file("uploads", path, contents, file.content_type or "application/octet-stream")
    return {"url": url, "path": path}


@router.delete("")
async def remove(clerk_id: CurrentUserId, path: str):
    """Delete a user's file."""
    if not path.startswith(f"{clerk_id}/"):
        return {"error": "Unauthorized"}
    delete_file("uploads", path)
    return {"status": "ok"}
```

## Wiring Changes

### Backend — `backend/app/api/router.py`
```python
from app.api.uploads import router as uploads_router
api_router.include_router(uploads_router, prefix="/uploads", tags=["uploads"])
```

## Supabase Dashboard Setup
1. Go to Supabase Dashboard → Storage
2. Create a bucket named `uploads`
3. Set bucket to public or private based on your needs
4. Configure file size limits and allowed MIME types

## Migration SQL
No SQL migration needed — Supabase Storage is managed via the dashboard/API.
