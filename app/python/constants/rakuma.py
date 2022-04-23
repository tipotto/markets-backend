from constants.util import PLATFORM_TYPE_WEB

SERVICE_NAME = 'rakuma'
WEB_URL = 'https://fril.jp'
CONS = {
    'name': SERVICE_NAME,
    'type': PLATFORM_TYPE_WEB,
    'auth_token': None,
    'data': {
        'req': {
            'url': {
                'web': WEB_URL,
                'api': None
            },
            'headers': None,
            'keys': {
                'page': 'page',
                'keyword': 'keyword',
                'negKeyword': 'negKeyword',
                'searchRange': None,
                'minPrice': 'minPrice',
                'maxPrice': 'maxPrice',
                'productStatus': 'productStatus',
                'salesStatus': 'salesStatus',
                'deliveryCost': 'deliveryCost'
            },
            'params': {
                'api': None,
                'web': {
                    'page': '&page={}',
                    'keyword': '/s?order=desc&query={}&sort=relevance',
                    'negKeyword': '&excluded_query={}',
                    'searchRange': None,
                    'minPrice': '&min={}',
                    'maxPrice': '&max={}',
                    'productStatus': {
                        'all': None,
                        'brand_new': '&status=new',
                        # 'brand_new': '&status=5',
                        'almost_unused': '&status=4',
                        'no_scratches_or_stains': '&status=6',
                        'slight_scratches_or_stains': '&status=3',
                        'noticeable_scratches_or_stains': '&status=2'
                    },
                    'salesStatus': {
                        'all': None,
                        'selling': '&transaction=selling',
                        'soldout': '&transaction=soldout'
                    },
                    'deliveryCost': {
                        'all': None,
                        'free': '&carriage=1',
                        'required': '&carriage=2'
                    },
                    # 'category': {
                    #     'all': '',
                    #     'fashion': {
                    #         'ladies': '&category_id=10001',
                    #         'mens': '&category_id=10005',
                    #     },
                    #     'food-beverage-alcohol': {
                    #         'food': '&category_id=1125',
                    #         'beverage': '&category_id=1126',
                    #         'alcohol': '&category_id=1510'
                    #     },
                    #     'sports-outdoor': {
                    #         'sports': '&category_id=10014',
                    #         'outdoor': '&category_id=1582'
                    #     },
                    #     'diet-health': '&category_id=520',
                    #     'cosmetic-beauty': '&category_id=10004',
                    #     'smartphone-tablet-pc': {
                    #         'smartphone': '&category_id=667',
                    #         'tablet-pc': '&category_id=676'
                    #     },
                    #     'tv-audio-camera': {
                    #         'tv': '&category_id=688',
                    #         'audio': '&category_id=694',
                    #         'camera': '&category_id=682'
                    #     },
                    #     'home-appliances': {
                    #         'home-appliances': '&category_id=701',
                    #         'cooking-appliances': '&category_id=1361',
                    #         'health-appliances': '&category_id=718',
                    #         'beauty-appliances': '&category_id=718',
                    #         'air-conditioning': '&category_id=1394',
                    #     },
                    #     'furniture-interior': '&category_id=10009',
                    #     'daily-necessities-accessories': '&category_id=10009',
                    #     'pet': '&category_id=1113',
                    #     'handmade': '&category_id=10010',
                    #     'musical-instrument': '&category_id=10013',
                    #     'game': {
                    #         'video-game': '&category_id=786',
                    #         'trading-card': '&category_id=821',
                    #         'card-game': '&category_id=864',
                    #         'board-game': '&category_id=868',
                    #     },
                    #     'toy-hobby': '&category_id=10007',
                    #     'baby-kids-maternity': '&category_id=10003',
                    #     'car-bike': {
                    #         'car': '&category_id=1136',
                    #         'bike': '&category_id=1155',
                    #         'bicycle': '&category_id=1569'
                    #     },
                    #     'cd-music': '&category_id=762',
                    #     'dvd': '&category_id=752',
                    #     'book-magazine-cartoon': {
                    #         'book': '&category_id=733',
                    #         'magazine': '&category_id=746',
                    #         'cartoon': '&category_id=721',
                    #     },
                    #     'ticket': '&category_id=10008'
                    # },
                }
            }
        },
        'res': {
            'params': {
                'api': None,
                'web': {
                    'items': {
                        'key': '.item-box',
                        'attr': None
                    },
                    'item': None,
                    'title': {
                        'key': '.item-box__item-name span[itemprop="name"]',
                        'attr': None
                    },
                    'price': {
                        'key': '.item-box__item-price span[itemprop="price"]',
                        'attr': None
                    },
                    'image': {
                        'key': 'img',
                        'attr': 'data-original'
                    },
                    'detail': {
                        'key': '.link_search_image',
                        'attr': 'href'
                    },
                    'pages': {
                        'key': '.pagination > .last > a',
                        'attr': 'href'
                    }
                }
            }
        }
    },
}
# PROXY = {
#     'tor': 'socks5://127.0.0.1:9001',
#     'luminati': 'http://127.0.0.1:24005',
# }
