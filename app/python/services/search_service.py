import math
import asyncio
import numpy as np
from aiohttp import ClientOSError, ClientPayloadError
from bs4 import BeautifulSoup
from constants import mercari, rakuma, paypay, yahooAuction, amazon
from constants.util import PLATFORM_TYPE_WEB, PLATFORM_TYPE_API, HTML_PARSER
import services.util_service as util


result: list = []
pager: list = []


def get_total_page(elem, form, plf):

    def _mercari():
        str_page_num = elem['meta']['numFound']
        return int(str_page_num) / 120

    def _paypay():
        str_page_num = elem.contents[-3].replace(",", "")
        return int(str_page_num) / 100

    def _rakuma():
        split_url = elem.rsplit('page=', 1)[-1]
        last_page_num_text = split_url.split('&', 1)[0]
        return int(last_page_num_text)

    def _yahoo_auction():
        str_page_num = elem.text.replace("件", "").replace(",", "")
        return int(str_page_num) / 50

    def _amazon():
        try:
            str_page_num = elem.text.split()[1]
        except IndexError:
            str_page_num = elem.text.split('件', 1)[0]
        finally:
            return int(str_page_num.replace(",", "")) / 48

    # これ以降はinitialの場合のみ実行
    if elem is None:
        return form['page']

    page = 0
    if plf == mercari.SERVICE_NAME:
        page = _mercari()

    elif plf == rakuma.SERVICE_NAME:
        page = _rakuma()

    elif plf == paypay.SERVICE_NAME:
        page = _paypay()

    elif plf == amazon.SERVICE_NAME:
        page = _amazon()

    elif plf == yahooAuction.SERVICE_NAME:
        page = _yahoo_auction()

    return page if isinstance(page, int) else math.ceil(page)


def extract(items, form, cons, kws, neg_kws, plf):
    type = cons['type']
    cons_item = cons['data']['res']['params'][type]['item']

    global result
    arr = result
    append = arr.append
    for item in items:
        if cons_item is not None:
            item = item[cons_item['key']]

        i = util.extract_item(item, form, cons, kws, neg_kws, plf)
        if not i:
            continue

        append(i)

    result = arr


async def run_api(form, cons, kws, neg_kws, plf):

    def _page():
        if plf == mercari.SERVICE_NAME:
            return pager.append(get_total_page(res, form, plf))
        pager.append(res[cons_res['pages']['key']])

    async def _fetch():
        url = cons_data['req']['url'][PLATFORM_TYPE_API]
        params = util.generate_params(form, cons, plf)
        headers, params = util.set_auth_token(cons, params, plf)

        if headers is not None:
            return await util.fetch_json_by_post(url, headers, params)
        return await util.fetch_json_by_get(url, params)

    cons_data = cons['data']
    cons_res = cons_data['res']['params'][cons['type']]

    res = await _fetch()
    items = res[cons_res['items']['key']]
    extract(items, form, cons, kws, neg_kws, plf)
    _page()


async def scrape(form, cons, kws, neg_kws, plf):

    async def _fetch():
        headers = util.generate_headers(cons_data['req'])
        url = util.generate_search_url(form, cons, plf)
        res = await util.fetch_html(url, headers, compress=True)
        bs = BeautifulSoup(res, HTML_PARSER)
        return bs

    def _page():
        if form['type'] != 'initial':
            return

        cons_pages = cons_res['pages']
        elem = bs.select_one(cons_pages['key'])

        if cons_pages['attr'] is not None:
            elem = elem.get(cons_pages['attr'])

        int_total = get_total_page(elem, form, plf)
        pager.append(int_total)

    cons_data = cons['data']
    cons_res = cons_data['res']['params'][cons['type']]

    bs = await _fetch()
    items = bs.select(cons_res['items']['key'])
    extract(items, form, cons, kws, neg_kws, plf)
    _page()


async def fetch(form, kws, neg_kws, plf):
    cons = util.get_params_by_platform(plf)

    if util.should_exit_by_sales_status(form, cons):
        return

    if cons['type'] == PLATFORM_TYPE_WEB:
        return await scrape(form, cons, kws, neg_kws, plf)
    return await run_api(form, cons, kws, neg_kws, plf)


async def search(form):
    try:
        util.ignore_aiohttp_ssl_error(asyncio.get_running_loop())
        kws = util.create_keyword_list(form)
        neg_kws = util.create_neg_keyword_list(form)

        cors = [fetch(form, kws, neg_kws, p) for p in form['platforms']]
        await asyncio.gather(*cors)

        max_page = 0 if len(pager) == 0 else np.amax(np.array(pager))

        return {
            'items': result,
            'pages': int(max_page)
        }

    except ClientOSError or ClientPayloadError:
        pass
