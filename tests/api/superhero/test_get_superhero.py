import pytest
from httpx import ASGITransport, AsyncClient
from tests.api.conftest import app, prepare_db
from tests.api.superhero.fixtures import patch_get_info_service


@pytest.mark.anyio
async def test_get_empty_db(prepare_db):
    hero_name: str = "oleg"
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get(f"/heroes/?name={hero_name}")
        assert response.status_code == 404
        response_data = response.json()
        assert response_data["detail"] == "Супер герои с такими параметрами не найдены."


@pytest.mark.anyio
async def test_get_hero_by_name_db(prepare_db, patch_get_info_service):
    hero: dict[str, str | int] = patch_get_info_service["success"]
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post("/heroes/", json={"name": hero["name"]})
        assert response.status_code == 201
        response = await ac.get(f"/heroes/?intelligence_lt={hero["intelligence"] + 10}")
        assert response.status_code == 200
        response_data = response.json()
        assert response_data == [hero]
