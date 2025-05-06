from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import async_session
from app.core.security import decode_token
from app.models import User

oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_db():
    async with async_session() as session:
        yield session


async def get_current_user(
    token: str = Depends(oauth_scheme), db: AsyncSession = Depends(get_db)
) -> User:
    user_id = decode_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    user = await db.get(User, int(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
