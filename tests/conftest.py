import asyncio
import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.main import app
from app.core.database import async_session, engine, Base


# ---------- GLOBAL EVENT LOOP (pytest‑asyncio) ----------
@pytest.fixture(scope="session")
def event_loop() -> asyncio.AbstractEventLoop:  # ← переопределяем дефолт
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# ---------- DATABASE PREPARATION ----------
@pytest.fixture(scope="session", autouse=True)
async def prepare_db(event_loop):  # ⬅ тот же loop
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
    async with async_session() as session:
        yield session


# ---------- HTTP CLIENT ----------
@pytest.fixture
async def client(event_loop):
    """HTTP‑клиент внутри того же event‑loop (ASGITransport)."""
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac


# ---------- HELPER: зарегистрировать пользователя и вернуть заголовок ----------
@pytest.fixture
async def auth_header(client):
    """Быстрая регистрация + получение access‑токена."""
    payload = {"name": "Test", "email": "test@example.com", "password": "secret"}
    await client.post("/register", json=payload)
    tokens = (await client.post("/login", json=payload)).json()
    return {"Authorization": f"Bearer {tokens['access']}"}
