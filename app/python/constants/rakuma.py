SERVICE_NAME = 'rakuma'
SITE_URL = 'https://fril.jp'

PROXY = {
    'tor': 'socks5://127.0.0.1:9001',
    'luminati': 'http://127.0.0.1:24005',
}

DATA = {
    'platform': SERVICE_NAME,
    'siteUrl': SITE_URL,
    'referer': SITE_URL + '/',
    'proxy': PROXY['tor'],
    'query': {
        'search': '/s?order=desc&page={0}&query={1}&sort=relevance',
        # 'search': '/search/{1}/page/{0}',
        'category': {
            'all': '',
            'fashion': {
                'ladies': '&category_id=10001',
                'mens': '&category_id=10005',
            },
            'food-beverage-alcohol': {
                'food': '&category_id=1125',
                'beverage': '&category_id=1126',
                'alcohol': '&category_id=1510'
            },
            'sports-outdoor': {
                'sports': '&category_id=10014',
                'outdoor': '&category_id=1582'
            },
            'diet-health': '&category_id=520',
            'cosmetic-beauty': '&category_id=10004',
            'smartphone-tablet-pc': {
                'smartphone': '&category_id=667',
                'tablet-pc': '&category_id=676'
            },
            'tv-audio-camera': {
                'tv': '&category_id=688',
                'audio': '&category_id=694',
                'camera': '&category_id=682'
            },
            'home-appliances': {
                'home-appliances': '&category_id=701',
                'cooking-appliances': '&category_id=1361',
                'health-appliances': '&category_id=718',
                'beauty-appliances': '&category_id=718',
                'air-conditioning': '&category_id=1394',
            },
            'furniture-interior': '&category_id=10009',
            'daily-necessities-accessories': '&category_id=10009',
            'pet': '&category_id=1113',
            'handmade': '&category_id=10010',
            'musical-instrument': '&category_id=10013',
            'game': {
                'video-game': '&category_id=786',
                'trading-card': '&category_id=821',
                'card-game': '&category_id=864',
                'board-game': '&category_id=868',
            },
            'toy-hobby': '&category_id=10007',
            'baby-kids-maternity': '&category_id=10003',
            'car-bike': {
                'car': '&category_id=1136',
                'bike': '&category_id=1155',
                'bicycle': '&category_id=1569'
            },
            'cd-music': '&category_id=762',
            'dvd': '&category_id=752',
            'book-magazine-cartoon': {
                'book': '&category_id=733',
                'magazine': '&category_id=746',
                'cartoon': '&category_id=721',
            },
            'ticket': '&category_id=10008'
        },
        'minPrice': 'min={}',
        'maxPrice': 'max={}',
        'productStatus': {
            'all': '',
            'brand_new': '&status=new',
            # 'brand_new': '&status=5',
            'almost_unused': '&status=4',
            'no_scratches_or_stains': '&status=6',
            'slight_scratches_or_stains': '&status=3',
            'noticeable_scratches_or_stains': '&status=2'
        },
        'salesStatus': {
            'all': '',
            'selling': '&transaction=selling',
            'soldout': '&transaction=soldout'
        },
        'deliveryCost': {
            'all': '',
            'free': '&carriage=1',
            'required': '&carriage=2'
        },
        'sortOrder': {
            'asc': '&order=asc&sort=sell_price',
            'desc': '&order=desc&sort=sell_price'
        },
    },
    'items': {'selector': '.item'},
    'title': {
        'selector': '.item-box__text-wrapper > .item-box__item-name > .link_search_title > span',
        'attr': ''
    },
    'price': {'selector': '.item-box__text-wrapper > div:nth-of-type(2) > .item-box__item-price > span:nth-child(2)'},
    'image': {
        'selector': '.item-box__image-wrapper > a > img',
        'attr': 'data-original'
    },
    'detail': {
        'selector': '.item-box__image-wrapper > a',
        'attr': 'href'
    }
}
