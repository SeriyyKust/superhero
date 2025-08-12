from typing import AsyncGenerator

from config import settings
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase


database_engine: AsyncEngine = create_async_engine(
    url=settings.db_url, echo=settings.db_echo
)
session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=database_engine, autoflush=False, autocommit=False, expire_on_commit=False
)


async def get_database_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Создаёт и управляет асинхронной сессией в SQLAlchemy
    :return: генератор, выдающий объект AsyncSession
    """
    async with session_factory() as session:
        yield session


class Base(DeclarativeBase):
    __abstract__ = True
