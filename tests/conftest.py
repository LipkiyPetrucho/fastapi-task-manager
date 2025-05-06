import asyncio
import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.main import app
from app.core.database import async_session, engine, Base


# ---------- DATABASE PREPARATION ----------
@pytest.fixture(scope="session", autouse=True)
async def prepare_db():
    loop = asyncio.get_running_loop()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    # при желании подчистить данные:
    await engine.dispose()


# ---------- DB SESSION ----------
@pytest.fixture
async def db_session() -> AsyncSession:
    """Отдаём отдельную async‑сессию на каждый тест."""
    loop = asyncio.get_running_loop()
    async with async_session() as session:
        yield session


# ---------- HTTP CLIENT ----------
@pytest.fixture
async def client():
    """HTTP‑клиент внутри того же event‑loop (ASGITransport)."""
    loop = asyncio.get_running_loop()
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac


# ---------- HELPER: зарегистрировать пользователя и вернуть заголовок ----------
@pytest.fixture
async def auth_header(client):
    """Быстрая регистрация + получение access‑токена."""
    loop = asyncio.get_running_loop()
    payload = {"name": "Test", "email": "test@example.com", "password": "secret"}
    await client.post("/register", json=payload)
    tokens = (await client.post("/login", json=payload)).json()
    return {"Authorization": f"Bearer {tokens['access']}"}
