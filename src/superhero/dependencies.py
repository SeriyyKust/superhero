from typing import Annotated
from fastapi import Query
from superhero.static import MAX_LENGTH_HERO_NAME
from superhero.schemas import HeroParamsSchema


_positive_int_annotated = Annotated[
            int | None,
            Query(
                ge=0
            )
        ]


def get_params_for_hero(
        name: Annotated[
            str | None,
            Query(
                min_length=1,
                max_length=MAX_LENGTH_HERO_NAME
            )
        ] = None,
        intelligence_eq: _positive_int_annotated = None,
        intelligence_lt: _positive_int_annotated = None,
        intelligence_gt: _positive_int_annotated = None,
        strength_eq: _positive_int_annotated = None,
        strength_lt: _positive_int_annotated = None,
        strength_gt: _positive_int_annotated = None,
        speed_eq: _positive_int_annotated = None,
        speed_lt: _positive_int_annotated = None,
        speed_gt: _positive_int_annotated = None,
        power_eq: _positive_int_annotated = None,
        power_lt: _positive_int_annotated = None,
        power_gt: _positive_int_annotated = None,
) -> HeroParamsSchema:
    return HeroParamsSchema(
        name=name,
        intelligence_eq=intelligence_eq,
        intelligence_lt=intelligence_lt,
        intelligence_gt=intelligence_gt,
        strength_eq=strength_eq,
        strength_lt=strength_lt,
        strength_gt=strength_gt,
        speed_eq=speed_eq,
        speed_lt=speed_lt,
        speed_gt=speed_gt,
        power_eq=power_eq,
        power_lt=power_lt,
        power_gt=power_gt,
    )
