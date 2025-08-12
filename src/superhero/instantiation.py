from superhero.services.get_info_hero import GetInfoHeroService
from config import settings


get_info_hero_service = GetInfoHeroService(
    access_token=settings.access_token_to_hero_api
)
