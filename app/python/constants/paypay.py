from constants.util import PLATFORM_TYPE_WEB

SERVICE_NAME = 'paypay'
WEB_URL = 'https://paypayfleamarket.yahoo.co.jp'
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
                'negKeyword': None,
                'searchRange': None,
                'minPrice': 'minPrice',
                'maxPrice': 'maxPrice',
                'productStatus': 'productStatus',
                'salesStatus': 'salesStatus',
                'deliveryCost': None
            },
            'params': {
                'api': None,
                'web': {
                    'page': '&page={}',
                    'keyword': '/search/{}?sort=ranking&order=asc',
                    'negKeyword': None,
                    'searchRange': None,
                    'minPrice': '&minPrice={}',
                    'maxPrice': '&maxPrice={}',
                    'productStatus': {
                        'all': None,
                        'brand_new': '&conditions=NEW',
                        'almost_unused': '&conditions=USED10',
                        'no_scratches_or_stains': '&conditions=USED20',
                        'slight_scratches_or_stains': '&conditions=USED40',
                        'noticeable_scratches_or_stains': '&conditions=USED60'
                    },
                    'salesStatus': {
                        'all': None,
                        'selling': '&open=1',
                        'soldout': '&sold=1'
                    },
                    # 基本的に全て送料無料のため
                    'deliveryCost': None,
                    # 'category': {
                    #     'all': '',
                    #     'fashion': {
                    #         'ladies': '&categoryIds=13457%2C2494',
                    #         'mens': '&categoryIds=13457%2C2495',
                    #     },
                    #     'food-beverage-alcohol': {
                    #         'food': '&categoryIds=2498',
                    #         'beverage': '&categoryIds=2498%2C2499',
                    #         'alcohol': '&categoryIds=2498%2C2499'
                    #     },
                    #     'sports-outdoor': {
                    #         'sports': '&categoryIds=2512',
                    #         'outdoor': '&categoryIds=2513'
                    #     },
                    #     'diet-health': '&categoryIds=2500',
                    #     'cosmetic-beauty': '&categoryIds=2501',
                    #     'smartphone-tablet-pc': {
                    #         'smartphone': '&categoryIds=2502%2C38338',
                    #         'tablet-pc': '&categoryIds=2502%2C21076'
                    #     },
                    #     'tv-audio-camera': {
                    #         'tv': '&categoryIds=2504%2C635',
                    #         'audio': '&categoryIds=2504%2C660',
                    #         'camera': '&categoryIds=2504%2C2443'
                    #     },
                    #     'home-appliances': {
                    #         'home-appliances': '&categoryIds=2505%2C5300',
                    #         'cooking-appliances': '&categoryIds=2505%2C587',
                    #         'health-appliances': '&categoryIds=2505%2C1919',
                    #         'beauty-appliances': '&categoryIds=2505%2C1987',
                    #         'air-conditioning': '&categoryIds=2505%2C4740',
                    #     },
                    #     'furniture-interior': '&categoryIds=2506',
                    #     'daily-necessities-accessories': '&categoryIds=2508',
                    #     'pet': '&categoryIds=2509',
                    #     'handmade': '&categoryIds=2510%2C2266',
                    #     'musical-instrument': '&categoryIds=2510%2C2327',
                    #     'game': {
                    #         'video-game': '&categoryIds=2511%2C2161',
                    #         'trading-card': '&categoryIds=2511%2C2420',
                    #         'card-game': '&categoryIds=2511%2C2165',
                    #         'board-game': '&categoryIds=2511%2C2169',
                    #     },
                    #     'toy-hobby': '&categoryIds=2511',
                    #     'baby-kids-maternity': '&categoryIds=2497',
                    #     'car-bike': {
                    #         'car': '&categoryIds=2514%2C41234',
                    #         'bike': '&categoryIds=2514%2C41235',
                    #         'bicycle': '&categoryIds=2514%2C3174'
                    #     },
                    #     'cd-music': '&categoryIds=2516',
                    #     'dvd': '&categoryIds=2517',
                    #     'book-magazine-cartoon': {
                    #         'book': '&categoryIds=10002',
                    #         'magazine': '&categoryIds=10002%2C10003',
                    #         'cartoon': '&categoryIds=10002%2C10251',
                    #     },
                    #     'ticket': '&categoryIds=2516%2C16509'
                    # },
                }
            }
        },
        'res': {
            'params': {
                'api': None,
                'web': {
                    'items': {
                        'key': '#itm > a',
                        'attr': None
                    },
                    'item': None,
                    'title': {
                        'key': 'img',
                        'attr': 'alt'
                    },
                    'price': {
                        'key': 'p',
                        'attr': None
                    },
                    'image': {
                        'key': 'img',
                        'attr': 'src'
                    },
                    'detail': {
                        'key': None,
                        'attr': 'href'
                    },
                    'pages': {
                        'key': '.Pagination__ItemCount-ee0830-4 > .Typography__Component-sc-10fxrsq-0',
                        'attr': None
                    },
                },
            },
        }
    },
}
# PROXY = {
#     'tor': 'socks5://127.0.0.1:9002',
#     'luminati': 'http://127.0.0.1:24006',
# }
