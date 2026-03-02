"""Example CRUD endpoints — replace with your product's resources."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.middleware import CurrentUserId
from app.db.session import get_db
from app.models.item import ItemCreate, ItemResponse, ItemUpdate
from app.services.item_service import (
    create_item,
    delete_item,
    get_item,
    list_items,
    update_item,
)

router = APIRouter()


@router.get("", response_model=list[ItemResponse])
async def list_items_endpoint(
    clerk_id: CurrentUserId, db: AsyncSession = Depends(get_db)
):
    return await list_items(db, clerk_id)


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
