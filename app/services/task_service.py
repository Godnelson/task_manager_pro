from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from fastapi import HTTPException
import uuid
from datetime import date

from app.models.task import Task, TaskStatus, TaskPriority
from app.models.user import User

SORT_FIELDS = {
    "created_at": Task.created_at,
    "due_date": Task.due_date,
    "priority": Task.priority,
    "updated_at": Task.updated_at,
    "title": Task.title,
}

async def create_task(db: AsyncSession, user: User, data) -> Task:
    task = Task(
        user_id=user.id,
        title=data.title,
        description=data.description,
        category_id=data.category_id,
        status=data.status,
        priority=data.priority,
        due_date=data.due_date,
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task

async def get_task(db: AsyncSession, user: User, task_id: uuid.UUID) -> Task:
    res = await db.execute(select(Task).where(Task.id == task_id, Task.user_id == user.id))
    task = res.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

async def update_task(db: AsyncSession, user: User, task_id: uuid.UUID, data) -> Task:
    task = await get_task(db, user, task_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    await db.commit()
    await db.refresh(task)
    return task

async def delete_task(db: AsyncSession, user: User, task_id: uuid.UUID) -> None:
    task = await get_task(db, user, task_id)
    await db.delete(task)
    await db.commit()

async def list_tasks(
    db: AsyncSession,
    user: User,
    q: str | None,
    status: TaskStatus | None,
    priority: TaskPriority | None,
    category_id: uuid.UUID | None,
    due_from: date | None,
    due_to: date | None,
    created_from: date | None,
    created_to: date | None,
    sort: str,
    page: int,
    page_size: int,
):
    stmt = select(Task).where(Task.user_id == user.id)
    count_stmt = select(func.count()).select_from(Task).where(Task.user_id == user.id)

    if q:
        ql = f"%{q.lower()}%"
        cond = or_(
            func.lower(Task.title).like(ql),
            func.lower(func.coalesce(Task.description, "")).like(ql),
        )
        stmt = stmt.where(cond)
        count_stmt = count_stmt.where(cond)

    if status:
        stmt = stmt.where(Task.status == status)
        count_stmt = count_stmt.where(Task.status == status)

    if priority:
        stmt = stmt.where(Task.priority == priority)
        count_stmt = count_stmt.where(Task.priority == priority)

    if category_id:
        stmt = stmt.where(Task.category_id == category_id)
        count_stmt = count_stmt.where(Task.category_id == category_id)

    if due_from:
        stmt = stmt.where(Task.due_date >= due_from)
        count_stmt = count_stmt.where(Task.due_date >= due_from)
    if due_to:
        stmt = stmt.where(Task.due_date <= due_to)
        count_stmt = count_stmt.where(Task.due_date <= due_to)

    # created_* are date-only filters; compare against date portion
    if created_from:
        stmt = stmt.where(func.date(Task.created_at) >= created_from)
        count_stmt = count_stmt.where(func.date(Task.created_at) >= created_from)
    if created_to:
        stmt = stmt.where(func.date(Task.created_at) <= created_to)
        count_stmt = count_stmt.where(func.date(Task.created_at) <= created_to)

    desc = False
    field = sort
    if sort.startswith("-"):
        desc = True
        field = sort[1:]

    order_col = SORT_FIELDS.get(field, Task.created_at)
    stmt = stmt.order_by(order_col.desc() if desc else order_col.asc())

    stmt = stmt.offset((page-1)*page_size).limit(page_size)

    total = (await db.execute(count_stmt)).scalar_one()
    items = (await db.execute(stmt)).scalars().all()
    return items, total
