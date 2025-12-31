from datetime import datetime, timedelta, timezone
from typing import Any, Optional, Dict
from jose import jwt
from passlib.context import CryptContext
import hashlib
import secrets
import uuid

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def create_access_token(subject: str, extra: Optional[Dict[str, Any]] = None) -> str:
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=settings.access_token_expire_min)

    payload: Dict[str, Any] = {
        "sub": subject,
        "type": "access",
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
        "jti": str(uuid.uuid4()),
    }
    if extra:
        payload.update(extra)

    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_alg)


def create_refresh_token(subject: str, jti: Optional[str] = None) -> tuple[str, str]:
    now = datetime.now(timezone.utc)
    exp = now + timedelta(days=settings.refresh_token_expire_days)
    jti = jti or secrets.token_urlsafe(24)
    payload: Dict[str, Any] = {"sub": subject, "type": "refresh", "jti": jti, "iat": int(now.timestamp()), "exp": exp}
    token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_alg)
    return token, jti


def decode_token(token: str) -> Dict[str, Any]:
    return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_alg])


def hash_refresh_token(token: str) -> str:
    # Pepper + SHA-256 to avoid storing refresh token in plain text
    raw = (settings.refresh_token_pepper + token).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()
