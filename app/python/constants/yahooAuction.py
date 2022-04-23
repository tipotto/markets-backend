from constants.util import PLATFORM_TYPE_WEB

SERVICE_NAME = 'yahoo-auction'
WEB_URL = 'https://auctions.yahoo.co.jp'
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
                'searchRange': 'searchRange',
                'minPrice': 'minPrice',
                'maxPrice': 'maxPrice',
                'productStatus': 'productStatus',
                'salesStatus': None,
                'deliveryCost': 'deliveryCost'
            },
            'params': {
                'api': None,
                'web': {
                    'page': '&b={}',
                    'keyword': '/search/search?va={}&fixed=1&exflg=1&n=50',
                    'negKeyword': '&ve={}',
                    'searchRange': {
                        'title': '&ngrm=0&f=0x2',
                        'title-desc': '&ngrm=2&f=0x4'
                    },
                    'minPrice': '&aucminprice={}',
                    'maxPrice': '&aucmaxprice={}',
                    'productStatus': {
                        'all': None,
                        'brand_new': 1,
                        'almost_unused': 3,
                        'no_scratches_or_stains': 4,
                        'slight_scratches_or_stains': 5,
                        'noticeable_scratches_or_stains': 6
                    },
                    'salesStatus': None,
                    'deliveryCost': {
                        'all': None,
                        'free': '&pstagefree=1',
                        'required': None
                    },
                }
            }
        },
        'res': {
            'params': {
                'api': None,
                'web': {
                    'items': {
                        # 'key': 'div.Products__list > ul.Products__items > li.Product',
                        'key': '.Product',
                        'attr': None
                    },
                    'item': None,
                    'title': {
                        # 'key': 'h3.Product__title > a.Product__titleLink',
                        'key': '.Product__titleLink',
                        'attr': None
                    },
                    'price': {
                        # 'key': 'div.Product__priceInfo > span.Product__price > span.Product__priceValue',
                        'key': '.Product__priceValue',
                        'attr': None
                    },
                    'image': {
                        # 'key': 'div.Product__image > a.Product__imageLink > img.Product__imageData',
                        'key': 'img',
                        'attr': 'src'
                    },
                    'detail': {
                        # 'key': 'h3.Product__title > a.Product__titleLink',
                        'key': '.Product__titleLink',
                        'attr': 'href'
                    },
                    'pages': {
                        # 'key': 'div.Result__header ul.Tab__items > li:last-of-type > div.Tab__itemInner > span.Tab__subText',
                        'key': '.Result__header ul > li:last-of-type .Tab__subText',
                        'attr': None
                    },
                },
            },
        }
    },
}
# PROXY = {
#     'tor': 'socks5://127.0.0.1:9000',
#     'luminati': 'http://127.0.0.1:24004',
# }
