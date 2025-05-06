from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.core.config import get_settings

settings = get_settings()

engine = create_async_engine(str(settings.database_url), echo=False)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def init_db():
    from app import models  # noqa:  F401

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
