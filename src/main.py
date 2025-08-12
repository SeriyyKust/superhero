from contextlib import asynccontextmanager

from database import Base, database_engine
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from superhero.models import HeroModel


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


@app.get("/test")
async def test_handler():
    return JSONResponse(status_code=200, content={"message": "ok"})
