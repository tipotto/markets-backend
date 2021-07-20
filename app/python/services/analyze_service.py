from bs4 import BeautifulSoup
import uuid
import asyncio
import numpy as np
from decimal import Decimal, ROUND_HALF_UP
from constants import util
import services.base_service as base


props = {
    'all_items': [],
    'rounded_price_arr': np.array([]),
    'raw_price_arr': np.array([]),
    'items_num_arr': np.array([]),
    'likes_num_arr': np.array([]),
    'items_by_price_range': {}
}

data = {
    'items': {
        'all': {
            'list': [],
            'byId': {},
            'allIds': []
        },
        'market': {
            'list': [],
            'byId': {},
            'allIds': []
        }
    },
    'price': {
        'min': 0,
        'max': 0,
        'average': 0,
        'market': {
            'min': 0,
            'max': 0,
        },
    },
    'chart': {
        'whole': {
            'priceLabels': [],
            'likesNums': [],
            'itemsNums': [],
        },
        'range': {
            'priceLabels': [],
            'likesNums': [],
            'itemsNums': [],
        },
        'detail': {
            'priceLabels': [],
            'likesNums': [],
            'itemsNums': [],
        }
    }
}


def get_search_urls(form, const):
    try:
        kw = form['keyword']
        target = form['searchTarget']
        site_url = const['siteUrl']
        pages = [1, 2, 3, 4, 5]
        return [site_url + const['query']['analyze'][target].format(p, kw) for p in pages]

    except Exception:
        raise


def generate_query(form, const):
    try:
        query = ''
        for key, value in form.items():
            path = ''
            if key == 'productStatus':
                path = base.get_product_status_query(value, const)

            elif key == 'deliveryCost':
                path = const['query']['deliveryCost'][value]

            else:
                continue

            query += path

        return query

    except Exception:
        raise


def generate_search_urls(form, const):
    try:
        urls = get_search_urls(form, const)
        query = generate_query(form, const)
        return [u if not query else u + query for u in urls]

    except Exception:
        raise


def get_likes(item, const):
    try:
        likes_selector = const['likes']['selector']

        # ラクマ、paypayフリマの場合
        if not likes_selector:
            return 0

        # メルカリでいいねがない場合、Noneが返る
        likes = item.select_one(likes_selector)
        return 0 if likes is None else int(likes.contents[0])

    except Exception:
        raise


def extract_item(item, kws, neg_kws, platform, price_type, const):
    try:
        # 商品名の取得
        title = base.get_title(item, platform, const)

        if len(kws) > 0 and base.is_each_keyword_contained(kws, title) is False:
            return {'data': None, 'error': 'keyword'}

        if len(neg_kws) > 0 and base.is_neg_keyword_contained(neg_kws, title) is True:
            return {'data': None, 'error': 'neg_keyword'}

        # 金額の取得
        price = base.get_price(item, const)

        if price['str'] is None:
            return {'data': None, 'error': 'price'}

        # 商品画像URLの取得
        image_url = base.get_image_url(item, const)

        # 詳細ページURLの取得
        detail_url = base.get_detail_url(item, platform, const)

        # いいねの取得
        likes = get_likes(item, const)

        if platform == 'mercari' and price_type == 'popular' and likes == 0:
            return {'data': None, 'error': 'likes'}

        result = {
            'id': str(uuid.uuid4()),
            'title': title,
            'price': price,
            'imageUrl': image_url,
            'detailUrl': detail_url,
            'platform': platform,
            'likes': likes
        }

        return {'data': result, 'error': None}

    except Exception:
        raise


def extract_popular_price(item, prop):
    try:
        # p = props
        all_items_by_type = prop['all_items']
        rounded_price_arr = prop['rounded_price_arr']
        raw_price_arr = prop['raw_price_arr']
        likes_num_arr = prop['likes_num_arr']
        items_by_price_range = prop['items_by_price_range']

        all_items_by_type.append(item)

        int_price = item['price']['int']
        raw_price_arr = np.append(raw_price_arr, int_price)

        # 価格を1000の位で切り上げる
        # もし価格が1000円未満の場合は、100の位で切り上げた結果を返す
        rounded_price = 0
        if int_price % 1000 == 0:
            rounded_price = int_price
        else:
            rounded_price = ceil(int_price, 1000)

        # フィールドにデータを追加
        if rounded_price in rounded_price_arr:
            index = np.where(rounded_price_arr == rounded_price)[0][0]
            likes_num_arr[index] += item['likes']
            items_by_price_range[rounded_price].append(item)

        else:
            rounded_price_arr = np.append(rounded_price_arr, rounded_price)
            likes_num_arr = np.append(likes_num_arr, item['likes'])
            items_by_price_range[rounded_price] = [item]

        return {
            'all_items': all_items_by_type,
            'rounded_price_arr': rounded_price_arr,
            'raw_price_arr': raw_price_arr,
            # 'items_num_arr': np.array([]),
            'likes_num_arr': likes_num_arr,
            'items_by_price_range': items_by_price_range
        }

    except Exception:
        raise


def extract_market_price(item, prop):
    try:
        # p = props
        all_items_by_type = prop['all_items']
        rounded_price_arr = prop['rounded_price_arr']
        raw_price_arr = prop['raw_price_arr']
        items_num_arr = prop['items_num_arr']
        items_by_price_range = prop['items_by_price_range']

        all_items_by_type.append(item)

        int_price = item['price']['int']
        raw_price_arr = np.append(raw_price_arr, int_price)

        # 価格を1000の位で切り上げる
        # もし価格が1000円未満の場合は、100の位で切り上げた結果を返す
        rounded_price = 0
        if int_price % 1000 == 0:
            rounded_price = int_price
        else:
            rounded_price = ceil(int_price, 1000)

        # フィールドにデータを追加
        if rounded_price in rounded_price_arr:
            index = np.where(rounded_price_arr == rounded_price)[0][0]
            items_num_arr[index] += 1
            items_by_price_range[rounded_price].append(item)

        else:
            rounded_price_arr = np.append(rounded_price_arr, rounded_price)
            items_num_arr = np.append(items_num_arr, 1)
            items_by_price_range[rounded_price] = [item]

        # props = {
        #     'all_items': all_items_by_type,
        #     'rounded_price_arr': rounded_price_arr,
        #     'raw_price_arr': raw_price_arr,
        #     'items_num_arr': items_num_arr,
        #     # 'likes_num_arr': np.array([]),
        #     'items_by_price_range': items_by_price_range
        # }
        return {
            'all_items': all_items_by_type,
            'rounded_price_arr': rounded_price_arr,
            'raw_price_arr': raw_price_arr,
            'items_num_arr': items_num_arr,
            # 'likes_num_arr': np.array([]),
            'items_by_price_range': items_by_price_range
        }

    except Exception:
        raise


async def scrape(url, kws, neg_kws, headers, platform, price_type, const):
    try:
        page = await base.get(url, headers, compress=True)

        soup = BeautifulSoup(page, util.HTML_PARSER)
        items = soup.select(const['items']['selector'])

        # platform = self.platform
        # price_type = self.price_type
        # extract = self.extract_item
        # extract_popular_price = self.extract_popular_price
        # extract_market_price = self.extract_market_price
        global props
        p = props

        for item in items:
            i = extract_item(item, kws, neg_kws, platform, price_type, const)
            data = i['data']
            err = i['error']

            if err in ['keyword', 'neg_keyword', 'price']:
                continue

            if err == 'likes':
                break

            updated_props = None
            if platform == 'mercari' and price_type == 'popular':
                updated_props = extract_popular_price(data, p)
            else:
                updated_props = extract_market_price(data, p)

            p = updated_props

        props = p

    except Exception:
        raise


# 四捨五入
def round_half_up(price, str_digit):
    try:
        d_str_price = Decimal(str(price))
        return int(d_str_price.quantize(Decimal(str_digit), rounding=ROUND_HALF_UP))

    except Exception:
        raise


# 切り上げ
def ceil(price, range):
    try:
        return ((int)(price / range) + 1) * range

    except Exception:
        raise


# 切り捨て
def floor(price, range):
    try:
        return (int)(price / range) * range

    except Exception:
        raise


def get_likes_num(price):
    try:
        rounded_price_arr = props['rounded_price_arr']
        likes_num_arr = props['likes_num_arr']

        arr = np.where(rounded_price_arr == price)[0]
        if len(arr) == 0:
            return 0

        return likes_num_arr[arr[0]]

    except Exception:
        raise


def get_items_num(price):
    try:
        items_by_price_range = props['items_by_price_range']

        if price in items_by_price_range:
            items = items_by_price_range[price]
            return len(items)

        return 0

    except Exception:
        raise


def add_price_comma(price):
    try:
        return '{:,}'.format(price)

    except Exception:
        raise


def change_price_unit(price):
    try:
        str_price = str(price).replace("000", "")
        return str_price if str_price == '0' else str_price + 'k'

    except Exception:
        raise


def get_chart_price_label(max_price_range):
    try:
        min_price_range = max_price_range - 1000
        return ' '.join([change_price_unit(min_price_range), '-', change_price_unit(max_price_range)])

    except Exception:
        raise


def get_whole_price_data_for_popular(p):
    try:
        if len(p['rounded_price_arr']) == 0:
            return None

        int_max_rounded_price = int(np.amax(p['rounded_price_arr']))
        int_min_rounded_price = int(np.amin(p['rounded_price_arr']))
        int_price_range_arr = np.arange(int_min_rounded_price, int_max_rounded_price + 1000, 1000)

        v_get_label = np.vectorize(get_chart_price_label)
        chart_price_label_arr = v_get_label(int_price_range_arr)

        v_get_likes_num = np.vectorize(get_likes_num)
        chart_likes_num_arr = v_get_likes_num(int_price_range_arr)

        data['chart']['whole'] = {
            'priceLabels': chart_price_label_arr.tolist(),
            'likesNums': chart_likes_num_arr.tolist(),
            'itemsNums': [],
        }

        return v_get_label, v_get_likes_num

    except Exception:
        raise


def get_whole_price_data_for_market(p):
    try:
        if len(p['rounded_price_arr']) == 0:
            return None

        int_max_rounded_price = int(np.amax(p['rounded_price_arr']))
        int_min_rounded_price = int(np.amin(p['rounded_price_arr']))
        int_price_range_arr = np.arange(int_min_rounded_price, int_max_rounded_price + 1000, 1000)

        v_get_label = np.vectorize(get_chart_price_label)
        chart_price_label_arr = v_get_label(int_price_range_arr)

        v_get_items_num = np.vectorize(get_items_num)
        chart_items_num_arr = v_get_items_num(int_price_range_arr)

        data['chart']['whole'] = {
            'priceLabels': chart_price_label_arr.tolist(),
            'likesNums': [],
            'itemsNums': chart_items_num_arr.tolist(),
        }

        return v_get_label, v_get_items_num

    except Exception:
        raise


def get_popular_price_range():
    try:
        global data
        d = data
        p = props

        chart_price_range = np.array([1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000])
        v_get_label, v_get_likes_num = get_whole_price_data_for_popular(p)

        if len(p['likes_num_arr']) == 0:
            return None

        # いいねの最大値のインデックスを取得
        # 複数の値が存在する場合、最初のインデックスを返す
        max_likes_index = np.argmax(p['likes_num_arr'])

        # 推奨価格帯（アイテム数が最大になる価格帯）を取得
        max_popular_price = p['rounded_price_arr'][max_likes_index]
        min_popular_price = max_popular_price - 1000

        # 推奨価格帯のアイテムリストを取得
        items_in_market_price = p['items_by_price_range'][max_popular_price]

        # 推奨価格帯の上限を10000の位で切り下げ
        floored_max_popular_price = 0
        if max_popular_price % 10000 == 0:
            floored_max_popular_price = 0 if max_popular_price <= 10000 else int(max_popular_price - 10000)
        else:
            floored_max_popular_price = floor(max_popular_price, 10000)

        int_price_range_arr = chart_price_range + floored_max_popular_price

        chart_price_label_arr = v_get_label(int_price_range_arr)

        chart_likes_num_arr = v_get_likes_num(int_price_range_arr)

        # 平均価格を算出
        avg_price = np.mean(p['raw_price_arr'])

        # 平均価格を小数点で四捨五入
        int_avg_price = round_half_up(avg_price, '0')

        # 最低価格を算出
        min_price = np.amin(p['raw_price_arr'])

        # 最高価格を算出
        max_price = np.amax(p['raw_price_arr'])

        d['items']['all']['list'] = p['all_items']
        d['items']['market']['list'] = items_in_market_price

        d['price'] = {
            'min': add_price_comma(int(min_price)),
            'max': add_price_comma(int(max_price)),
            'average': add_price_comma(int_avg_price),
            'market': {
                'min': add_price_comma(int(min_popular_price)),
                'max': add_price_comma(int(max_popular_price))
            }
        }

        d['chart']['range'] = {
            'priceLabels': chart_price_label_arr.tolist(),
            'likesNums': chart_likes_num_arr.tolist(),
            'itemsNums': [],
        }

        data = d

        return p, max_likes_index

    except Exception:
        raise


def get_market_price_range():
    try:
        global data
        d = data
        p = props

        chart_price_range = np.array([1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000])
        v_get_label, v_get_items_num = get_whole_price_data_for_market(p)

        if len(p['items_num_arr']) == 0:
            return None

        # いいねの最大値のインデックスを取得
        # 複数の値が存在する場合、最初のインデックスを返す
        max_items_num_index = np.argmax(p['items_num_arr'])

        # 推奨価格帯（アイテム数が最大になる価格帯）を取得
        max_market_price = p['rounded_price_arr'][max_items_num_index]
        min_market_price = max_market_price - 1000

        # 推奨価格帯のアイテムリストを取得
        items_in_market_price = p['items_by_price_range'][max_market_price]

        # 推奨価格帯の上限を10000の位で切り下げ
        floored_max_market_price = 0
        if max_market_price % 10000 == 0:
            floored_max_market_price = 0 if max_market_price <= 10000 else int(max_market_price - 10000)
        else:
            floored_max_market_price = floor(max_market_price, 10000)

        int_price_range_arr = chart_price_range + floored_max_market_price

        chart_price_label_arr = v_get_label(int_price_range_arr)

        chart_items_num_arr = v_get_items_num(int_price_range_arr)

        # 平均価格を算出
        avg_price = np.mean(p['raw_price_arr'])

        # 平均価格を小数点で四捨五入
        int_avg_price = round_half_up(avg_price, '0')

        # 最低価格を算出
        min_price = np.amin(p['raw_price_arr'])

        # 最高価格を算出
        max_price = np.amax(p['raw_price_arr'])

        d['items']['all']['list'] = p['all_items']
        d['items']['market']['list'] = items_in_market_price

        d['price'] = {
            'min': add_price_comma(int(min_price)),
            'max': add_price_comma(int(max_price)),
            'average': add_price_comma(int_avg_price),
            'market': {
                'min': add_price_comma(int(min_market_price)),
                'max': add_price_comma(int(max_market_price))
            }
        }

        d['chart']['range'] = {
            'priceLabels': chart_price_label_arr.tolist(),
            'likesNums': [],
            'itemsNums': chart_items_num_arr.tolist(),
        }

        data = d

        return p, max_items_num_index

    except Exception:
        raise


def get_popular_price_detail(p, max_likes_num_index):
    try:
        chart_price_range = np.array([100, 200, 300, 400, 500, 600, 700, 800, 900, 1000])
        likes_num_arr = np.zeros(10)

        # 推奨価格帯（いいね数が最大になる価格帯）を取得
        max_popular_price = p['rounded_price_arr'][max_likes_num_index]

        price_range_int_arr = (int(max_popular_price) - 1000) + chart_price_range
        v_add_comma = np.vectorize(add_price_comma)
        price_range_arr_with_comma = v_add_comma(price_range_int_arr)

        max_likes_items = p['items_by_price_range'][max_popular_price]

        for item in max_likes_items:
            int_price = item['price']['int']

            # 価格を10の位で四捨五入
            rounded_int_price = round_half_up(int_price, '1E2')

            index = np.where(price_range_int_arr == rounded_int_price)[0][0]
            likes_num_arr[index] += item['likes']

        data['chart']['detail'] = {
            'priceLabels': price_range_arr_with_comma.tolist(),
            'likesNums': likes_num_arr.tolist(),
            'itemsNums': [],
        }

    except Exception:
        raise


def get_market_price_detail(p, max_num_index):
    try:
        chart_price_range = np.array([100, 200, 300, 400, 500, 600, 700, 800, 900, 1000])
        items_num_arr = np.zeros(10)

        # 推奨価格帯（いいね数が最大になる価格帯）を取得
        max_market_price = p['rounded_price_arr'][max_num_index]

        price_range_int_arr = (int(max_market_price) - 1000) + chart_price_range
        v_add_comma = np.vectorize(add_price_comma)
        price_range_arr_with_comma = v_add_comma(price_range_int_arr)

        market_price_items = p['items_by_price_range'][max_market_price]

        for item in market_price_items:
            int_price = item['price']['int']

            # 価格を10の位で四捨五入
            rounded_int_price = round_half_up(int_price, '1E2')
            index = np.where(price_range_int_arr == rounded_int_price)[0][0]
            items_num_arr[index] += 1

        data['chart']['detail'] = {
            'priceLabels': price_range_arr_with_comma.tolist(),
            'likesNums': [],
            'itemsNums': items_num_arr.tolist(),
        }

    except Exception:
        raise


def get_popular_price():
    try:
        p, max_likes_num_index = get_popular_price_range()

        if max_likes_num_index is not None:
            get_popular_price_detail(p, max_likes_num_index)

    except Exception:
        raise


def get_market_price():
    try:
        p, max_items_num_index = get_market_price_range()

        if max_items_num_index is not None:
            get_market_price_detail(p, max_items_num_index)

    except Exception:
        raise


async def analyze(form):
    try:
        plf = form['platform']
        p_type = form['priceType']
        const = base.get_params_by_platform(plf)
        headers = base.generate_headers(const)
        urls = generate_search_urls(form, const)

        kws = base.create_keyword_list(form)
        neg_kws = base.create_neg_keyword_list(form)

        cors = [scrape(u, kws, neg_kws, headers, plf, p_type, const) for u in urls]
        await asyncio.gather(*cors)

        if plf == 'mercari' and p_type == 'popular':
            get_popular_price()
        else:
            get_market_price()

        return data

    except Exception:
        raise


def execute(form):
    try:
        return asyncio.run(analyze(form))
        # result = asyncio.run(analyze(form))
        # return {
        #     'status': 'success',
        #     'result': result,
        #     'error': ''
        # }
    except Exception:
        raise
