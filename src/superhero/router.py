from database import get_database_session
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)
from superhero.dependencies import get_params_for_hero
from superhero.instantiation import get_info_hero_service
from superhero.schemas import HeroAddSchema, HeroBaseSchema, HeroParamsSchema
from superhero.services.crud import add_hero_to_db, get_heros_from_db_by_params
from superhero.services.get_info_hero import GetInfoHeroError, HeroInfoDontExistError


router = APIRouter(prefix="/heroes", tags=["heroes"])


@router.post(path="/", summary="Добавление нового героя", response_model=HeroBaseSchema)
async def api_add_hero(
    new_hero: HeroAddSchema, session: AsyncSession = Depends(get_database_session)
):
    # Проверка в базе данных -> допустим его нет
    try:
        hero: HeroBaseSchema = await get_info_hero_service.execute(name=new_hero.name)
    except HeroInfoDontExistError:
        raise HTTPException(
            status_code=404, detail=f"Героя с именем {new_hero.name} не существует."
        )
    except GetInfoHeroError:
        raise HTTPException(
            status_code=500,
            detail="Возникла ошибка при обращении к внешнему сервису с базой героев.",
        )
    try:
        await add_hero_to_db(session=session, new_hero=hero)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Возникла ошибка при попытке сохранить героя в базу данных",
        )
    return hero


@router.get(
    path="/",
    summary="Получение героев по параметрам",
    response_model=list[HeroBaseSchema],
)
async def api_get_heroes_by_params(
    params: HeroParamsSchema = Depends(get_params_for_hero),
    session: AsyncSession = Depends(get_database_session),
):
    return await get_heros_from_db_by_params(session=session, params=params)
