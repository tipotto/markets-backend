import json
import uuid
import random
import re
import numpy as np
import asyncio
from aiohttp import ClientSession
from fake_headers import Headers
from urllib import parse
from constants import mercari, rakuma, paypay, yahooAuction, amazon, rakuten, yahooShopping
from constants.util import PLATFORM_TYPE_WEB, PLATFORM_TYPE_API, KEYWORD_REG_EXP, OS_LIST, BROWSER_LIST, HEADERS_DICT, SEARCH_BLACKLIST, ANALYZE_BLACKLIST
from services.keep_alive_client_request_class import KeepAliveClientRequest


def get_params_by_platform(plf):
    if plf == mercari.SERVICE_NAME:
        return mercari.CONS
    elif plf == rakuma.SERVICE_NAME:
        return rakuma.CONS
    elif plf == paypay.SERVICE_NAME:
        return paypay.CONS
    elif plf == yahooAuction.SERVICE_NAME:
        return yahooAuction.CONS
    elif plf == amazon.SERVICE_NAME:
        return amazon.CONS
    elif plf == rakuten.SERVICE_NAME:
        return rakuten.CONS
    elif plf == yahooShopping.SERVICE_NAME:
        return yahooShopping.CONS


def split_keyword(kw):

    # keywordの先頭と末尾の空白を削除
    removed = kw.strip()

    # keywordに空白（全角、半角、タブ文字）が含まれているかチェック
    # 含まれていれば、空白で分割してリストにする
    # 含まれていなければ、keywordリストを作成
    if re.search(KEYWORD_REG_EXP, removed):
        return re.split(KEYWORD_REG_EXP, removed)

    return [kw]


def create_keyword_list(form):

    if form['searchRange'] == 'title-desc':
        return []

    return split_keyword(form['keyword'])


def create_neg_keyword_list(form):

    if not form['negKeyword']:
        return []

    return split_keyword(form['negKeyword'])


def should_exclude_by_keyword(form, keys, kws, title):

    if keys['searchRange'] is not None:
        return False

    if form['searchRange'] == 'title-desc':
        return False

    if is_each_keyword_contained(kws, title) is True:
        return False

    return True


def should_exclude_by_neg_keyword(keys, neg_kws, title):

    if keys['negKeyword'] is not None:
        return False

    if len(neg_kws) == 0:
        return False

    if is_neg_keyword_contained(neg_kws, title) is False:
        return False

    return True


def should_exclude_by_price(form, price_dict, keys):

    # 価格未設定の商品はスルー
    if not price_dict:
        return True

    # 価格が0円の場合はスルー
    price = price_dict['int']
    if price == 0:
        return True

    # Analyzeの場合は何もせずに終了
    if ('minPrice' not in form) or ('maxPrice' not in form):
        return False

    # Amazonでない場合は何もせずに終了
    if (keys['minPrice'] is not None) or (keys['maxPrice'] is not None):
        return False

    min_price = form['minPrice']
    max_price = form['maxPrice']

    if min_price > 0 and max_price > 0:
        if (min_price <= price) and (price <= max_price):
            return False
        return True

    if min_price > 0:
        if min_price <= price:
            return False
        return True

    if max_price > 0:
        if price <= max_price:
            return False
        return True

    # if min_price <= 0 and max_price <= 0:
    return False


def should_exit_by_sales_status(form, cons):

    if form['salesStatus'] != 'soldout':
        return False

    cons_req = cons['data']['req']
    keys = cons_req['keys']
    cons_web = cons_req['params'][PLATFORM_TYPE_WEB]

    if (keys['salesStatus'] is not None) and (cons_web['salesStatus']['soldout'] is not None):
        return False

    return True


def url_encode(val):
    return parse.quote(val)


def add_price_comma(price):
    return '{:,}'.format(price)


async def fetch_html(url, hdrs, **kwargs):
    # 以下のエラーの発生を抑えるために、KeepAliveClientRequestクラスを設定
    # aiohttp.client_exceptions.ClientPayloadError: Response payload is not completed
    async with ClientSession(request_class=KeepAliveClientRequest, headers=hdrs) as session:
        async with session.get(url, **kwargs) as resp:
            return (await resp.text())


async def fetch_json_by_get(url, params):
    async with ClientSession() as session:
        async with session.get(url, params=params) as resp:
            return (await resp.json())


async def fetch_json_by_post(url, hdrs, json):
    async with ClientSession(headers=hdrs) as session:
        async with session.post(url, json=json) as resp:
            return (await resp.json())


# async def get_dynamic_page(url):
#     try:
#         splash_url = 'http://localhost:8050/render.html'
#         data = {
#             'url': url,
#             'wait': 0.5,
#             # 'engine': 'chromium'
#         }

#         async with ClientSession() as session:
#             async with session.post(splash_url, json=data) as resp:
#                 return (await resp.text())

#     except Exception:
#         raise


def generate_headers(cons_req):
    if cons_req['headers'] is not None:
        return cons_req['headers']

    os = random.choice(OS_LIST)
    browser = random.choice(BROWSER_LIST)
    headers_type = os + '-' + browser
    headers = HEADERS_DICT[headers_type]

    fake_headers = Headers(
        browser=browser,
        os=os,
        headers=False
    ).generate()

    headers['User-Agent'] = fake_headers['User-Agent']
    headers['Referer'] = cons_req['url'][PLATFORM_TYPE_WEB] + '/'
    return headers


def generate_search_url(form, cons, plf):
    cons_req = cons['data']['req']
    return cons_req['url'][PLATFORM_TYPE_WEB] + generate_params(form, cons, plf)


def get_auth_token(cons):
    token_path = cons['auth_token']
    f = open(token_path)
    return json.load(f)


def set_auth_token(cons, params, plf):
    if plf != mercari.SERVICE_NAME:
        return None, params

    headers = generate_headers(cons['data']['req'])
    dict = get_auth_token(cons)
    headers['Dpop'] = dict['dpop']
    params['searchSessionId'] = dict['searchSessionId']
    return headers, params


def get_start_item_index(page, item_count):
    return (item_count * (page - 1)) + 1


def set_get_param(req_val, prms):
    if req_val is None:
        return prms

    prms += req_val
    return prms


def set_post_param(req_key, req_val, prms, plf):
    if req_val is None:
        return prms

    if plf == mercari.SERVICE_NAME:
        prms['searchCondition'][req_key] = req_val
    else:
        prms[req_key] = req_val

    return prms


def format(text, val):
    if type(val) is str:
        return text.format(url_encode(val))
    return text.format(val)


def generate_params(form, cons, plf):

    def _params():
        if type == PLATFORM_TYPE_WEB:
            return ''
        return cons_prms[PLATFORM_TYPE_API]

    def _blacklist():
        if 'page' in form:
            return SEARCH_BLACKLIST
        return ANALYZE_BLACKLIST

    type = cons['type']
    cons_data = cons['data']
    cons_req = cons_data['req']
    keys = cons_req['keys']
    cons_prms = cons_req['params']
    cons_web = cons_prms[PLATFORM_TYPE_WEB]

    p = _params()
    for key, val in form.items():
        if key in _blacklist():
            continue

        if key == 'keyword':
            p = set_kw_param(key, val, keys[key], type, plf, p, cons_web)

        elif key == 'negKeyword':
            p = set_neg_kw_param(key, val, keys[key], type, plf, p, cons_web)

        elif key == 'minPrice' or key == 'maxPrice':
            p = set_price_param(key, val, keys[key], type, plf, p, cons_web)

        elif key == 'productStatus':
            p = set_product_status_param(key, val, keys[key], type, plf, p, cons_web)

        elif key == 'page':
            p = set_page_param(key, val, keys[key], type, plf, p, cons_web)

        else:
            # searchRange, salesStatus, deliveryCost
            p = set_param(key, val, keys[key], type, plf, p, cons_web)

    return p


def set_page_param(key, val, req_key, type, plf, prms, cons_web):
    if req_key is None:
        return prms

    if type == PLATFORM_TYPE_WEB:
        return set_get_param(format(cons_web[key], val), prms)

    if plf == mercari.SERVICE_NAME:
        page_token = 'v1:' + str(0 if val == 0 else val - 1)
        return set_post_param(req_key, page_token, prms, plf)

    elif plf == yahooShopping.SERVICE_NAME:
        start_index = get_start_item_index(val, 50)
        return set_post_param(req_key, start_index, prms, plf)

    return set_post_param(req_key, val, prms, plf)


def set_kw_param(key, val, req_key, type, plf, prms, cons_web):
    if req_key is None:
        return prms

    if type == PLATFORM_TYPE_WEB:
        return set_get_param(format(cons_web[key], val), prms)
    return set_post_param(req_key, val, prms, plf)


def set_neg_kw_param(key, val, req_key, type, plf, prms, cons_web):
    if req_key is None:
        return prms

    if not val:
        return prms

    if type == PLATFORM_TYPE_WEB:
        return set_get_param(format(cons_web[key], val), prms)
    return set_post_param(req_key, val, prms, plf)


def set_price_param(key, val, req_key, cons_type, plf, prms, cons_web):

    if req_key is None:
        return prms

    if val <= 0:
        return prms

    if cons_type == PLATFORM_TYPE_WEB:
        return set_get_param(format(cons_web[key], val), prms)
    return set_post_param(req_key, val, prms, plf)


def set_param(key, val, req_key, type, plf, prms, cons_web):
    if req_key is None:
        return prms

    if type == PLATFORM_TYPE_WEB:
        return set_get_param(cons_web[key][val], prms)
    return set_post_param(req_key, cons_web[key][val], prms, plf)


def set_product_status_get_param(val_arr, plf, prms, cons_ps):
    if 'all' in val_arr:
        return set_get_param(cons_ps['all'], prms)

    if plf == amazon.SERVICE_NAME:
        if 'brand_new' not in val_arr:
            return set_get_param(cons_ps['used'], prms)

        if ('almost_unused' in val_arr) or ('no_scratches_or_stains' in val_arr) or ('slight_scratches_or_stains' in val_arr) or ('noticeable_scratches_or_stains' in val_arr):
            return set_get_param(cons_ps['all'], prms)

        return set_get_param(cons_ps['new'], prms)

    path = ''
    for status in val_arr:
        val = cons_ps[status]

        if plf == yahooAuction.SERVICE_NAME:
            path += ('&istatus=' + str(val) if not path else '%2C' + str(val))
        else:
            path += val

    return set_get_param(path, prms)


def set_product_status_post_param(val_arr, req_key, plf, prms, cons_ps):
    if 'all' in val_arr:
        return set_post_param(req_key, cons_ps['all'], prms, plf)

    if plf == mercari.SERVICE_NAME:
        arr = []
        for val in val_arr:
            arr.append(cons_ps[val])
        return set_post_param(req_key, arr, prms, plf)

    if 'brand_new' not in val_arr:
        return set_post_param(req_key, cons_ps['used'], prms, plf)

    if ('almost_unused' in val_arr) or ('no_scratches_or_stains' in val_arr) or ('slight_scratches_or_stains' in val_arr) or ('noticeable_scratches_or_stains' in val_arr):
        return prms

    return set_post_param(req_key, cons_ps['new'], prms, plf)


def set_product_status_param(key, val_arr, req_key, type, plf, prms, cons_web):
    if req_key is None:
        return prms

    if len(val_arr) == 0:
        return prms

    if type == PLATFORM_TYPE_WEB:
        return set_product_status_get_param(val_arr, plf, prms, cons_web[key])
    return set_product_status_post_param(val_arr, req_key, plf, prms, cons_web[key])


def extract_item(item, form, cons, kws, neg_kws, plf):
    type = cons['type']
    data = cons['data']
    req_prms = data['req']
    keys = req_prms['keys']
    res_prms = data['res']['params'][type]

    title = get_title(item, res_prms, type)

    if should_exclude_by_keyword(form, keys, kws, title):
        return

    if should_exclude_by_neg_keyword(keys, neg_kws, title):
        return

    price = get_price(item, res_prms, type, plf)

    if should_exclude_by_price(form, price, keys):
        return

    image_url = get_image_url(item, res_prms, type)

    detail_url = get_detail_url(item, req_prms['url'][PLATFORM_TYPE_WEB], res_prms, type, plf)

    return {
        'id': str(uuid.uuid4()),
        'title': title,
        'price': price,
        'imageUrl': image_url,
        'detailUrl': detail_url,
        'platform': plf,
        'isFavorite': False
    }


def get_title(item, res_prms, type):
    cons_title = res_prms['title']
    key = cons_title['key']

    if type == PLATFORM_TYPE_API:
        return item[key]

    title = item.select_one(key)
    if title is None:
        return ''

    attr = cons_title['attr']

    return title.text if attr is None else title.get(attr)


def get_price(item, res_prms, type, plf):
    cons_price = res_prms['price']
    key = cons_price['key']

    if type == PLATFORM_TYPE_API:
        price = int(item[key]) if plf == mercari.SERVICE_NAME else item[key]
        return {'str': add_price_comma(price), 'int': price}

    price_elem = item.select_one(key)

    if not price_elem:
        return

    price_str = price_elem.text.replace("¥", "").replace("￥", "").replace("円", "").replace(" ", "")

    if price_str == '???':
        return

    return {'str': price_str, 'int': int(price_str.replace(",", ""))}


def get_image_url(item, res_prms, cons_type):
    cons_img = res_prms['image']
    key = cons_img['key']
    attr = cons_img['attr']

    if cons_type == PLATFORM_TYPE_WEB:
        image = item.select_one(key)
        return image if attr is None else image.get(attr)

    data = item[key]
    if attr is None or type(attr) is not tuple:
        return data

    for i in attr:
        data = data[i]
    return data


def get_detail_url(item, web_url, res_prms, type, plf):
    cons_detail = res_prms['detail']
    key = cons_detail['key']
    attr = cons_detail['attr']

    if type == PLATFORM_TYPE_API:
        return web_url + '/item/' + item[key] if plf == mercari.SERVICE_NAME else item[key]

    path = None
    if key is None:
        path = item.get(attr)
    else:
        path = item.select_one(key).get(attr)

    return path if path.startswith('http') else web_url + path


def check_keyword_in_title(kw, title):
    return True if kw in title else False


def is_each_keyword_contained(kws, title):
    v_check_title = np.vectorize(check_keyword_in_title)
    results = v_check_title(kws, title)
    return False if False in results else True


def is_neg_keyword_contained(neg_kws, title):
    v_check_title = np.vectorize(check_keyword_in_title)
    results = v_check_title(neg_kws, title)
    return True if True in results else False


def ignore_ssl_error(loop, context):

    def validate_error(exception, protocol):
        import ssl
        SSL_PROTOCOLS = (asyncio.sslproto.SSLProtocol,)

        if (isinstance(exception, ssl.SSLError) and exception.reason == 'KRB5_S_INIT' and isinstance(protocol, SSL_PROTOCOLS)):
            return True
        return False

    if context.get("message") in {
        "SSL error in data received",
        "Fatal error on transport",
    }:
        # validate we have the right exception, transport and protocol
        exception = context.get('exception')
        protocol = context.get('protocol')
        if validate_error(exception, protocol):
            if loop.get_debug():
                asyncio.log.logger.debug('Ignoring asyncio SSL KRB5_S_INIT error')
            return

    orig_handler = loop.get_exception_handler()

    if orig_handler is not None:
        orig_handler(loop, context)
    else:
        loop.default_exception_handler(context)


def ignore_aiohttp_ssl_error(loop):
    loop.set_exception_handler(ignore_ssl_error)
