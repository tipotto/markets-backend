import asyncio
import random
import uuid
import re
import time
import traceback
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from constants import common, mercari, rakuma, paypay
from fake_headers import Headers

# result = {
#     'mercari': {
#         'likes': [],
#         'asc': [],
#         'desc': [],
#     },
#     'rakuma': {
#         'likes': [],
#         'asc': [],
#         'desc': [],
#     },
#     'paypay': {
#         'likes': [],
#         'asc': [],
#         'desc': [],
#     }
# }
result = {
    'price': [],
    # 'market': {
    # },
}


def generate_headers(const):

    os = random.choice(common.OS_LIST)
    browser = random.choice(common.BROWSER_LIST)
    # print('2. os', os)
    # print('3. browser', browser)

    headers_type = os + '-' + browser
    headers = common.HEADERS_DICT[headers_type]

    fake_headers = Headers(
        browser=browser,
        os=os,
        headers=False
    ).generate()

    headers['User-Agent'] = fake_headers['User-Agent']
    headers['Referer'] = const['referer']

    return headers


# async def get(url, headers, proxy, **kwargs):
#     async with ClientSession(headers=headers) as session:
#         async with session.get(url, proxy=proxy, **kwargs) as resp:
#             return (await resp.text())


async def get(url, headers, **kwargs):
    async with ClientSession(headers=headers) as session:
        async with session.get(url, **kwargs) as resp:
            return (await resp.text())


def get_params_by_platform(platform):
    if platform == mercari.SERVICE_NAME:
        return mercari.DATA
    elif platform == rakuma.SERVICE_NAME:
        return rakuma.DATA

    return paypay.DATA


def get_title(const, item):
    titles = item.select(const['title']['selector'])

    if const['platform'] == paypay.SERVICE_NAME:
        return titles[0].get(const['title']['attr'])

    return titles[0].contents[0]


def get_price(const, item):
    prices = item.select(const['price']['selector'])
    price = prices[0].contents[0]
    price_str = price.replace("¥", "").replace(" ", "")
    price_int = int(price_str.replace(",", ""))
    return {'str': price_str, 'int': price_int}


def get_image_url(const, item):
    images = item.select(const['image']['selector'])
    return images[0].get(const['image']['attr'])


def get_detail_url(const, item):
    platform = const['platform']
    detailSelector = const['detail']['selector']
    detailAttr = const['detail']['attr']
    siteUrl = const['siteUrl']

    if platform == mercari.SERVICE_NAME:
        details = item.select(detailSelector)
        return siteUrl + details[0].get(detailAttr)

    elif platform == rakuma.SERVICE_NAME:
        details = item.select(detailSelector)
        return details[0].get(detailAttr)

    relativePath = item.get(detailAttr)
    return siteUrl + relativePath


def get_likes(const, item):
    likesSelector = const['likes']['selector']

    # ラクマ、paypayフリマの場合
    if not likesSelector:
        return 0

    # メルカリでいいねがない場合、Noneが返る
    return item.select_one(likesSelector)


def is_each_keyword_contained(keywords, title):

    results = list(map(lambda w: w in title, keywords))

    if False in results:
        return False

    return True


def create_keyword_list(form):

    if form['keywordFilter'] == 'unuse':
        return None

    keyword = form['keyword']

    # keywordの先頭と末尾の空白を削除
    removed = keyword.strip()

    # keywordに空白（全角、半角、タブ文字）が含まれているかチェック
    # 含まれていれば、空白で分割してリストにする
    # 含まれていなければ、keywordリストを作成
    if re.search(common.KEYWORD_REG_EXP, removed):
        return re.split(common.KEYWORD_REG_EXP, removed)

    return [keyword]


def extract(const, item, kws, type):
    # 商品名の取得
    title = get_title(const, item)

    if kws is not None and is_each_keyword_contained(kws, title) is False:
        return 'keyword'

    # 金額の取得
    price = get_price(const, item)

    # 商品画像URLの取得
    imageUrl = get_image_url(const, item)

    # 詳細ページURLの取得
    detailUrl = get_detail_url(const, item)

    # いいねの取得
    likes = get_likes(const, item)

    # searchTypeがpriceであることを確認する
    if likes is None and type == 'price':
        return 'likes'

    return {
        'id': str(uuid.uuid4()),
        'title': title,
        'price': price,
        'imageUrl': imageUrl,
        'detailUrl': detailUrl,
        'platform': const['platform'],
        'likes': likes
    }


def add_query_prefix(query, isPrefix):
    return ('?' + query) if isPrefix is False else ('&' + query)


def get_price_query(key, value, const):
    if value == 0:
        return ''

    return const['query'][key].format(value)


def get_product_status_query(key, valueArr, const):
    path = ''
    if ('all' in valueArr):
        # 空文字が返される
        path = const['query'][key]['all']

    else:
        for status in valueArr:
            path += const['query'][key][status]

    return path


def generate_query(form, const):
    query = ''
    for key, value in form.items():
        path = ''
        if key == 'productStatus':
            path = get_product_status_query(key, value, const)

        elif key == 'deliveryCost':
            path = const['query'][key][value]

        else:
            continue

        query += path

    return query


def get_search_urls(form, const):
    siteUrl = const['siteUrl']
    kw = form['keyword']
    type = form['searchType']
    pages = [1, 2, 3]
    return [siteUrl + const['query']['analyze'][type]['like'].format(p, kw) for p in pages]


def generate_search_urls(form, const):
    urls = get_search_urls(form, const)
    query = generate_query(form, const)
    return [(u if not query else u + query) for u in urls]


# def generate_search_url(form, const, sortType):
#     siteUrl = const['siteUrl']
#     q = get_search_query(form, const, sortType)
#     path = siteUrl + q
#     query = generate_query(form, const)
#     return (path if not query else path + query)


async def scrape(url, kws, headers, const, type):
    try:
        page = await get(url, headers, compress=True)

        soup = BeautifulSoup(page, common.HTML_PARSER)
        items = soup.select(const['items']['selector'])

        for item in items:

            i = extract(const, item, kws, type)

            if i == 'keyword':
                continue

            if i == 'price':
                break

            arr = result[type]
            arr.append(i)

    except Exception:
        raise


async def calculate(form):
    try:
        kws = create_keyword_list(form)
        const = get_params_by_platform('mercari')
        headers = generate_headers(const)
        urls = generate_search_urls(form, const)
        type = form['searchType']

        cors = [scrape(u, kws, headers, const, type) for u in urls]
        await asyncio.gather(*cors)

    except Exception:
        raise


async def analyze(form, kws, platform, wait_time=0.1):
    try:
        const = get_params_by_platform(platform)
        headers = generate_headers(const)
        urls = generate_search_urls(form, const)
        type = form['searchType']

        for u in urls:
            scrape(u, kws, headers, const, type)
            # await asyncio.sleep(wait_time)
            # time.sleep(0.1)

        # await asyncio.sleep(wait_time)

    except Exception:
        raise


async def parallel_by_gather(form):
    try:
        kws = create_keyword_list(form)
        platforms = form['platforms']
        cors = [analyze(form, kws, p) for p in platforms]
        await asyncio.gather(*cors)

    except Exception:
        raise


def calculate_price(form):
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(calculate(form))
        return {
            'status': 'success',
            'results': result,
            'error': ''
        }

    except Exception:
        return {
            'status': 'failure',
            'results': result,
            'error': traceback.format_exc()
        }


def analyze_market(form):
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(parallel_by_gather(form))
        return {
            'status': 'success',
            'results': result,
            'error': ''
        }

    except Exception:
        return {
            'status': 'failure',
            'results': result,
            'error': traceback.format_exc()
        }


# メソッドの動作確認用
# if __name__ == "__main__":

#     # form = {
#     #     'category': {'main': 'pet', 'sub': ''},
#     #     'query': '日向坂46 斎藤京子',
#     #     # platforms: mercari, rakuma, paypay
#     #     'platforms': ['paypay'],
#     #     'minPrice': '0',
#     #     'maxPrice': '0',
#     #     'productStatus': ['all', 'brand_new', 'almost_unused', 'no_scratches_or_stains'],
#     #     'salesStatus': 'selling',
#     #     'deliveryCost': 'all',
#     #     'sortOrder': 'asc'
#     # }

#     # execute(form)

#     try:
#         # platform = 'paypay'
#         # const = get_params_by_platform(platform)
#         # url = generate_search_url(form, platform, const)
#         is_contained = is_each_keyword_contained(
#             '渡邉美穂', '日向坂46 渡邉美穂 チェキ')
#         print('is_contained', is_contained)

#     except Exception as e:
#         print('Error occurred:', e)
#         print('traceback', traceback.format_exc())
