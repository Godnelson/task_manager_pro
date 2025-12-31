from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException
import uuid

from app.models.category import Category
from app.models.user import User

async def create_category(db: AsyncSession, user: User, name: str) -> Category:
    cat = Category(user_id=user.id, name=name)
    db.add(cat)
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Category name already exists")
    await db.refresh(cat)
    return cat

async def get_category(db: AsyncSession, user: User, category_id: uuid.UUID) -> Category:
    res = await db.execute(select(Category).where(Category.id == category_id, Category.user_id == user.id))
    cat = res.scalar_one_or_none()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    return cat

async def list_categories(db: AsyncSession, user: User, q: str | None, page: int, page_size: int):
    stmt = select(Category).where(Category.user_id == user.id)
    count_stmt = select(func.count()).select_from(Category).where(Category.user_id == user.id)

    if q:
        ql = f"%{q.lower()}%"
        stmt = stmt.where(func.lower(Category.name).like(ql))
        count_stmt = count_stmt.where(func.lower(Category.name).like(ql))

    stmt = stmt.order_by(Category.created_at.desc()).offset((page-1)*page_size).limit(page_size)

    total = (await db.execute(count_stmt)).scalar_one()
    items = (await db.execute(stmt)).scalars().all()
    return items, total

async def update_category(db: AsyncSession, user: User, category_id: uuid.UUID, name: str | None) -> Category:
    cat = await get_category(db, user, category_id)
    if name is not None:
        cat.name = name
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Category name already exists")
    await db.refresh(cat)
    return cat

async def delete_category(db: AsyncSession, user: User, category_id: uuid.UUID) -> None:
    cat = await get_category(db, user, category_id)
    await db.delete(cat)
    await db.commit()
