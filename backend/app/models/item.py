"""Example Pydantic models — replace with your product's models."""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ItemCreate(BaseModel):
    name: str
    description: str = ""
    metadata: dict = {}


class ItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    metadata: dict | None = None


class ItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    name: str
    description: str
    metadata: dict = Field(validation_alias="metadata_")
    created_at: datetime
    updated_at: datetime
