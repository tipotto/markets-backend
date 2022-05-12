from constants.util import PLATFORM_TYPE_API

SERVICE_NAME = 'mercari'
WEB_URL = 'https://jp.mercari.com'
API_URL = 'https://api.mercari.jp/v2/entities:search'
# AUTH_TOKEN_PATH = '/home/vagrant/workspace/markets/backend/app/python/mercari_cert.json'
AUTH_TOKEN_PATH = '/var/www/api/app/python/mercari_cert.json'
CONS = {
    'name': SERVICE_NAME,
    'type': PLATFORM_TYPE_API,
    'auth_token': AUTH_TOKEN_PATH,
    'data': {
        'req': {
            'url': {
                'web': WEB_URL,
                'api': API_URL
            },
            'headers': {
                "Host": "api.mercari.jp",
                "Sec-Ch-Ua": "\"Chromium\";v=\"96\", \" Not A;Brand\";v=\"99\"",
                "Sec-Ch-Ua-Mobile": "?0",
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.51 Safari/537.36",
                "Content-Type": "application/json;charset=UTF-8",
                "Accept": "application/json, text/plain, */*",
                "X-Platform": "web",
                "Sec-Ch-Ua-Platform": "\"Linux\"",
                "Origin": "https://jp.mercari.com",
                "Sec-Fetch-Site": "cross-site",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty",
                "Referer": "https://jp.mercari.com/",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "en-US,en;q=0.9"
            },
            'keys': {
                'page': 'pageToken',
                'keyword': 'keyword',
                'negKeyword': 'excludeKeyword',
                'searchRange': None,
                'minPrice': 'priceMin',
                'maxPrice': 'priceMax',
                'productStatus': 'itemConditionId',
                'salesStatus': 'status',
                'deliveryCost': 'shippingPayerId'
            },
            'params': {
                'api': {
                    "userId": "",
                    "pageSize": 120,
                    "pageToken": "",
                    "indexRouting": "INDEX_ROUTING_UNSPECIFIED",
                    "thumbnailTypes": [],
                    "searchCondition": {
                        "keyword": "",
                        "excludeKeyword": "",
                        "sort": "SORT_SCORE",
                        "order": "ORDER_DESC",
                        "status": [],
                        "sizeId": [],
                        "categoryId": [],
                        "brandId": [],
                        "sellerId": [],
                        "priceMin": 0,
                        "priceMax": 0,
                        "itemConditionId": [],
                        "shippingPayerId": [],
                        "shippingFromArea": [],
                        "shippingMethod": [],
                        "colorId": [],
                        "hasCoupon": False,
                        "attributes": [],
                        "itemTypes": [],
                        "skuIds": []
                    },
                    "defaultDatasets": [],
                    "serviceFrom": "suruga"
                },
                'web': {
                    'page': None,
                    'keyword': None,
                    'negKeyword': None,
                    'searchRange': None,
                    'minPrice': None,
                    'maxPrice': None,
                    'productStatus': {
                        'all': [1, 2, 3, 4, 5],
                        'brand_new': 1,
                        'almost_unused': 2,
                        'no_scratches_or_stains': 3,
                        'slight_scratches_or_stains': 4,
                        'noticeable_scratches_or_stains': 5
                    },
                    'salesStatus': {
                        # 'all': [],
                        'all': ['STATUS_ON_SALE', 'STATUS_SOLD_OUT', 'STATUS_TRADING'],
                        'selling': ['STATUS_ON_SALE'],
                        'soldout': ['STATUS_SOLD_OUT']
                    },
                    'deliveryCost': {
                        'all': [1, 2],
                        'free': [2],
                        'required': [1]
                    },
                    'category': None
                }
            }
        },
        'res': {
            'params': {
                'api': {
                    'items': {
                        'key': 'items',
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
                        'key': 'thumbnails',
                        'attr': (0,)
                    },
                    'detail': {
                        'key': 'id',
                        'attr': None
                    },
                    'pages': None,
                },
                'web': None
            }
        }
    },
}
