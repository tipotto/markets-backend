import random
import re
import numpy as np
from aiohttp import ClientSession
from fake_headers import Headers
from constants import util, mercari, rakuma, paypay


def get_params_by_platform(platform):
    if platform == mercari.SERVICE_NAME:
        return mercari.DATA
    elif platform == rakuma.SERVICE_NAME:
        return rakuma.DATA

    return paypay.DATA


def split_keyword(keyword):

    # if not keyword:
    #     return []

    # keywordの先頭と末尾の空白を削除
    removed = keyword.strip()

    # keywordに空白（全角、半角、タブ文字）が含まれているかチェック
    # 含まれていれば、空白で分割してリストにする
    # 含まれていなければ、keywordリストを作成
    if re.search(util.KEYWORD_REG_EXP, removed):
        return re.split(util.KEYWORD_REG_EXP, removed)

    return [keyword]


def create_keyword_list(form):
    try:
        if form['searchRange'] == 'title-desc':
            return []

        return split_keyword(form['keyword'])

    except Exception:
        raise


def create_neg_keyword_list(form):
    try:
        if not form['negKeyword']:
            return []

        return split_keyword(form['negKeyword'])

    except Exception:
        raise


async def get(url, headers, **kwargs):
    try:
        async with ClientSession(headers=headers) as session:
            async with session.get(url, **kwargs) as resp:
                return (await resp.text())

    except Exception:
        raise


def generate_headers(const):
    try:
        os = random.choice(util.OS_LIST)
        browser = random.choice(util.BROWSER_LIST)
        # print('2. os', os)
        # print('3. browser', browser)

        headers_type = os + '-' + browser
        headers = util.HEADERS_DICT[headers_type]

        fake_headers = Headers(
            browser=browser,
            os=os,
            headers=False
        ).generate()

        headers['User-Agent'] = fake_headers['User-Agent']
        headers['Referer'] = const['referer']
        return headers

    except Exception:
        raise


def get_product_status_query(values, const):
    try:
        path = ''
        if ('all' in values):
            # 空文字が返される
            path = const['query']['productStatus']['all']

        else:
            for status in values:
                path += const['query']['productStatus'][status]

        return path

    except Exception:
        raise


def get_title(item, platform, const):
    try:
        titles = item.select(const['title']['selector'])
        if platform == paypay.SERVICE_NAME:
            return titles[0].get(const['title']['attr'])

        return titles[0].contents[0]

    except Exception:
        raise


def get_price(item, const):
    try:
        prices = item.select(const['price']['selector'])
        price = prices[0].contents[0]
        price_str = price.replace("¥", "").replace("円", "").replace(" ", "")

        if price_str == '???':
            return {'str': None, 'int': 0}

        price_int = int(price_str.replace(",", ""))
        return {'str': price_str, 'int': price_int}

    except Exception:
        raise


def get_image_url(item, const):
    try:
        images = item.select(const['image']['selector'])
        return images[0].get(const['image']['attr'])

    except Exception:
        raise


def get_detail_url(item, platform, const):
    try:
        detail_selector = const['detail']['selector']
        detail_attr = const['detail']['attr']
        site_url = const['siteUrl']

        if platform == mercari.SERVICE_NAME:
            details = item.select(detail_selector)
            return site_url + details[0].get(detail_attr)

        elif platform == rakuma.SERVICE_NAME:
            details = item.select(detail_selector)
            return details[0].get(detail_attr)

        relativePath = item.get(detail_attr)
        return site_url + relativePath

    except Exception:
        raise


def check_keyword_in_title(keyword, title):
    try:
        return True if keyword in title else False

    except Exception:
        raise


def is_neg_keyword_contained(neg_keyword_arr, title):
    try:
        v_check_title = np.vectorize(check_keyword_in_title)
        results = v_check_title(neg_keyword_arr, title)
        return True if True in results else False

    except Exception:
        raise


def is_each_keyword_contained(keyword_arr, title):
    try:
        v_check_title = np.vectorize(check_keyword_in_title)
        results = v_check_title(keyword_arr, title)
        return False if False in results else True

    except Exception:
        raise
