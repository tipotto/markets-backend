from constants.util import PLATFORM_TYPE_API

SERVICE_NAME = 'rakuten'
WEB_URL = 'https://www.rakuten.co.jp'
API_URL = 'https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706'
APP_ID = '1058593024773857397'
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
                'page': 'page',
                'keyword': 'keyword',
                'negKeyword': 'NGKeyword',
                'searchRange': 'field',
                'minPrice': 'minPrice',
                'maxPrice': 'maxPrice',
                'productStatus': 'used',
                'salesStatus': 'availability',
                'deliveryCost': 'postageFlag'
            },
            'params': {
                'api': {
                    "applicationId": APP_ID,
                    "format": "json",
                    "hits": 30,
                    "imageFlag": 1,
                },
                'web': {
                    'page': None,
                    'keyword': None,
                    'negKeyword': None,
                    'searchRange': {
                        # 'title': 1,
                        'title': 0,
                        'title-desc': 0
                    },
                    'minPrice': None,
                    'maxPrice': None,
                    'productStatus': {
                        'all': None,
                        'new': 0,
                        'used': 1
                    },
                    'salesStatus': {
                        'all': 0,
                        'selling': 1,
                        'soldout': None
                    },
                    'deliveryCost': {
                        'all': 0,
                        'free': 1,
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
                        'key': 'Items',
                        'attr': None
                    },
                    'item': {
                        'key': 'Item',
                        'attr': None
                    },
                    'title': {
                        'key': 'itemName',
                        'attr': None
                    },
                    'price': {
                        'key': 'itemPrice',
                        'attr': None
                    },
                    'image': {
                        'key': 'mediumImageUrls',
                        'attr': (0, 'imageUrl')
                    },
                    'detail': {
                        'key': 'itemUrl',
                        'attr': None
                    },
                    'pages': {
                        'key': 'pageCount',
                        'attr': None
                    },
                },
                'web': None
            }
        }
    },
}
