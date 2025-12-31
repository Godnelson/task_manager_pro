from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.core.db import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryOut, PageOut
from app.services import category_service

router = APIRouter(prefix="/categories", tags=["categories"])

@router.post("", response_model=CategoryOut)
async def create_category(
    payload: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await category_service.create_category(db, user, payload.name)

@router.get("", response_model=PageOut)
async def list_categories(
    q: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    items, total = await category_service.list_categories(db, user, q, page, page_size)
    return {"items": items, "page": page, "page_size": page_size, "total": total}

@router.get("/{category_id}", response_model=CategoryOut)
async def get_category(
    category_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await category_service.get_category(db, user, category_id)

@router.patch("/{category_id}", response_model=CategoryOut)
async def update_category(
    category_id: uuid.UUID,
    payload: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await category_service.update_category(db, user, category_id, payload.name)

@router.delete("/{category_id}")
async def delete_category(
    category_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    await category_service.delete_category(db, user, category_id)
    return {"ok": True}
