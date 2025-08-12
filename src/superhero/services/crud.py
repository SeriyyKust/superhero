from typing import Sequence

from superhero.models import HeroModel
from superhero.schemas import HeroBaseSchema
from sqlalchemy import Result, select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from superhero.schemas import HeroParamsSchema


async def add_hero_to_db(
    session: AsyncSession, new_hero: HeroBaseSchema
) -> HeroModel:
    db_new_hero = HeroModel(**new_hero.model_dump())
    session.add(db_new_hero)
    await session.commit()
    await session.refresh(db_new_hero)
    return db_new_hero


async def get_heros_from_db_by_params(
    session: AsyncSession,
    params: HeroParamsSchema
) -> Sequence[HeroModel]:
    conditions = []
    for key, value in params.model_dump().items():
        if value:
            if key.endswith("_eq"):
                column = getattr(HeroModel, key[:-3])
                conditions.append(column==value)
            elif key.endswith("_gt"):
                column = getattr(HeroModel, key[:-3])
                conditions.append(column > value)
            elif key.endswith("_lt"):
                column = getattr(HeroModel, key[:-3])
                conditions.append(column < value)
            else:
                column = getattr(HeroModel, key)
                conditions.append(column == value)
    query = select(HeroModel).where(and_(*conditions))
    result: Result = await session.execute(query)
    return result.scalars().all()
