SERVICE_NAME = 'mercari'
SITE_URL = 'https://www.mercari.com'

PROXY = {
    'tor': 'socks5://127.0.0.1:9000',
    'luminati': 'http://127.0.0.1:24004',
}

DATA = {
    'platform': SERVICE_NAME,
    'siteUrl': SITE_URL,
    'referer': SITE_URL + '/jp/',
    'proxy': PROXY['tor'],
    'query': {
        'search': '/jp/search/?page={0}&keyword={1}&sort_order=like_desc',
        # 'search': '/jp/search/?page={0}&keyword={1}',
        # 'search': '/jp/search/?keyword={}',
        'analyze': {
            'market': '',
            'price': {
                'like': '/jp/search/?page={0}&keyword={1}&sort_order=like_desc&status_trading_sold_out=1',
                # 'asc': '/jp/search/?page={0}&keyword={1}&sort_order=price_asc&status_trading_sold_out=1',
                # 'desc': '/jp/search/?page={0}&keyword={1}&sort_order=price_desc&status_trading_sold_out=1',
            },
        },
        'category': {
            'all': '&category_root=',
            'fashion': {
                'ladies': '&category_root=1&category_child=',
                'mens': '&category_root=2&category_child=',
            },
            'food-beverage-alcohol': {
                'food': '&category_root=10&category_child=112',
                'beverage': '&category_root=10&category_child=929',
                'alcohol': '&category_root=10&category_child=929'
            },
            'sports-outdoor': {
                'sports': '&category_root=8&category_child=',
                'outdoor': '&category_root=8&category_child=1164'
            },
            'diet-health': '&category_root=6&category_child=94',
            'cosmetic-beauty': '&category_root=6&category_child=',
            'smartphone-tablet-pc': {
                'smartphone': '&category_root=7&category_child=100',
                'tablet-pc': '&category_root=7&category_child=96'
            },
            'tv-audio-camera': {
                'tv': '&category_root=7&category_child=98',
                'audio': '&category_root=7&category_child=99',
                'camera': '&category_root=7&category_child=97'
            },
            'home-appliances': {
                'home-appliances': '&category_root=7&category_child=101',
                'cooking-appliances': '&category_root=7&category_child=102',
                'health-appliances': '&category_root=7&category_child=1237',
                'beauty-appliances': '&category_root=7&category_child=1237',
                'air-conditioning': '&category_root=7&category_child=1243',
            },
            'furniture-interior': '&category_root=4&category_child=',
            'daily-necessities-accessories': '&category_root=4&category_child=',
            'pet': '&category_root=10&category_child=69',
            'handmade': '&category_root=9&category_child=',
            'musical-instrument': '&category_root=1328&category_child=79',
            'game': {
                'video-game': '&category_root=5&category_child=76',
                'trading-card': '&category_root=1328&category_child=82',
                'card-game': '&category_root=1328&category_child=86&category_grand_child%5B764%5D=1',
                'board-game': '&category_root=1328&category_child=86&category_grand_child%5B768%5D=1',
            },
            'toy-hobby': '&category_root=1328&category_child=',
            'baby-kids-maternity': '&category_root=3&category_child=',
            'car-bike': {
                'car': '&category_root=1318&category_child=1329',
                'bike': '&category_root=1318&category_child=949',
                'bicycle': '&category_root=8&category_child=1139&category_grand_child%5B900%5D=1'
            },
            'cd-music': '&category_root=5&category_child=75',
            'dvd': '&category_root=5&category_child=74',
            'book-magazine-cartoon': {
                'book': '&category_root=5&category_child=72',
                'magazine': '&category_root=5&category_child=73',
                'cartoon': '&category_root=5&category_child=71',
            },
            'ticket': '&category_root=1027&category_child='
        },
        'minPrice': '&price_min={}',
        'maxPrice': '&price_max={}',
        'productStatus': {
            'all': '&condition_all=1&item_condition_id%5B1%5D=1&item_condition_id%5B2%5D=1&item_condition_id%5B3%5D=1&item_condition_id%5B4%5D=1&item_condition_id%5B5%5D=1&item_condition_id%5B6%5D=1',
            'brand_new': '&item_condition_id%5B1%5D=1',
            'almost_unused': '&item_condition_id%5B2%5D=1',
            'no_scratches_or_stains': '&item_condition_id%5B3%5D=1',
            'slight_scratches_or_stains': '&item_condition_id%5B4%5D=1',
            'noticeable_scratches_or_stains': '&item_condition_id%5B5%5D=1'
        },
        'salesStatus': {
            'all': '&status_all=1&status_on_sale=1&status_trading_sold_out=1',
            'selling': '&status_on_sale=1',
            'soldout': '&status_trading_sold_out=1'
        },
        'deliveryCost': {
            'all': '&shipping_payer_all=1&shipping_payer_id%5B1%5D=1&shipping_payer_id%5B2%5D=1',
            'free': '&shipping_payer_id%5B2%5D=1',
            'required': '&shipping_payer_id%5B1%5D=1'
        },
        # 'sortOrder': {
        #     'asc': '&sort_order=price_asc',
        #     'desc': '&sort_order=price_desc'
        # },
    },
    'items': {'selector': '.items-box'},
    'title': {
        'selector': 'a > div.items-box-body > h3',
        'attr': ''
    },
    'price': {'selector': 'a > div.items-box-body > div.items-box-num > div.items-box-price'},
    'image': {
        'selector': 'a > figure.items-box-photo > img',
        'attr': 'data-src'
    },
    'detail': {
        'selector': 'a',
        'attr': 'href'
    },
    'likes': {
        'selector': 'a > div.items-box-body > div.items-box-num > div:last-child > span',
    }
}
