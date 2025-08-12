from contextlib import asynccontextmanager

from database import Base, database_engine
from fastapi import FastAPI
from superhero.router import router as superhero_router


@asynccontextmanager
async def database_lifespan(_app: FastAPI):
    """
    Создаёт базу данным с определёнными отношениями,
    если она не определена
    """
    async with database_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=database_lifespan)
app.include_router(superhero_router)
