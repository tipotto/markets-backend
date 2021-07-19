from typing import TypedDict, Literal, Optional
from util_service_type import PriceType


class AnalysisItemType(TypedDict):
    id: str
    title: str
    price: PriceType
    imageUrl: str
    detailUrl: str
    platform: Literal['mercari', 'rakuma', 'paypay']
    likes: int


class AnalysisResultType(TypedDict):
    data: Optional[AnalysisItemType]
    error: Optional[Literal['keyword', 'likes']]


class AnalysisFormType(TypedDict):
    searchType: Literal['market', 'price']
    keyword: str
    platforms: list[Literal['mercari', 'rakuma', 'paypay']]
    productStatus: list[Literal['all', 'brand_new', 'almost_unused', 'no_scratches_or_stains', 'slight_scratches_or_stains', 'noticeable_scratches_or_stains']]
    deliveryCost: Literal['all', 'free', 'required']
    keywordFilter: Literal['use', 'unuse']
