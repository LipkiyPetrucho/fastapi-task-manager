from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import init_db
from app.routers import auth, tasks


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="TestWork05",
    lifespan=lifespan,
)

app.include_router(auth.router)
app.include_router(tasks.router)
