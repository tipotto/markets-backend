import asyncio
from bs4 import BeautifulSoup
import numpy as np
from aiohttp import ClientOSError, ClientPayloadError
from decimal import Decimal, ROUND_HALF_UP
from constants import rakuten
from constants.util import PLATFORM_TYPE_WEB, PLATFORM_TYPE_API, HTML_PARSER
import services.util_service as util


props = {
    'all_items': [],
    'rounded_price_arr': np.array([]),
    'raw_price_arr': np.array([]),
    'items_num_arr': np.array([]),
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
            'itemsNums': [],
        },
        'range': {
            'priceLabels': [],
            'itemsNums': [],
        },
        'detail': {
            'priceLabels': [],
            'itemsNums': [],
        }
    }
}


# 四捨五入
def round_half_up(price, str_digit):
    d_str_price = Decimal(str(price))
    return int(d_str_price.quantize(Decimal(str_digit), rounding=ROUND_HALF_UP))


# 切り上げ
def ceil(price, range):
    return ((int)(price / range) + 1) * range


# 切り捨て
def floor(price, range):
    return (int)(price / range) * range


def ceil_price(price, int_digit):
    if price % int_digit == 0:
        return price
    return ceil(price, int_digit)


def floor_price(max_market_price):
    # 相場価格の上限値を10000の位で切り下げ
    # max_market_priceが10000の倍数の場合：
    # max_market_price = 10000なら0、それ以外ならmax_market_price - 10000
    # max_market_priceが10000の倍数でない場合：
    # max_market_priceを10000の位で切り下げ
    # 10000未満の値は0, それ以上の値は10000の位の下限値に切り下げ（20000, 30000, 40000...）
    if max_market_price % 10000 == 0:
        if max_market_price == 10000:
            return 0
        return int(max_market_price - 10000)

    return floor(max_market_price, 10000)


def extract_market_price(item, prop):
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
    rounded_price = ceil_price(int_price, 1000)

    # フィールドにデータを追加
    if rounded_price in rounded_price_arr:
        index = np.where(rounded_price_arr == rounded_price)[0][0]
        items_num_arr[index] += 1
        items_by_price_range[rounded_price].append(item)

    else:
        rounded_price_arr = np.append(rounded_price_arr, rounded_price)
        items_num_arr = np.append(items_num_arr, 1)
        items_by_price_range[rounded_price] = [item]

    return {
        'all_items': all_items_by_type,
        'rounded_price_arr': rounded_price_arr,
        'raw_price_arr': raw_price_arr,
        'items_num_arr': items_num_arr,
        'items_by_price_range': items_by_price_range
    }


def get_items_num(price):
    items_by_price_range = props['items_by_price_range']
    if price not in items_by_price_range:
        return 0
    items = items_by_price_range[price]
    return len(items)


def change_price_unit(price):
    str_price = str(price).replace("000", "")
    return str_price if str_price == '0' else str_price + 'k'


def get_whole_price_chart_label(max_price_range):
    min_price_range = max_price_range - 1000
    return ' '.join([change_price_unit(min_price_range), '-', change_price_unit(max_price_range)])


def get_market_price_chart_label(max_price_range):
    min_price_range = max_price_range - 100
    return ' '.join([util.add_price_comma(min_price_range), '-', util.add_price_comma(max_price_range)])


def get_market_price():
    global data
    d = data
    p = props

    # アイテム数が0の場合は終了
    if len(p['all_items']) == 0:
        return

    # 平均価格を算出
    avg_price = np.mean(p['raw_price_arr'])

    # 平均価格を小数点で四捨五入
    int_avg_price = round_half_up(avg_price, '0')

    # 最低価格を算出
    min_price = int(np.amin(p['raw_price_arr']))

    # 最高価格を算出
    max_price = int(np.amax(p['raw_price_arr']))

    # アイテム数が最大値となるインデックスを取得
    # 最大値が存在する場合、現状では最初のインデックスを返す
    # TODO: 複数存在する場合の処理を検討する
    max_items_num_index = np.argmax(p['items_num_arr'])

    # 相場価格帯: アイテム数が最大になる価格帯
    # 相場価格の上限値を取得
    max_market_price = int(p['rounded_price_arr'][max_items_num_index])

    # 相場価格の下限値を取得
    min_market_price = max_market_price - 1000

    # 相場価格帯に含まれるアイテムリストを取得
    items_in_market_price = p['items_by_price_range'][max_market_price]

    # 相場価格の上限値を10000の位で切り下げ
    floored_max_market_price = floor_price(max_market_price)

    # リストを作成し、その各要素にfloored_max_market_priceを加算したリストを作成
    # floored_max_market_price = 10000の場合:
    # int_price_range_arr = [11000, 12000, 13000, 14000, 15000... 20000]
    chart_price_range = np.array(
        [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000])
    int_price_range_arr = chart_price_range + floored_max_market_price

    v_get_label, v_get_items_num, whole_price_data = get_market_price_whole(p)

    detail_price_data = get_market_price_detail(p, min_market_price, max_market_price)
    chart_price_label_arr = v_get_label(int_price_range_arr)
    chart_items_num_arr = v_get_items_num(int_price_range_arr)

    d['items']['all']['list'] = p['all_items']
    d['items']['market']['list'] = items_in_market_price
    d['price'] = {
        'min': util.add_price_comma(min_price),
        'max': util.add_price_comma(max_price),
        'average': util.add_price_comma(int_avg_price),
        'market': {
            'min': util.add_price_comma(min_market_price),
            'max': util.add_price_comma(max_market_price)
        }
    }
    d['chart']['whole'] = whole_price_data
    d['chart']['range'] = {
        'priceLabels': chart_price_label_arr.tolist(),
        'itemsNums': chart_items_num_arr.tolist(),
    }
    d['chart']['detail'] = detail_price_data
    data = d


def get_market_price_whole(p):
    # 1000円単位で分類した価格リストを取得
    rounded_price_arr = p['rounded_price_arr']

    # 価格帯の最大値を取得
    # rounded_price_arrは、1000円単位の価格帯リスト
    int_max_rounded_price = int(np.amax(rounded_price_arr))

    # 価格帯の最小値を取得
    int_min_rounded_price = int(np.amin(rounded_price_arr))

    # 1000刻みの等差配列を作成
    # 範囲は、min <= n < (max + 1000)
    # min=1000, max=10000の場合、1000 <= n < (10000 + 1000)のリストとなる。
    # リスト上限を10000+1000とすることで、10000もリストに含まれる。
    # result = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
    int_price_range_arr = np.arange(
        int_min_rounded_price, int_max_rounded_price + 1000, 1000)

    # 等差配列のラベルリストを作成
    v_get_label = np.vectorize(get_whole_price_chart_label)
    chart_price_label_arr = v_get_label(int_price_range_arr)

    # 各価格帯のアイテム数リストを作成
    v_get_items_num = np.vectorize(get_items_num)
    chart_items_num_arr = v_get_items_num(int_price_range_arr)

    whole_price_data = {
        'priceLabels': chart_price_label_arr.tolist(),
        'itemsNums': chart_items_num_arr.tolist(),
    }

    return v_get_label, v_get_items_num, whole_price_data


def get_market_price_detail(p, min_market_price, max_market_price):
    # 100円刻みの相場価格リストを作成
    chart_price_range = np.array(
        [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000])
    price_range_int_arr = chart_price_range + min_market_price

    # 相場価格のラベルリストを作成
    v_get_m_label = np.vectorize(get_market_price_chart_label)
    price_range_arr_with_comma = v_get_m_label(price_range_int_arr)

    market_price_items = p['items_by_price_range'][max_market_price]

    # items_num_arr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    items_num_arr = np.zeros(10, dtype=int)

    for item in market_price_items:
        int_price = item['price']['int']

        # 価格を100の位で切り上げ
        rounded_int_price = ceil_price(int_price, 100)

        index = np.where(price_range_int_arr == rounded_int_price)[0][0]
        items_num_arr[index] += 1

    return {
        'priceLabels': price_range_arr_with_comma.tolist(),
        'itemsNums': items_num_arr.tolist(),
    }


def get_pages_list(plf):
    if plf == rakuten.SERVICE_NAME:
        return [1, 2, 3]
    return [1, 2, 3, 4, 5]


def extract(items, form, cons, kws, neg_kws, plf):
    type = cons['type']
    cons_item = cons['data']['res']['params'][type]['item']

    global props
    p = props
    for item in items:
        if cons_item is not None:
            item = item[cons_item['key']]

        i = util.extract_item(item, form, cons, kws, neg_kws, plf)
        if not i:
            continue

        p = extract_market_price(i, p)

    props = p


async def run_api(form, cons, params, hdrs, plf, page, kws, neg_kws):

    def _page():
        keys = cons_req['keys']
        cons_web = cons_req['params'][PLATFORM_TYPE_WEB]
        return util.set_page_param('page', page, keys['page'], type, plf, params, cons_web)

    async def _fetch():
        url = cons_req['url'][PLATFORM_TYPE_API]
        if hdrs is not None:
            return await util.fetch_json_by_post(url, hdrs, params)
        return await util.fetch_json_by_get(url, params)

    type = cons['type']
    cons_data = cons['data']
    cons_req = cons_data['req']
    cons_res = cons_data['res']['params'][type]

    params = _page()
    res = await _fetch()
    items = res[cons_res['items']['key']]
    extract(items, form, cons, kws, neg_kws, plf)


async def scrape(form, cons, url, hdrs, plf, page, kws, neg_kws):

    def _page():
        cons_req = cons_data['req']
        keys = cons_req['keys']
        cons_web = cons_req['params'][PLATFORM_TYPE_WEB]
        return util.set_page_param('page', page, keys['page'], type, plf, url, cons_web)

    type = cons['type']
    cons_data = cons['data']
    cons_res = cons_data['res']['params'][type]

    url = _page()
    res = await util.fetch_html(url, hdrs, compress=False)
    bs = BeautifulSoup(res, HTML_PARSER)
    items = bs.select(cons_res['items']['key'])
    extract(items, form, cons, kws, neg_kws, plf)


async def fetch_from_api(form, cons, plf, kws, neg_kws):
    prms = util.generate_params(form, cons, plf)
    hdrs, prms = util.set_auth_token(cons, prms, plf)
    cors = [run_api(form, cons, prms, hdrs, plf, p, kws, neg_kws)
            for p in get_pages_list(plf)]
    await asyncio.gather(*cors)


async def fetch_from_web(form, cons, plf, kws, neg_kws):
    hdrs = util.generate_headers(cons['data']['req'])
    url = util.generate_search_url(form, cons, plf)
    cors = [scrape(form, cons, url, hdrs, plf, p, kws, neg_kws)
            for p in get_pages_list(plf)]
    await asyncio.gather(*cors)


async def fetch(form, cons, plf, kws, neg_kws):
    if cons['type'] == PLATFORM_TYPE_WEB:
        return await fetch_from_web(form, cons, plf, kws, neg_kws)
    return await fetch_from_api(form, cons, plf, kws, neg_kws)


async def analyze(form):
    try:
        util.ignore_aiohttp_ssl_error(asyncio.get_running_loop())
        plf = form['platform']
        cons = util.get_params_by_platform(plf)

        if util.should_exit_by_sales_status(form, cons):
            return data

        kws = util.create_keyword_list(form)
        neg_kws = util.create_neg_keyword_list(form)
        await fetch(form, cons, plf, kws, neg_kws)
        get_market_price()
        return data

    except ClientOSError or ClientPayloadError:
        pass
