from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from datetime import date

from app.core.db import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.task import TaskStatus, TaskPriority
from app.schemas.task import TaskCreate, TaskUpdate, TaskOut, PageOut
from app.services import task_service

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("", response_model=TaskOut)
async def create_task(
    payload: TaskCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await task_service.create_task(db, user, payload)

@router.get("", response_model=PageOut)
async def list_tasks(
    q: str | None = None,
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
    category_id: uuid.UUID | None = None,
    due_from: date | None = None,
    due_to: date | None = None,
    created_from: date | None = None,
    created_to: date | None = None,
    sort: str = Query("-created_at"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    items, total = await task_service.list_tasks(
        db, user, q, status, priority, category_id,
        due_from, due_to, created_from, created_to,
        sort, page, page_size
    )
    return {"items": items, "page": page, "page_size": page_size, "total": total}

@router.get("/{task_id}", response_model=TaskOut)
async def get_task(
    task_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await task_service.get_task(db, user, task_id)

@router.patch("/{task_id}", response_model=TaskOut)
async def update_task(
    task_id: uuid.UUID,
    payload: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await task_service.update_task(db, user, task_id, payload)

@router.delete("/{task_id}")
async def delete_task(
    task_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    await task_service.delete_task(db, user, task_id)
    return {"ok": True}
