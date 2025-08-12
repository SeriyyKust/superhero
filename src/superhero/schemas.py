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


class HeroParamsSchema(BaseModel):
    name: str | None = Field(
        title="Имя супер-героя",
        min_length=1,
        max_length=MAX_LENGTH_HERO_NAME,
        default=None
    )
    intelligence_eq: PositiveInt | None = Field(
        title="Интеллект ==",
        default=None
    )
    intelligence_lt: PositiveInt | None = Field(
        title="Интеллект <",
        default=None
    )
    intelligence_gt: PositiveInt | None = Field(
        title="Интеллект >",
        default=None
    )
    strength_eq: PositiveInt | None = Field(
        title="Сила ==",
        default=None
    )
    strength_lt: PositiveInt | None = Field(
        title="Сила <",
        default=None
    )
    strength_gt: PositiveInt | None = Field(
        title="Сила >",
        default=None
    )
    speed_eq: PositiveInt | None = Field(
        title="Скорость ==",
        default=None
    )
    speed_lt: PositiveInt | None = Field(
        title="Скорость <",
        default=None
    )
    speed_gt: PositiveInt | None = Field(
        title="Скорость >",
        default=None
    )
    power_eq: PositiveInt | None = Field(
        title="Мощь ==",
        default=None
    )
    power_lt: PositiveInt | None = Field(
        title="Мощь <",
        default=None
    )
    power_gt: PositiveInt | None = Field(
        title="Мощь >",
        default=None
    )
