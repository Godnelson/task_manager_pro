import uuid
from datetime import datetime, date
from pydantic import BaseModel, Field, ConfigDict
from app.models.task import TaskStatus, TaskPriority

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=140)
    description: str | None = None
    category_id: uuid.UUID | None = None
    status: TaskStatus = TaskStatus.todo
    priority: TaskPriority = TaskPriority.med
    due_date: date | None = None

class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=140)
    description: str | None = None
    category_id: uuid.UUID | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    due_date: date | None = None

class TaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    category_id: uuid.UUID | None = None
    title: str
    description: str | None = None
    status: str
    priority: str
    due_date: date | None = None
    created_at: datetime
    updated_at: datetime

class PageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    items: list[TaskOut]
    page: int
    page_size: int
    total: int

