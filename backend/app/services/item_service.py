"""Example CRUD service — replace with your product's services.

Follows the clerk_id → user_id ownership pattern.
"""

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Item, User
from app.models.item import ItemCreate, ItemUpdate


async def get_user_id_from_clerk_id(db: AsyncSession, clerk_id: str) -> str:
    """Look up the internal user UUID from a Clerk user ID."""
    result = await db.execute(select(User.id).where(User.clerk_id == clerk_id))
    user_id = result.scalar_one_or_none()
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found. Please sign in again.",
        )
    return str(user_id)


async def list_items(
    db: AsyncSession, clerk_id: str, *, limit: int = 50, offset: int = 0
) -> tuple[list[Item], int]:
    """List items for a user with pagination. Returns (items, total_count)."""
    user_id = await get_user_id_from_clerk_id(db, clerk_id)
    base = select(Item).where(Item.user_id == user_id)

    count_result = await db.execute(select(func.count()).select_from(base.subquery()))
    total = count_result.scalar_one()

    result = await db.execute(
        base.order_by(Item.created_at.desc()).limit(limit).offset(offset)
    )
    return list(result.scalars().all()), total


async def get_item(db: AsyncSession, clerk_id: str, item_id: str) -> Item:
    """Get a single item, ensuring it belongs to the user."""
    user_id = await get_user_id_from_clerk_id(db, clerk_id)
    result = await db.execute(
        select(Item).where(Item.id == item_id, Item.user_id == user_id)
    )
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )
    return item


async def create_item(db: AsyncSession, clerk_id: str, data: ItemCreate) -> Item:
    """Create a new item."""
    user_id = await get_user_id_from_clerk_id(db, clerk_id)
    item = Item(
        user_id=user_id,
        name=data.name,
        description=data.description,
        metadata_=data.metadata,
    )
    db.add(item)
    await db.flush()
    await db.refresh(item)
    return item


async def update_item(db: AsyncSession, clerk_id: str, item_id: str, data: ItemUpdate) -> Item:
    """Update an item, ensuring it belongs to the user."""
    item = await get_item(db, clerk_id, item_id)

    update_data = data.model_dump(exclude_none=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update",
        )

    for key, value in update_data.items():
        if key == "metadata":
            setattr(item, "metadata_", value)
        else:
            setattr(item, key, value)

    await db.flush()
    await db.refresh(item)
    return item


async def delete_item(db: AsyncSession, clerk_id: str, item_id: str) -> None:
    """Delete an item, ensuring it belongs to the user."""
    item = await get_item(db, clerk_id, item_id)
    await db.delete(item)
