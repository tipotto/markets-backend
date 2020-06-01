MERCARI = 'mercari'
RAKUTEN = 'rakuten'
PAYPAY = 'paypay'

SITE_URL = {
    MERCARI: 'https://www.mercari.com',
    RAKUTEN: 'https://fril.jp',
    PAYPAY: 'https://paypayfleamarket.yahoo.co.jp'
}

PROXY = {
    MERCARI: {
        'tor': 'socks5://127.0.0.1:9000',
        'luminati': 'http://127.0.0.1:24004',
    },
    RAKUTEN: {
        'tor': 'socks5://127.0.0.1:9001',
        'luminati': 'http://127.0.0.1:24005',
    },
    PAYPAY: {
        'tor': 'socks5://127.0.0.1:9002',
        'luminati': 'http://127.0.0.1:24006',
    }
}

HTTP_HEADER = {
    MERCARI: {
        'referer': SITE_URL[MERCARI] + '/jp/',
    },
    RAKUTEN: {
        'referer': SITE_URL[RAKUTEN] + '/',
    },
    PAYPAY: {
        'referer': SITE_URL[PAYPAY] + '/search/%E6%97%A5%E5%90%91%E5%9D%8246%20%E6%B8%A1%E9%82%89%E7%BE%8E%E7%A9%82?page=1',
    },
}

MERCARI_PARAM = {
    'header': HTTP_HEADER[MERCARI],
    'proxy': PROXY[MERCARI]['tor'],
    'platform': MERCARI,
    'siteUrl': SITE_URL[MERCARI],
    'searchUrl': SITE_URL[MERCARI] + '/jp/search/?keyword={}&status_on_sale=1',
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
}

RAKUTEN_PARAM = {
    'header': HTTP_HEADER[RAKUTEN],
    'proxy': PROXY[RAKUTEN]['tor'],
    'siteUrl': SITE_URL[RAKUTEN],
    'searchUrl': SITE_URL[RAKUTEN] + '/search/{}',
    'platform': RAKUTEN,
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

PAYPAY_PARAM = {
    'header': HTTP_HEADER[PAYPAY],
    'proxy': PROXY[PAYPAY]['tor'],
    'siteUrl': SITE_URL[PAYPAY],
    'searchUrl': SITE_URL[PAYPAY] + '/search/{}?open=1',
    'platform': PAYPAY,
    'items': {'selector': '.ItemThumbnail__Component-tlgyjt-0'},
    'title': {
        'selector': '.ItemThumbnail__Image-tlgyjt-1',
        'attr': 'alt'
    },
    'price': {'selector': '.ItemThumbnail__Price-tlgyjt-3'},
    'image': {
        'selector': '.ItemThumbnail__Image-tlgyjt-1',
        'attr': 'src'
    },
    'detail': {
        'selector': '',
        'attr': 'href'
    }
}
