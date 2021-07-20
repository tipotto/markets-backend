import uuid
import math
from bs4 import BeautifulSoup
from constants import util
import services.base_service as base
import asyncio


def extract(item, kws, neg_kws, platform, const):
    try:
        # 商品名の取得
        title = base.get_title(item, platform, const)

        if len(kws) > 0 and base.is_each_keyword_contained(kws, title) is False:
            return None

        if len(neg_kws) > 0 and base.is_neg_keyword_contained(neg_kws, title) is True:
            return None

        # 金額の取得
        price = base.get_price(item, const)

        # 商品画像URLの取得
        image_url = base.get_image_url(item, const)

        # 詳細ページURLの取得
        detail_url = base.get_detail_url(item, platform, const)

        return {
            'id': str(uuid.uuid4()),
            'title': title,
            'price': price,
            'imageUrl': image_url,
            'detailUrl': detail_url,
            'platform': platform,
            'isFavorite': False
        }

    except Exception:
        raise


def get_price_query(key, value, const):
    try:
        if value == 0:
            return ''
        return const['query'][key].format(value)

    except Exception:
        raise


def get_category_query(category, const):
    try:
        main_value = category['main']
        sub_value = category['sub']

        if not main_value:
            return ''

        if not sub_value:
            return const['query']['category'][main_value]

        return const['query']['category'][main_value][sub_value]

    except Exception:
        raise


def get_search_query(form, const):
    try:
        return const['query']['search'].format(form['page'], form['keyword'])

    except Exception:
        raise


def generate_query(form, const):
    try:
        query = ''
        for key, value in form.items():
            if key in ['type', 'page', 'keyword', 'negKeyword', 'platforms', 'searchRange', 'sortOrder']:
                continue

            path = ''
            if key == 'category':
                path = get_category_query(value, const)

            elif key == 'minPrice' or key == 'maxPrice':
                path = get_price_query(key, value, const)

            elif key == 'productStatus':
                path = base.get_product_status_query(value, const)

            else:
                path = const['query'][key][value]

            query += path

        return query

    except Exception:
        raise


def generate_search_url(form, const):
    try:
        siteUrl = const['siteUrl']
        q = get_search_query(form, const)
        path = siteUrl + q
        query = generate_query(form, const)
        return (path if not query else path + query)

    except Exception:
        raise


def get_page(pager, platform, form, const):
    try:
        if form['type'] == 'next':
            return 0

        # これ以降はinitialの場合のみ実行
        if pager is None:
            # self.page == 1となる
            return form['page']

        if platform == 'paypay':
            page_num_text = pager.contents[-3].replace(",", "")
            # print('page_num_text', page_num_text)

            page_num = int(page_num_text) / 100
            # print('page_num', page_num)

            return page_num if isinstance(page_num, int) else math.ceil(page_num)

        last_page_url = pager.get(const['pages']['attr'])
        # print('last_page_url', last_page_url)

        split_url = last_page_url.rsplit('page=', 1)[-1]
        # print('split_url', split_url)

        last_page_num_text = split_url.split('&', 1)[0]
        # print('last_page_num_text', last_page_num_text)

        return int(last_page_num_text)

    except Exception:
        raise


async def scrape(form, kws, neg_kws, platform):
    try:
        const = base.get_params_by_platform(platform)
        headers = base.generate_headers(const)

        url = generate_search_url(form, const)
        page = await base.get(url, headers, compress=True)
        # page = await get(url, headers, common.PROXY, compress=True)

        soup = BeautifulSoup(page, util.HTML_PARSER)

        pager = soup.select_one(const['pages']['selector'])
        pagers = get_page(pager, platform, form, const)

        items = soup.select(const['items']['selector'])

        result = []
        append = result.append
        for item in items:

            i = extract(item, kws, neg_kws, platform, const)

            if i is None:
                continue

            append(i)

        return {
            'items': result,
            'pages': pagers
        }

    except Exception:
        raise


async def search(form):
    try:
        kws = base.create_keyword_list(form)
        neg_kws = base.create_neg_keyword_list(form)
        cors = [scrape(form, kws, neg_kws, p) for p in form['platforms']]
        return await asyncio.gather(*cors)

    except Exception:
        raise


def execute(form):
    try:
        return asyncio.run(search(form))

    except Exception:
        raise
