MERCARI = {
    'socks': 'socks5://127.0.0.1:9000',
    'platform': 'mercari',
    'url': 'https://www.mercari.com/jp/search/?keyword={}&status_on_sale=1',
    'items': {'selector': '.items-box'},
    'title': {'selector': 'a > div.items-box-body > h3'},
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

RAKUTEN = {
    'socks': 'socks5://127.0.0.1:9001',
    'url': 'https://fril.jp/search/{}',
    'platform': 'rakuten',
    'items': {'selector': '.item'},
    'title': {'selector': '.item-box__text-wrapper > .item-box__item-name > .link_search_title > span'},
    'price': {'selector': '.item-box__text-wrapper > div:nth-of-type(2) > .item-box__item-price > span:nth-child(2)'},
    'image': {
        'selector': '.item-box__image-wrapper > a > img',
        'attr': 'src'
    },
    'detail': {
        'selector': '.item-box__image-wrapper > a',
        'attr': 'href'
    }
}
