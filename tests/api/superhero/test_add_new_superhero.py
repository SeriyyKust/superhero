import pytest
from httpx import ASGITransport, AsyncClient
from tests.api.conftest import app, prepare_db
from tests.api.superhero.fixtures import patch_get_info_service


@pytest.mark.anyio
async def test_post_hero_success(prepare_db, patch_get_info_service):
    hero: dict[str, str | int] = patch_get_info_service["success"]
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post("/heroes/", json={"name": hero["name"]})
        assert response.status_code == 201
        data = response.json()
        assert data["name"].lower() == hero["name"].lower()
        for key in ("intelligence", "strength", "speed", "power"):
            assert data[key] == hero[key]


@pytest.mark.anyio
async def test_post_hero_dont_exist(prepare_db):
    hero_name: str = "gaga"
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post("/heroes/", json={"name": hero_name})
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == f"Героя с именем {hero_name} не существует."
