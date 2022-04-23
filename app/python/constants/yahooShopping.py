from constants.util import PLATFORM_TYPE_API

SERVICE_NAME = 'yahoo-shopping'
WEB_URL = 'https://shopping.yahoo.co.jp'
API_URL = 'https://shopping.yahooapis.jp/ShoppingWebService/V3/itemSearch'
APP_ID = 'dj00aiZpPTdhbmxFOGhUZ0lSRCZzPWNvbnN1bWVyc2VjcmV0Jng9ZWU-'
CONS = {
    'name': SERVICE_NAME,
    'type': PLATFORM_TYPE_API,
    'auth_token': None,
    'data': {
        'req': {
            'url': {
                'web': WEB_URL,
                'api': API_URL
            },
            'headers': None,
            'keys': {
                'page': 'start',
                'keyword': 'query',
                'negKeyword': None,
                'searchRange': None,
                'minPrice': 'price_from',
                'maxPrice': 'price_to',
                'productStatus': 'condition',
                'salesStatus': 'in_stock',
                'deliveryCost': 'shipping'
            },
            'params': {
                'api': {
                    "appid": APP_ID,
                    "results": 50,
                    "image_size": 300,
                },
                'web': {
                    'page': None,
                    'keyword': None,
                    'negKeyword': None,
                    'searchRange': None,
                    'minPrice': None,
                    'maxPrice': None,
                    'productStatus': {
                        'all': None,
                        'new': 'new',
                        'used': 'used'
                    },
                    'salesStatus': {
                        'all': 'True',
                        'selling': 'True',
                        'soldout': 'False'
                    },
                    'deliveryCost': {
                        'all': None,
                        'free': 'free',
                        'required': None
                    },
                    'category': None
                }
            }
        },
        'res': {
            'params': {
                'api': {
                    'items': {
                        'key': 'hits',
                        'attr': None
                    },
                    'item': None,
                    'title': {
                        'key': 'name',
                        'attr': None
                    },
                    'price': {
                        'key': 'price',
                        'attr': None
                    },
                    'image': {
                        'key': 'exImage',
                        'attr': ('url',)
                    },
                    'detail': {
                        'key': 'url',
                        'attr': None
                    },
                    'pages': {
                        'key': 'totalResultsAvailable',
                        'attr': None
                    },
                },
                'web': None
            },
        }
    },
}
