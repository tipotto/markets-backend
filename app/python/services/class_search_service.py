import uuid
import math
from bs4 import BeautifulSoup
from constants import util, mercari, rakuma, paypay
from services.class_base_service import BaseService


class SearchService(BaseService):

    type: str = ''
    page: int = 1

    def __init__(self, const):
        super().__init__(const)
        self.url = self.generate_search_url()
        self.result = []
        self.pagers = 1

    @staticmethod
    def init(platform):
        try:
            if platform == mercari.SERVICE_NAME:
                return SearchService(mercari.DATA)
            elif platform == rakuma.SERVICE_NAME:
                return SearchService(rakuma.DATA)

            return SearchService(paypay.DATA)

        except Exception:
            raise

    @classmethod
    def set_class_properties(cls, form):
        try:
            super().set_class_properties(form)
            cls.type = form['type']
            cls.page = form['page']

        except Exception:
            raise

    def extract(self, item):
        try:
            # 商品名の取得
            title = super().get_title(item)

            if self.search_range == 'title' and super().is_each_keyword_contained(title) is False:
                return None

            if len(self.neg_keyword) != 0 and super().is_neg_keyword_contained(title) is True:
                return None

            # 金額の取得
            price = super().get_price(item)

            # 商品画像URLの取得
            image_url = super().get_image_url(item)

            # 詳細ページURLの取得
            detail_url = super().get_detail_url(item)

            return {
                'id': str(uuid.uuid4()),
                'title': title,
                'price': price,
                'imageUrl': image_url,
                'detailUrl': detail_url,
                'platform': self.platform,
                'isFavorite': False
            }

        except Exception:
            raise

    def get_price_query(self, key, value):
        try:
            if value == 0:
                return ''
            return self.query[key].format(value)

        except Exception:
            raise

    def get_category_query(self, category):
        try:
            main_value = category['main']
            sub_value = category['sub']

            if not main_value:
                return ''

            if not sub_value:
                return self.query['category'][main_value]

            return self.query['category'][main_value][sub_value]

        except Exception:
            raise

    def get_search_query(self):
        try:
            page = self.page
            keyword = self.keyword
            return self.query['search'].format(page, keyword)

        except Exception:
            raise

    def generate_query(self):
        try:
            query = ''
            for key, value in self.form.items():
                if key in ['type', 'page', 'keyword', 'negKeyword', 'platforms', 'searchRange', 'sortOrder']:
                    continue

                path = ''
                if key == 'category':
                    path = self.get_category_query(value)

                elif key == 'minPrice' or key == 'maxPrice':
                    path = self.get_price_query(key, value)

                elif key == 'productStatus':
                    path = super().get_product_status_query(value)

                else:
                    path = self.query[key][value]

                query += path

            return query

        except Exception:
            raise

    def generate_search_url(self):
        try:
            siteUrl = self.const['siteUrl']
            q = self.get_search_query()
            path = siteUrl + q
            query = self.generate_query()
            return (path if not query else path + query)

        except Exception:
            raise

    def get_page(self, pager):
        try:
            if self.type == 'next':
                return 0

            # これ以降はinitialの場合のみ実行
            if pager is None:
                # self.page == 1となる
                return self.page

            if self.platform == 'paypay':
                page_num_text = pager.contents[-3].replace(",", "")
                # print('page_num_text', page_num_text)

                page_num = int(page_num_text) / 100
                # print('page_num', page_num)

                return page_num if isinstance(page_num, int) else math.ceil(page_num)

            last_page_url = pager.get(self.const['pages']['attr'])
            # print('last_page_url', last_page_url)

            split_url = last_page_url.rsplit('page=', 1)[-1]
            # print('split_url', split_url)

            last_page_num_text = split_url.split('&', 1)[0]
            # print('last_page_num_text', last_page_num_text)

            return int(last_page_num_text)

        except Exception:
            raise

    async def scrape(self):
        try:
            page = await super().get(self.url, compress=True)
            # page = await get(url, headers, common.PROXY, compress=True)

            soup = BeautifulSoup(page, util.HTML_PARSER)

            pager = soup.select_one(self.const['pages']['selector'])
            self.pagers = self.get_page(pager)

            items = soup.select(self.const['items']['selector'])

            extract = self.extract
            append = self.result.append

            for item in items:

                i = extract(item)

                if i is None:
                    continue

                append(i)

            return {
                'items': self.result,
                'pages': self.pagers
            }

        except Exception:
            raise
