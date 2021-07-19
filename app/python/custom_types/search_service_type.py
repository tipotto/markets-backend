from typing import TypedDict, Literal
from .util_service_type import PriceType


class SearchItemType(TypedDict):
    id: str
    title: str
    price: PriceType
    imageUrl: str
    detailUrl: str
    platform: Literal['mercari', 'rakuma', 'paypay']
    isFavorite: bool


# class SearchResultType(TypedDict):
#     data: Optional[SearchItemType]
#     error: Optional[Literal['keyword', 'likes']]


class SearchFormType(TypedDict):
    page: int
    category: dict[Literal['main', 'sub'], str]
    searchType: Literal['market', 'price']
    keyword: str
    platforms: list[Literal['mercari', 'rakuma', 'paypay']]
    minPrice: int
    maxPrice: int
    productStatus: list[Literal['all', 'brand_new', 'almost_unused', 'no_scratches_or_stains', 'slight_scratches_or_stains', 'noticeable_scratches_or_stains']]
    salesStatus: Literal['all', 'selling', 'soldout']
    deliveryCost: Literal['all', 'free', 'required']
    sortOrder: Literal['asc', 'desc']
    keywordFilter: Literal['use', 'unuse']


class CategoryType(TypedDict):
    main: str
    sub: str


PriceKeyTypes: Literal['minPrice', 'maxPrice']
ProductStatusValueTypes: list[Literal['all', 'brand_new', 'almost_unused', 'no_scratches_or_stains', 'slight_scratches_or_stains', 'noticeable_scratches_or_stains']]
# class CategoryType(TypedDict):
#     main: Literal['main', 'sub']
#     sub: Literal['main', 'sub']
