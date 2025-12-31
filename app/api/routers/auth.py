from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.schemas.auth import RegisterIn, LoginIn, TokenOut, RefreshIn, LogoutIn
from app.schemas.user import UserPublic
from app.services import auth_service
from app.core.rate_limit import limiter

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserPublic)
@limiter.limit("5/minute")
async def register(request: Request, payload: RegisterIn, db: AsyncSession = Depends(get_db)):
    user = await auth_service.register(db, payload.email, payload.password)
    return user

@router.post("/login", response_model=TokenOut)
@limiter.limit("5/minute")
async def login(request: Request, payload: LoginIn, db: AsyncSession = Depends(get_db)):
    access, refresh = await auth_service.login(db, payload.email, payload.password)
    return TokenOut(access_token=access, refresh_token=refresh)

@router.post("/refresh", response_model=TokenOut)
@limiter.limit("20/minute")
async def refresh(request: Request, payload: RefreshIn, db: AsyncSession = Depends(get_db)):
    access, refresh = await auth_service.refresh(db, payload.refresh_token)
    return TokenOut(access_token=access, refresh_token=refresh)

@router.post("/logout")
@limiter.limit("20/minute")
async def logout(request: Request, payload: LogoutIn, db: AsyncSession = Depends(get_db)):
    await auth_service.logout(db, payload.refresh_token)
    return {"ok": True}
