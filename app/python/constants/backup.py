WEBSITE_URL = ''
CONS = {
    'url': {
        'web': WEBSITE_URL,
        'api': None
    },
    'auth_token': None,
    'data': {
        'req': {
            'headers': None,
            'referer': WEBSITE_URL + '/',
            'keys': None,
            'params': {
                'api': None,
                'web': {
                    'search': '',
                    'analyze': '',
                    'negKeyword': '',
                    'minPrice': '&minPrice={}',
                    'maxPrice': '&maxPrice={}',
                }
            }
        },
        'res': {
            'keys': None,
            'selectors': {}
        }
    },
}
