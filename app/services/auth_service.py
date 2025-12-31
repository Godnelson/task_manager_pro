from datetime import datetime, timezone, timedelta
import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.core.security import (
    hash_password, verify_password,
    create_access_token, create_refresh_token,
    decode_token, hash_refresh_token
)
from app.core.config import settings

def utcnow():
    return datetime.now(timezone.utc)

async def register(db: AsyncSession, email: str, password: str) -> User:
    res = await db.execute(select(User).where(User.email == email))
    if res.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Email already registered")

    user = User(email=email, password_hash=hash_password(password))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def login(db: AsyncSession, email: str, password: str) -> tuple[str, str]:
    res = await db.execute(select(User).where(User.email == email))
    user = res.scalar_one_or_none()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access = create_access_token(str(user.id))
    refresh, jti = create_refresh_token(str(user.id))

    rt = RefreshToken(
        user_id=user.id,
        jti=jti,
        token_hash=hash_refresh_token(refresh),
        expires_at=utcnow() + timedelta(days=settings.refresh_token_expire_days),
    )
    db.add(rt)
    await db.commit()
    return access, refresh

async def refresh(db: AsyncSession, refresh_token: str) -> tuple[str, str]:
    try:
        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise ValueError("wrong token type")
        user_id = uuid.UUID(payload["sub"])
        jti = payload["jti"]
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    res = await db.execute(select(RefreshToken).where(RefreshToken.jti == jti))
    stored = res.scalar_one_or_none()
    if not stored or stored.revoked_at is not None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token revoked")
    if stored.expires_at <= utcnow():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired")

    if stored.token_hash != hash_refresh_token(refresh_token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token mismatch")

    # rotate
    stored.revoked_at = utcnow()
    access = create_access_token(str(user_id))
    new_refresh, new_jti = create_refresh_token(str(user_id))

    new_stored = RefreshToken(
        user_id=user_id,
        jti=new_jti,
        token_hash=hash_refresh_token(new_refresh),
        expires_at=utcnow() + timedelta(days=settings.refresh_token_expire_days),
    )
    db.add(new_stored)
    await db.commit()
    return access, new_refresh

async def logout(db: AsyncSession, refresh_token: str) -> None:
    try:
        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise ValueError("wrong token type")
        jti = payload["jti"]
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    res = await db.execute(select(RefreshToken).where(RefreshToken.jti == jti))
    stored = res.scalar_one_or_none()
    if stored and stored.revoked_at is None:
        stored.revoked_at = utcnow()
        await db.commit()
