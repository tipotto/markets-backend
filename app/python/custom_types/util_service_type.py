from typing import TypedDict, Literal


class PriceType(TypedDict):
    str: str
    int: int


ProductStatusKeyTypes = list[Literal['all', 'brand_new', 'almost_unused', 'no_scratches_or_stains', 'slight_scratches_or_stains', 'noticeable_scratches_or_stains']]
