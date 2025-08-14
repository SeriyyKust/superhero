import os

import pytest_asyncio
from dotenv import load_dotenv
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool
from src.database import Base, get_database_session
from src.superhero.router import router as superhero_router


app = FastAPI()
app.include_router(superhero_router)


load_dotenv(".env.test")


ACCESS_TOKEN_TO_HERO_API: str = os.getenv("ACCESS_TOKEN_TO_HERO_API")


async_database_engine_test: AsyncEngine = create_async_engine(
    url=os.getenv("DB_URL"),
    poolclass=NullPool,
)
session_factory_test: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=async_database_engine_test, expire_on_commit=False
)


@pytest_asyncio.fixture(scope="module")
async def prepare_db():
    async with async_database_engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with async_database_engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture()
async def db_session():
    async with session_factory_test() as session:
        yield session


@pytest_asyncio.fixture(autouse=True)
def override_get_db_fixture(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_database_session] = override_get_db
