import traceback
import asyncio
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from constants import common, mercari, rakuma, paypay
import random
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
    return int(price.replace("¥", "").replace(
        " ", "").replace(",", ""))


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
        'title': title,
        'price': price,
        'imageUrl': imageUrl,
        'detailUrl': detailUrl,
        'platform': const['platform'],
    }


def add_query_prefix(query, isPrefix):
    if not query:
        return ''

    return ('?' + query) if isPrefix is False else ('&' + query)


def get_formatted_query(key, value, const):
    # query > search, minPrice, maxPrice で使用
    return const['query'][key].format(value)


def get_query_for_product_status_for_paypay(key, value, platform, const, prefix):
    path = ''
    if ('all' in value):
        path = const['query'][key]['all']

    else:
        isPrefix = prefix
        for status in value:
            q = const['query'][key][status]

            if not q:
                continue

            path += add_query_prefix(q, isPrefix)

            if isPrefix is False:
                isPrefix = True

    return path


def get_query_for_product_status(key, value, platform, const):
    path = ''
    if ('all' in value):
        path = const['query'][key]['all']

    else:
        for status in value:
            q = const['query'][key][status]

            if not q:
                continue

            path += q

    return path


def generate_query_for_paypay(form, platform, const):

    query = ''
    isPrefix = False
    for key, value in form.items():
        if key == 'query' or key == 'platforms':
            continue

        # lenメソッド: 文字列の空文字、NULL判定や、配列の要素数の判定を行う
        if len(value) == 0:
            continue

        path = ''
        if key == 'category':
            q = get_query_for_category(key, value, const)

            if not q:
                continue

            path += add_query_prefix(q, isPrefix)

            if isPrefix is False:
                isPrefix = True

        elif key == 'minPrice' or key == 'maxPrice':
            q = get_formatted_query(key, value, const)
            path += add_query_prefix(q, isPrefix)

            if isPrefix is False:
                isPrefix = True

        elif key == 'productStatus':
            path = get_query_for_product_status_for_paypay(
                key, value, platform, const, isPrefix)

            if not path:
                continue

            if isPrefix is False:
                isPrefix = True

        else:
            q = const['query'][key][value]

            if not q:
                continue

            path += add_query_prefix(q, isPrefix)

            if isPrefix is False:
                isPrefix = True

        query += path

    return query


def get_query_for_category(key, value, const):

    main = value['main']
    sub = value['sub']

    if not main:
        return ''

    if not sub:
        return const['query'][key][main]

    return const['query'][key][main][sub]


def generate_query(form, platform, const):
    query = ''
    for key, value in form.items():
        if key == 'query' or key == 'platforms':
            continue

        # lenメソッド: 文字列の空文字、NULL判定や、配列の要素数の判定を行う
        if len(value) == 0:
            continue

        path = ''
        if key == 'category':
            path = get_query_for_category(key, value, const)

        elif key == 'minPrice' or key == 'maxPrice':
            path = get_formatted_query(key, value, const)

        elif key == 'productStatus':
            path = get_query_for_product_status(key, value, platform, const)

        else:
            path = const['query'][key][value]

        query += path

    return query


def generate_search_query(form, platform, const):
    if platform == paypay.SERVICE_NAME:
        return generate_query_for_paypay(form, platform, const)

    return generate_query(form, platform, const)


def generate_search_url(form, platform, const):

    siteUrl = const['siteUrl']
    q = get_formatted_query('search', form['query'], const)

    path = siteUrl + q

    query = generate_search_query(form, platform, const)

    return (path if not query else path + query)


async def scrape(form, platform, hook=None):

    const = get_params_by_platform(platform)
    headers = generate_headers(const)

    # Aiohttpでは、httpプロキシにしか対応していない（socksプロキシ使用不可）
    # proxy = common.PROXY

    url = generate_search_url(form, platform, const)

    # async with sem:
    # page = await get(url, headers, proxy, compress=True)
    page = await get(url, headers, compress=True)

    # print('page', page)

    # 取得したHTMLのメモリサイズを確認
    # print(sys.getsizeof(page))

    soup = BeautifulSoup(page, common.HTML_PARSER)
    items = soup.select(const['items']['selector'], limit=common.ITEM_NUMBER)

    # print('items', items)

    # counter = 0
    try:
        for item in items:

            # 各アイテムから必要なデータを抽出
            result = extract(const, item)
            results.append(result)

            # counter += 1

            # 例外処理の挙動を確認するために、故意に例外を発生させる。
            # if counter == 6:
            #     raise Exception

    except Exception as e:
        print('Error occurred:', e)
        # with open(r"./app/log/error.log", 'a') as f:
        #     traceback.print_exc(file=f)

        return {
            'status': 'failure',
            'results': results,
            'error': traceback.format_exc()
        }

        # print("Error occurred while fetching search results.")

    # return results


async def parallel_by_gather(form):
    # sem = asyncio.Semaphore(3)

    platforms = form['platforms']

    # cors = [scrape(sem, query, p) for p in platforms]
    cors = [scrape(form, p) for p in platforms]
    # results = await asyncio.gather(*cors)
    await asyncio.gather(*cors)
    # return results


def execute(form):
    loop = asyncio.get_event_loop()
    # results = loop.run_until_complete(parallel_by_gather(form))
    loop.run_until_complete(parallel_by_gather(form))
    result = {
        'status': 'success',
        'results': results,
        'error': ''
    }
    print('result', result)


# # メソッドの動作確認用
if __name__ == "__main__":

    form = {
        'category': {'main': '', 'sub': ''},
        'query': '日向坂46 斎藤京子',
        # platforms: mercari, rakuma, paypay
        'platforms': ['paypay'],
        'minPrice': '0',
        'maxPrice': '0',
        'productStatus': ['all'],
        'salesStatus': 'selling',
        'deliveryCost': 'all',
        'sortOrder': 'asc'
    }

    # execute(form)

    try:
        platform = 'paypay'
        const = get_params_by_platform(platform)
        url = generate_search_url(form, platform, const)
        print('url', url)

    except Exception as e:
        print('Error occurred:', e)

        print('traceback', traceback.format_exc())

    # platforms = form['platforms']

    # for p in platforms:
    #     print('1. platform', p)

    #     const = get_params_by_platform(p)
    #     headers = generate_headers(const)
    #     r = requests.get('http://whatismyheader.com/', headers=headers)

    #     print("4. headers", headers)
    #     print("5. request header", r.text)
