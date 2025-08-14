import logging
from typing import Sequence

from database import get_database_session
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)
from superhero.dependencies import get_info_hero_service, get_params_for_hero
from superhero.models import HeroModel
from superhero.schemas import HeroAddSchema, HeroBaseSchema, HeroParamsSchema
from superhero.services.crud import add_hero_to_db, get_heroes_from_db_by_params
from superhero.services.get_info_hero import (
    GetInfoHeroError,
    GetInfoHeroService,
    HeroInfoDontExistError,
)


_logger = logging.getLogger("superhero_router")
_handler = logging.FileHandler("superhero_router.log", mode="w")
_formatter = logging.Formatter("[%(name)s %(asctime)s %(levelname)s]: %(message)s")
_handler.setFormatter(_formatter)
_logger.addHandler(_handler)


router = APIRouter(prefix="/heroes", tags=["heroes"])


@router.post(
    path="/",
    summary="Добавление нового героя",
    response_model=HeroBaseSchema,
    status_code=201,
)
async def api_add_hero(
    new_hero: HeroAddSchema,
    session: AsyncSession = Depends(get_database_session),
    hero_service: GetInfoHeroService = Depends(get_info_hero_service),
):
    try:
        heroes: Sequence[HeroModel] = await get_heroes_from_db_by_params(
            session=session, params=HeroParamsSchema(name=new_hero.name)
        )
        if len(heroes):
            return heroes[0]
    except Exception as er:
        text: str = "Во время обращения к базе данных произошла ошибка."
        _logger.error(text + " %s", str(er))
        raise HTTPException(status_code=500, detail=text)
    try:
        hero: HeroBaseSchema = await hero_service.execute(name=new_hero.name)
    except HeroInfoDontExistError:
        text: str = f"Героя с именем {new_hero.name} не существует."
        _logger.info(text)
        raise HTTPException(status_code=404, detail=text)
    except GetInfoHeroError as er:
        text: str = "Возникла ошибка при обращении к внешнему сервису с базой героев."
        _logger.error(text + " %s", str(er))
        raise HTTPException(status_code=500, detail=text)
    try:
        await add_hero_to_db(session=session, new_hero=hero)
    except Exception as er:
        text: str = "Возникла ошибка при попытке сохранить героя в базу данных."
        _logger.error(text + " %s", str(er))
        raise HTTPException(
            status_code=500,
            detail=text,
        )
    return hero


@router.get(
    path="/",
    summary="Получение героев по параметрам",
    response_model=list[HeroBaseSchema],
    status_code=200,
)
async def api_get_heroes_by_params(
    params: HeroParamsSchema = Depends(get_params_for_hero),
    session: AsyncSession = Depends(get_database_session),
):
    try:
        heroes: Sequence[HeroModel] = await get_heroes_from_db_by_params(
            session=session, params=params
        )
    except Exception as er:
        text: str = "Во время обращения к базе данных произошла ошибка."
        _logger.error(text + " %s", str(er))
        raise HTTPException(status_code=500, detail=text)
    else:
        if not len(heroes):
            raise HTTPException(
                status_code=404,
                detail="Супер герои с такими параметрами не найдены.",
            )
        return heroes
