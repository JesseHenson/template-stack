"""Add FK constraint and indexes.

Revision ID: 002
Revises: 001
Create Date: 2024-01-01 00:00:01.000000
"""
from typing import Sequence, Union

from alembic import op

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index("ix_users_clerk_id", "users", ["clerk_id"])
    op.create_index("ix_items_user_id", "items", ["user_id"])
    op.create_foreign_key(
        "fk_items_user_id",
        "items",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("fk_items_user_id", "items", type_="foreignkey")
    op.drop_index("ix_items_user_id", "items")
    op.drop_index("ix_users_clerk_id", "users")
