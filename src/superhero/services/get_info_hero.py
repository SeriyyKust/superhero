from typing import Any

import aiohttp
from aiohttp import ClientResponse
from superhero.schemas import HeroBaseSchema


class GetInfoHeroError(Exception): ...


class HeroInfoDontExistError(Exception): ...


class GetInfoHeroService:

    def __init__(self, access_token: str) -> None:
        self._access_token: str = access_token
        self._url: str = "https://superheroapi.com/api"

    async def execute(self, name: str) -> HeroBaseSchema:
        try:
            async with aiohttp.ClientSession() as session:
                response: ClientResponse = await session.get(
                    url=f"{self._url}/{self._access_token}/search/{name}", timeout=30
                )
                content: dict[Any, Any] = await response.json()
        except Exception as er:
            raise GetInfoHeroError(
                f"Во время выполнения запроса к сервису произошла ошибка {er}."
            )
        else:
            if content.get("response", "error") == "success":
                try:
                    init_hero: dict[str, str | int] = {
                        "name": content["results"][0]["name"],
                        "intelligence": int(
                            content["results"][0]["powerstats"]["intelligence"]
                        ),
                        "strength": int(content["results"][0]["powerstats"]["strength"]),
                        "speed": int(content["results"][0]["powerstats"]["speed"]),
                        "power": int(content["results"][0]["powerstats"]["power"]),
                    }
                    return HeroBaseSchema(**init_hero)
                except Exception as er:
                    raise GetInfoHeroError(
                        f"Во время выполнения запроса к сервису произошла ошибка {er}."
                    )
            else:
                if content.get("error", "") == "character with given name not found":
                    raise HeroInfoDontExistError(
                        f"Супер-героя с именем {name} нет в базе сервиса."
                    )
                else:
                    raise GetInfoHeroError(
                        "Во время выполнения запроса к сервису произошла "
                        "неизвестная ошибка."
                    )
