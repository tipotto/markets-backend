import traceback
import asyncio
import random
import uuid
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from constants import common, mercari, rakuma, paypay
from fake_headers import Headers

results = []


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


def extract(const, item):
    # 商品名の取得
    title = get_title(const, item)

    # 金額の取得
    price = get_price(const, item)

    # 商品画像URLの取得
    imageUrl = get_image_url(const, item)

    # 詳細ページURLの取得
    detailUrl = get_detail_url(const, item)

    return {
        'id': str(uuid.uuid4()),
        'title': title,
        'price': price,
        'imageUrl': imageUrl,
        'detailUrl': detailUrl,
        'platform': const['platform'],
        'isFavorite': False
    }


def add_query_prefix(query, isPrefix):
    return ('?' + query) if isPrefix is False else ('&' + query)


def get_search_query(key, formValue, const):
    return const['query']['search'].format(formValue['page'], formValue['keyword'])


def get_price_query(key, value, const):
    if value == 0:
        return ''

    return const['query'][key].format(value)


def get_rakuma_query_for_product_status(key, valueArr, platform, const, prefix):
    path = ''
    if ('all' in valueArr):
        path = const['query'][key]['all']

    else:
        isPrefix = prefix
        for status in valueArr:
            q = const['query'][key][status]

            path += add_query_prefix(q, isPrefix)

            if isPrefix is False:
                isPrefix = True

    return path


def get_query_for_product_status(key, valueArr, platform, const):
    path = ''
    if ('all' in valueArr):
        # 空文字が返される
        path = const['query'][key]['all']

    else:
        for status in valueArr:
            path += const['query'][key][status]

    return path


def generate_rakuma_query(form, platform, const):

    query = ''
    isPrefix = False
    for key, value in form.items():
        if key == 'page' or key == 'keyword' or key == 'platforms':
            continue

        path = ''
        if key == 'category':
            q = get_query_for_category(key, value, const)

            if not q:
                continue

            path = add_query_prefix(q, isPrefix)

        elif key == 'minPrice' or key == 'maxPrice':
            q = get_price_query(key, value, const)

            if not q:
                continue

            path = add_query_prefix(q, isPrefix)

        elif key == 'productStatus':
            q = get_rakuma_query_for_product_status(
                key, value, platform, const, isPrefix)

            if not q:
                continue

            path = q

        else:
            q = const['query'][key][value]

            if not q:
                continue

            path = add_query_prefix(q, isPrefix)

        if isPrefix is False:
            isPrefix = True

        query += path

    return query


def get_query_for_category(key, value, const):

    mainValue = value['main']
    subValue = value['sub']

    if not mainValue:
        return ''

    if not subValue:
        return const['query'][key][mainValue]

    return const['query'][key][mainValue][subValue]


def generate_query(form, platform, const):
    query = ''
    for key, value in form.items():
        if key == 'page' or key == 'keyword' or key == 'platforms':
            continue

        path = ''
        if key == 'category':
            path = get_query_for_category(key, value, const)

        elif key == 'minPrice' or key == 'maxPrice':
            path = get_price_query(key, value, const)

        elif key == 'productStatus':
            path = get_query_for_product_status(key, value, platform, const)

        else:
            path = const['query'][key][value]

        query += path

    return query


def generate_search_query(form, platform, const):
    if platform == rakuma.SERVICE_NAME:
        return generate_rakuma_query(form, platform, const)

    return generate_query(form, platform, const)


def generate_search_url(form, platform, const):

    siteUrl = const['siteUrl']
    q = get_search_query('search', form, const)

    path = siteUrl + q

    query = generate_search_query(form, platform, const)

    return (path if not query else path + query)


async def scrape(form, platform, hook=None):

    const = get_params_by_platform(platform)
    headers = generate_headers(const)
    url = generate_search_url(form, platform, const)

    page = await get(url, headers, compress=True)
    # page = await get(url, headers, common.PROXY, compress=True)

    soup = BeautifulSoup(page, common.HTML_PARSER)
    items = soup.select(const['items']['selector'])

    try:
        for item in items:

            result = extract(const, item)
            results.append(result)

    except Exception:

        return {
            'status': 'failure',
            'results': results,
            'error': traceback.format_exc()
        }


async def parallel_by_gather(form):
    cors = [scrape(form, p) for p in form['platforms']]
    await asyncio.gather(*cors)


def execute(form):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(parallel_by_gather(form))
    return {
        'status': 'success',
        'results': results,
        'error': ''
    }


# メソッドの動作確認用
# if __name__ == "__main__":

#     form = {
#         'category': {'main': 'pet', 'sub': ''},
#         'query': '日向坂46 斎藤京子',
#         # platforms: mercari, rakuma, paypay
#         'platforms': ['paypay'],
#         'minPrice': '0',
#         'maxPrice': '0',
#         'productStatus': ['all', 'brand_new', 'almost_unused', 'no_scratches_or_stains'],
#         'salesStatus': 'selling',
#         'deliveryCost': 'all',
#         'sortOrder': 'asc'
#     }

#     # execute(form)

#     try:
#         platform = 'paypay'
#         const = get_params_by_platform(platform)
#         url = generate_search_url(form, platform, const)
#         print('url', url)

#     except Exception as e:
#         print('Error occurred:', e)
#         print('traceback', traceback.format_exc())
