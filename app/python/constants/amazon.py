from constants.util import PLATFORM_TYPE_WEB

SERVICE_NAME = 'amazon'
WEB_URL = 'https://www.amazon.co.jp'
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
                'minPrice': None,
                'maxPrice': None,
                'productStatus': 'productStatus',
                'salesStatus': None,
                'deliveryCost': 'deliveryCost'
            },
            'params': {
                'api': None,
                'web': {
                    'page': '&page={}',
                    'keyword': '/s?k={}',
                    'negKeyword': None,
                    'searchRange': None,
                    'minPrice': None,
                    'maxPrice': None,
                    'productStatus': {
                        'all': None,
                        'new': '&ref=sr_nr_p_n_condition-type_1',
                        'used': '&ref=sr_nr_p_n_condition-type_2'
                    },
                    'salesStatus': None,
                    'deliveryCost': {
                        'all': None,
                        'free': '&rh=p_76%3A2227293051',
                        'required': None
                    },
                    'category': None
                }
            }
        },
        'res': {
            'params': {
                'api': None,
                'web': {
                    'items': {
                        'key': '#search div[data-component-type="s-search-result"]',
                        'attr': None
                    },
                    'item': None,
                    'title': {
                        'key': 'img',
                        'attr': 'alt'
                    },
                    'price': {
                        # 'key': 'span.a-price-whole',
                        'key': '.a-price-whole',
                        'attr': None
                    },
                    'image': {
                        # 'key': 'img.s-image',
                        'key': 'img',
                        'attr': 'src'
                    },
                    'detail': {
                        'key': 'span[data-component-type="s-product-image"] a',
                        'attr': 'href'
                    },
                    'pages': {
                        'key': 'span[data-component-type="s-result-info-bar"] h1 span:first-of-type',
                        'attr': None
                    },
                },
            },
        }
    },
}
