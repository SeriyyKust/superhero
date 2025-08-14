from unittest.mock import AsyncMock

import pytest_asyncio
from src.superhero.router import get_info_hero_service
from src.superhero.schemas import HeroBaseSchema
from src.superhero.services.get_info_hero import GetInfoHeroError, HeroInfoDontExistError
from tests.api.conftest import app


# Мокает сервис обращения со сторонней API для избежания ошибок с её стороны
@pytest_asyncio.fixture
async def patch_get_info_service():
    data: dict[str, dict[str, str | int]] = {
        "success": {
            "name": "mario",
            "intelligence": 2,
            "strength": 33,
            "speed": 44,
            "power": 2,
        },
        "dont-exist": {"name": "mario-74"},
    }

    async def fake_execute(name: str):
        if name == data["success"]["name"]:
            return HeroBaseSchema.model_validate(data)
        elif name == data["dont-exist"]["name"]:
            raise HeroInfoDontExistError
        else:
            raise GetInfoHeroError

    mock_service = AsyncMock()
    mock_service.execute.side_effect = fake_execute
    app.dependency_overrides[get_info_hero_service] = lambda: mock_service
    yield data
    app.dependency_overrides.pop(get_info_hero_service)
