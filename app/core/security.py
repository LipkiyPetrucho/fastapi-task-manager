from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import get_settings

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
settings = get_settings()


def hash_password(pwd: str) -> str:
    return pwd_ctx.hash(pwd)


def verify_password(pwd: str, hashed: str) -> bool:
    return pwd_ctx.verify(pwd, hashed)


def _create_token(sub: str, exp_delta) -> str:
    to_encode = {
                "sub": sub,
                "exp": datetime.now(timezone.utc) + exp_delta,
        }
    return jwt.encode(to_encode, settings.jwt_secret, settings.jwt_algo)


def create_access(sub: str) -> str:
    return _create_token(sub, timedelta(minutes=settings.access_expires_minutes))


def create_refresh(sub: str) -> str:
    return _create_token(sub, timedelta(days=settings.refresh_expires_days))


def decode_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, settings.jwt_secret, settings.jwt_algo)
        return payload["sub"]
    except JWTError:
        return None
