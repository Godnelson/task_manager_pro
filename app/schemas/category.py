import uuid
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=80)

class CategoryUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=80)

class CategoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    created_at: datetime

class PageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    items: list[CategoryOut]
    page: int
    page_size: int
    total: int
