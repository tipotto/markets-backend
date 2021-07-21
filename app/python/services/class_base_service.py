import random
import re
import numpy as np
from aiohttp import ClientSession
from fake_headers import Headers
from constants import util, mercari, rakuma, paypay


class BaseService():

    form: dict = {}
    keyword: str = ''
    keyword_arr: list = []
    neg_keyword: str = ''
    neg_keyword_arr: list = []    
    search_range: str = ''

    def __init__(self, const):
        self.const = const
        self.platform = const['platform']
        self.site_url = const['siteUrl']
        self.referer = const['referer']
        self.query = const['query']
        self.headers = self.generate_headers()

    @classmethod
    def split_keyword(cls, keyword):

        # if not keyword:
        #     return

        # keywordの先頭と末尾の空白を削除
        removed = keyword.strip()

        # keywordに空白（全角、半角、タブ文字）が含まれているかチェック
        # 含まれていれば、空白で分割してリストにする
        # 含まれていなければ、keywordリストを作成
        if re.search(util.KEYWORD_REG_EXP, removed):
            return re.split(util.KEYWORD_REG_EXP, removed)

        return [keyword]

    @classmethod
    def set_class_properties(cls, form):
        try:
            if form['searchRange'] == 'title':
                cls.keyword_arr = cls.split_keyword(form['keyword'])

            if len(form['negKeyword']) != 0:
                cls.neg_keyword = form['negKeyword']
                cls.neg_keyword_arr = cls.split_keyword(form['negKeyword'])

            cls.form = form
            cls.keyword = form['keyword']
            cls.search_range = form['searchRange']

        except Exception:
            raise

    async def get(self, url, **kwargs):
        try:
            async with ClientSession(headers=self.headers) as session:
                async with session.get(url, **kwargs) as resp:
                    return (await resp.text())

        except Exception:
            raise

    def generate_headers(self):
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
            headers['Referer'] = self.referer
            return headers

        except Exception:
            raise

    def get_product_status_query(self, values):
        try:
            path = ''
            if ('all' in values):
                # 空文字が返される
                path = self.query['productStatus']['all']

            else:
                for status in values:
                    path += self.query['productStatus'][status]

            return path

        except Exception:
            raise

    def get_title(self, item):
        try:
            titles = item.select(self.const['title']['selector'])
            if self.platform == paypay.SERVICE_NAME:
                return titles[0].get(self.const['title']['attr'])

            return titles[0].contents[0]

        except Exception:
            raise

    def get_price(self, item):
        try:
            prices = item.select(self.const['price']['selector'])
            price = prices[0].contents[0]
            price_str = price.replace("¥", "").replace("円", "").replace(" ", "")

            if price_str == '???':
                return {'str': None, 'int': 0}

            price_int = int(price_str.replace(",", ""))
            return {'str': price_str, 'int': price_int}

        except Exception:
            raise

    def get_image_url(self, item):
        try:
            images = item.select(self.const['image']['selector'])
            return images[0].get(self.const['image']['attr'])

        except Exception:
            raise

    def get_detail_url(self, item):
        try:
            platform = self.platform
            detail_selector = self.const['detail']['selector']
            detail_attr = self.const['detail']['attr']

            if platform == mercari.SERVICE_NAME:
                details = item.select(detail_selector)
                return self.site_url + details[0].get(detail_attr)

            elif platform == rakuma.SERVICE_NAME:
                details = item.select(detail_selector)
                return details[0].get(detail_attr)

            relativePath = item.get(detail_attr)
            return self.site_url + relativePath

        except Exception:
            raise

    def check_keyword_in_title(self, keyword, title):
        try:
            return True if keyword in title else False

        except Exception:
            raise

    def is_neg_keyword_contained(self, title):
        try:
            v_check_title = np.vectorize(self.check_keyword_in_title)
            results = v_check_title(self.neg_keyword_arr, title)
            return True if True in results else False

        except Exception:
            raise

    def is_each_keyword_contained(self, title):
        try:
            v_check_title = np.vectorize(self.check_keyword_in_title)
            results = v_check_title(self.keyword_arr, title)
            return False if False in results else True

        except Exception:
            raise
