from pydantic import BaseModel, ConfigDict, Field, PositiveInt
from superhero.static import MAX_LENGTH_HERO_NAME


class HeroAddSchema(BaseModel):
    name: str = Field(
        title="Имя супер-героя", min_length=1, max_length=MAX_LENGTH_HERO_NAME
    )


class HeroBaseSchema(HeroAddSchema):
    model_config = ConfigDict(from_attributes=True)
    # id: int = PositiveInt(title="Идентификатор героя")
    intelligence: PositiveInt = Field(title="Интеллект")
    strength: PositiveInt = Field(title="Сила")
    speed: PositiveInt = Field(title="Скорость")
    power: PositiveInt = Field(title="Мощь")
