"""Example CRUD endpoints — replace with your product's resources."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.middleware import CurrentUserId
from app.db.session import get_db
from app.models.item import ItemCreate, ItemResponse, ItemUpdate, PaginatedResponse
from app.services.item_service import (
    create_item,
    delete_item,
    get_item,
    list_items,
    update_item,
)

router = APIRouter()


@router.get("", response_model=PaginatedResponse[ItemResponse])
async def list_items_endpoint(
    clerk_id: CurrentUserId,
    db: AsyncSession = Depends(get_db),
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    items, total = await list_items(db, clerk_id, limit=limit, offset=offset)
    return PaginatedResponse(items=items, total=total, limit=limit, offset=offset)


@router.post("", response_model=ItemResponse, status_code=201)
async def create_item_endpoint(
    clerk_id: CurrentUserId, data: ItemCreate, db: AsyncSession = Depends(get_db)
):
    return await create_item(db, clerk_id, data)


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item_endpoint(
    clerk_id: CurrentUserId, item_id: str, db: AsyncSession = Depends(get_db)
):
    return await get_item(db, clerk_id, item_id)


@router.patch("/{item_id}", response_model=ItemResponse)
async def update_item_endpoint(
    clerk_id: CurrentUserId, item_id: str, data: ItemUpdate, db: AsyncSession = Depends(get_db)
):
    return await update_item(db, clerk_id, item_id, data)


@router.delete("/{item_id}", status_code=204)
async def delete_item_endpoint(
    clerk_id: CurrentUserId, item_id: str, db: AsyncSession = Depends(get_db)
):
    await delete_item(db, clerk_id, item_id)
