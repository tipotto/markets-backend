from bs4 import BeautifulSoup
import uuid
import asyncio
import numpy as np
from decimal import Decimal, ROUND_HALF_UP
from constants import util, mercari, rakuma, paypay
from services.class_base_service import BaseService


class AnalyzeService(BaseService):

    search_target: str = ''
    price_type: str = ''

    def __init__(self, const):
        super().__init__(const)
        self.urls = self.generate_search_urls()
        self.props = {
            'all_items': [],
            'rounded_price_arr': np.array([]),
            'raw_price_arr': np.array([]),
            'items_num_arr': np.array([]),
            'likes_num_arr': np.array([]),
            'items_by_price_range': {}
        }
        self.data = {
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

    @staticmethod
    def init(platform):
        try:
            if platform == mercari.SERVICE_NAME:
                return AnalyzeService(mercari.DATA)
            elif platform == rakuma.SERVICE_NAME:
                return AnalyzeService(rakuma.DATA)

            return AnalyzeService(paypay.DATA)

        except Exception:
            raise

    @classmethod
    def set_class_properties(cls, form):
        try:
            super().set_class_properties(form)
            cls.search_target = form['searchTarget']
            cls.price_type = form['priceType']

        except Exception:
            raise

    def get_search_urls(self):
        try:
            kw = self.keyword
            target = self.search_target
            pages = [1, 2, 3, 4, 5]
            return [self.site_url + self.query['analyze'][target].format(p, kw) for p in pages]

        except Exception:
            raise

    def generate_query(self):
        try:
            query = ''
            for key, value in self.form.items():
                path = ''
                if key == 'productStatus':
                    path = super().get_product_status_query(value)

                elif key == 'deliveryCost':
                    path = self.query['deliveryCost'][value]

                else:
                    continue

                query += path

            return query

        except Exception:
            raise

    def generate_search_urls(self):
        try:
            urls = self.get_search_urls()
            query = self.generate_query()
            return [u if not query else u + query for u in urls]

        except Exception:
            raise

    def get_likes(self, item):
        try:
            likes_selector = self.const['likes']['selector']

            # ラクマ、paypayフリマの場合
            if not likes_selector:
                return 0

            # メルカリでいいねがない場合、Noneが返る
            likes = item.select_one(likes_selector)
            return 0 if likes is None else int(likes.contents[0])

        except Exception:
            raise

    def extract_item(self, item):
        try:
            # 商品名の取得
            title = super().get_title(item)

            if self.search_range == 'title' and super().is_each_keyword_contained(title) is False:
                return {'data': None, 'error': 'keyword'}

            if len(self.neg_keyword) != 0 and super().is_neg_keyword_contained(title) is True:
                return {'data': None, 'error': 'neg_keyword'}

            # 金額の取得
            price = super().get_price(item)

            if price['str'] is None:
                return {'data': None, 'error': 'price'}

            # 商品画像URLの取得
            image_url = super().get_image_url(item)

            # 詳細ページURLの取得
            detail_url = super().get_detail_url(item)

            # いいねの取得
            likes = self.get_likes(item)

            if self.platform == 'mercari' and self.price_type == 'popular' and likes == 0:
                return {'data': None, 'error': 'likes'}

            result = {
                'id': str(uuid.uuid4()),
                'title': title,
                'price': price,
                'imageUrl': image_url,
                'detailUrl': detail_url,
                'platform': self.platform,
                'likes': likes
            }

            return {'data': result, 'error': None}

        except Exception:
            raise

    def extract_popular_price(self, item):
        try:
            props = self.props
            all_items_by_type = props['all_items']
            rounded_price_arr = props['rounded_price_arr']
            raw_price_arr = props['raw_price_arr']
            likes_num_arr = props['likes_num_arr']
            items_by_price_range = props['items_by_price_range']

            all_items_by_type.append(item)

            int_price = item['price']['int']
            raw_price_arr = np.append(raw_price_arr, int_price)

            # 価格を1000の位で切り上げる
            # もし価格が1000円未満の場合は、100の位で切り上げた結果を返す
            rounded_price = 0
            if int_price % 1000 == 0:
                rounded_price = int_price
            else:
                rounded_price = self.ceil(int_price, 1000)

            # フィールドにデータを追加
            if rounded_price in rounded_price_arr:
                index = np.where(rounded_price_arr == rounded_price)[0][0]
                likes_num_arr[index] += item['likes']
                items_by_price_range[rounded_price].append(item)

            else:
                rounded_price_arr = np.append(rounded_price_arr, rounded_price)
                likes_num_arr = np.append(likes_num_arr, item['likes'])
                items_by_price_range[rounded_price] = [item]

            self.props = {
                'all_items': all_items_by_type,
                'rounded_price_arr': rounded_price_arr,
                'raw_price_arr': raw_price_arr,
                # 'items_num_arr': np.array([]),
                'likes_num_arr': likes_num_arr,
                'items_by_price_range': items_by_price_range
            }

        except Exception:
            raise

    def extract_market_price(self, item):
        try:
            props = self.props
            all_items_by_type = props['all_items']
            rounded_price_arr = props['rounded_price_arr']
            raw_price_arr = props['raw_price_arr']
            items_num_arr = props['items_num_arr']
            items_by_price_range = props['items_by_price_range']

            all_items_by_type.append(item)

            int_price = item['price']['int']
            raw_price_arr = np.append(raw_price_arr, int_price)

            # 価格を1000の位で切り上げる
            # もし価格が1000円未満の場合は、100の位で切り上げた結果を返す
            rounded_price = 0
            if int_price % 1000 == 0:
                rounded_price = int_price
            else:
                rounded_price = self.ceil(int_price, 1000)

            # フィールドにデータを追加
            if rounded_price in rounded_price_arr:
                index = np.where(rounded_price_arr == rounded_price)[0][0]
                items_num_arr[index] += 1
                items_by_price_range[rounded_price].append(item)

            else:
                rounded_price_arr = np.append(rounded_price_arr, rounded_price)
                items_num_arr = np.append(items_num_arr, 1)
                items_by_price_range[rounded_price] = [item]

            self.props = {
                'all_items': all_items_by_type,
                'rounded_price_arr': rounded_price_arr,
                'raw_price_arr': raw_price_arr,
                'items_num_arr': items_num_arr,
                # 'likes_num_arr': np.array([]),
                'items_by_price_range': items_by_price_range
            }

        except Exception:
            raise

    async def scrape(self, url):
        try:
            page = await super().get(url, compress=True)

            soup = BeautifulSoup(page, util.HTML_PARSER)
            items = soup.select(self.const['items']['selector'])

            platform = self.platform
            price_type = self.price_type
            extract = self.extract_item
            extract_popular_price = self.extract_popular_price
            extract_market_price = self.extract_market_price

            for item in items:
                i = extract(item)
                data = i['data']
                err = i['error']

                if err in ['keyword', 'neg_keyword', 'price']:
                    continue

                if err == 'likes':
                    break

                if platform == 'mercari' and price_type == 'popular':
                    extract_popular_price(data)
                else:
                    extract_market_price(data)

        except Exception:
            raise

    # 四捨五入
    def round_half_up(self, price, str_digit):
        try:
            d_str_price = Decimal(str(price))
            return int(d_str_price.quantize(Decimal(str_digit), rounding=ROUND_HALF_UP))

        except Exception:
            raise

    # 切り上げ
    def ceil(self, price, range):
        try:
            return ((int)(price / range) + 1) * range

        except Exception:
            raise

    # 切り捨て
    def floor(self, price, range):
        try:
            return (int)(price / range) * range

        except Exception:
            raise

    def get_likes_num(self, price):
        try:
            rounded_price_arr = self.props['rounded_price_arr']
            likes_num_arr = self.props['likes_num_arr']

            arr = np.where(rounded_price_arr == price)[0]
            if len(arr) == 0:
                return 0

            return likes_num_arr[arr[0]]

        except Exception:
            raise

    def get_items_num(self, price):
        try:
            items_by_price_range = self.props['items_by_price_range']

            if price in items_by_price_range:
                items = items_by_price_range[price]
                return len(items)

            return 0

        except Exception:
            raise

    def add_price_comma(self, price):
        try:
            return '{:,}'.format(price)

        except Exception:
            raise

    def change_price_unit(self, price):
        try:
            str_price = str(price).replace("000", "")
            return str_price if str_price == '0' else str_price + 'k'

        except Exception:
            raise

    def get_chart_price_label(self, max_price_range):
        try:
            min_price_range = max_price_range - 1000
            return ' '.join([self.change_price_unit(min_price_range), '-', self.change_price_unit(max_price_range)])

        except Exception:
            raise

    def get_whole_price_data_for_popular(self):
        try:
            p = self.props

            if len(p['rounded_price_arr']) == 0:
                return None

            int_max_rounded_price = int(np.amax(p['rounded_price_arr']))
            int_min_rounded_price = int(np.amin(p['rounded_price_arr']))
            int_price_range_arr = np.arange(int_min_rounded_price, int_max_rounded_price + 1000, 1000)

            v_get_label = np.vectorize(self.get_chart_price_label)
            chart_price_label_arr = v_get_label(int_price_range_arr)

            v_get_likes_num = np.vectorize(self.get_likes_num)
            chart_likes_num_arr = v_get_likes_num(int_price_range_arr)

            self.data['chart']['whole'] = {
                'priceLabels': chart_price_label_arr.tolist(),
                'likesNums': chart_likes_num_arr.tolist(),
                'itemsNums': [],
            }

            return p, v_get_label, v_get_likes_num

        except Exception:
            raise

    def get_whole_price_data_for_market(self):
        try:
            p = self.props

            if len(p['rounded_price_arr']) == 0:
                return None

            int_max_rounded_price = int(np.amax(p['rounded_price_arr']))
            int_min_rounded_price = int(np.amin(p['rounded_price_arr']))
            int_price_range_arr = np.arange(int_min_rounded_price, int_max_rounded_price + 1000, 1000)

            v_get_label = np.vectorize(self.get_chart_price_label)
            chart_price_label_arr = v_get_label(int_price_range_arr)

            v_get_items_num = np.vectorize(self.get_items_num)
            chart_items_num_arr = v_get_items_num(int_price_range_arr)

            self.data['chart']['whole'] = {
                'priceLabels': chart_price_label_arr.tolist(),
                'likesNums': [],
                'itemsNums': chart_items_num_arr.tolist(),
            }

            return p, v_get_label, v_get_items_num

        except Exception:
            raise

    def get_popular_price_range(self):
        chart_price_range = np.array([1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000])
        try:
            p, v_get_label, v_get_likes_num = self.get_whole_price_data_for_popular()

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
                floored_max_popular_price = self.floor(max_popular_price, 10000)

            int_price_range_arr = chart_price_range + floored_max_popular_price

            chart_price_label_arr = v_get_label(int_price_range_arr)

            chart_likes_num_arr = v_get_likes_num(int_price_range_arr)

            # 平均価格を算出
            avg_price = np.mean(p['raw_price_arr'])

            # 平均価格を小数点で四捨五入
            int_avg_price = self.round_half_up(avg_price, '0')

            # 最低価格を算出
            min_price = np.amin(p['raw_price_arr'])

            # 最高価格を算出
            max_price = np.amax(p['raw_price_arr'])

            self.data['items']['all']['list'] = p['all_items']
            self.data['items']['market']['list'] = items_in_market_price

            add_price_comma = self.add_price_comma
            self.data['price'] = {
                'min': add_price_comma(int(min_price)),
                'max': add_price_comma(int(max_price)),
                'average': add_price_comma(int_avg_price),
                'market': {
                    'min': add_price_comma(int(min_popular_price)),
                    'max': add_price_comma(int(max_popular_price))
                }
            }

            self.data['chart']['range'] = {
                'priceLabels': chart_price_label_arr.tolist(),
                'likesNums': chart_likes_num_arr.tolist(),
                'itemsNums': [],
            }

            return max_likes_index

        except Exception:
            raise

    def get_market_price_range(self):
        chart_price_range = np.array([1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000])
        try:
            p, v_get_label, v_get_items_num = self.get_whole_price_data_for_market()

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
                floored_max_market_price = self.floor(max_market_price, 10000)

            int_price_range_arr = chart_price_range + floored_max_market_price

            chart_price_label_arr = v_get_label(int_price_range_arr)

            chart_items_num_arr = v_get_items_num(int_price_range_arr)

            # 平均価格を算出
            avg_price = np.mean(p['raw_price_arr'])

            # 平均価格を小数点で四捨五入
            int_avg_price = self.round_half_up(avg_price, '0')

            # 最低価格を算出
            min_price = np.amin(p['raw_price_arr'])

            # 最高価格を算出
            max_price = np.amax(p['raw_price_arr'])

            self.data['items']['all']['list'] = p['all_items']
            self.data['items']['market']['list'] = items_in_market_price

            add_price_comma = self.add_price_comma
            self.data['price'] = {
                'min': add_price_comma(int(min_price)),
                'max': add_price_comma(int(max_price)),
                'average': add_price_comma(int_avg_price),
                'market': {
                    'min': add_price_comma(int(min_market_price)),
                    'max': add_price_comma(int(max_market_price))
                }
            }

            self.data['chart']['range'] = {
                'priceLabels': chart_price_label_arr.tolist(),
                'likesNums': [],
                'itemsNums': chart_items_num_arr.tolist(),
            }

            return max_items_num_index

        except Exception:
            raise

    # def add_likes_num(self, item, price_range_int_arr):
    #     try:
    #         int_price = item['price']['int']

    #         # 価格を10の位で四捨五入
    #         rounded_int_price = self.round_half_up(int_price, '1E2')

    #         index = np.where(price_range_int_arr == rounded_int_price)[0][0]
    #         self.likes_num_arr[index] += item['likes']

    #     except Exception:
    #         raise

    # def add_items_num(self, item, price_range_int_arr):
    #     try:
    #         int_price = item['price']['int']

    #         # 価格を10の位で四捨五入
    #         rounded_int_price = self.round_half_up(int_price, '1E2')
    #         index = np.where(price_range_int_arr == rounded_int_price)[0][0]
    #         self.items_num_arr[index] += 1

    #     except Exception:
    #         raise

    def get_popular_price_detail(self, max_likes_num_index):
        try:
            chart_price_range = np.array([100, 200, 300, 400, 500, 600, 700, 800, 900, 1000])
            likes_num_arr = np.zeros(10)
            p = self.props

            # 推奨価格帯（いいね数が最大になる価格帯）を取得
            max_popular_price = p['rounded_price_arr'][max_likes_num_index]

            price_range_int_arr = (int(max_popular_price) - 1000) + chart_price_range
            v_add_comma = np.vectorize(self.add_price_comma)
            price_range_arr_with_comma = v_add_comma(price_range_int_arr)

            max_likes_items = p['items_by_price_range'][max_popular_price]

            # v_add_likes_num = np.vectorize(self.add_likes_num)
            # v_add_likes_num(max_likes_items, price_range_int_arr)

            for item in max_likes_items:
                int_price = item['price']['int']

                # 価格を10の位で四捨五入
                rounded_int_price = self.round_half_up(int_price, '1E2')

                index = np.where(price_range_int_arr == rounded_int_price)[0][0]
                likes_num_arr[index] += item['likes']

            self.data['chart']['detail'] = {
                'priceLabels': price_range_arr_with_comma.tolist(),
                'likesNums': likes_num_arr.tolist(),
                'itemsNums': [],
            }

        except Exception:
            raise

    def get_market_price_detail(self, max_num_index):
        try:
            chart_price_range = np.array([100, 200, 300, 400, 500, 600, 700, 800, 900, 1000])
            items_num_arr = np.zeros(10)
            p = self.props

            # 推奨価格帯（いいね数が最大になる価格帯）を取得
            max_market_price = p['rounded_price_arr'][max_num_index]

            price_range_int_arr = (int(max_market_price) - 1000) + chart_price_range
            v_add_comma = np.vectorize(self.add_price_comma)
            price_range_arr_with_comma = v_add_comma(price_range_int_arr)

            market_price_items = p['items_by_price_range'][max_market_price]

            # v_add_items_num = np.vectorize(self.add_items_num)
            # v_add_items_num(np.array(market_price_items), price_range_int_arr)

            for item in market_price_items:
                int_price = item['price']['int']

                # 価格を10の位で四捨五入
                rounded_int_price = self.round_half_up(int_price, '1E2')
                index = np.where(price_range_int_arr == rounded_int_price)[0][0]
                items_num_arr[index] += 1

            self.data['chart']['detail'] = {
                'priceLabels': price_range_arr_with_comma.tolist(),
                'likesNums': [],
                'itemsNums': items_num_arr.tolist(),
            }

        except Exception:
            raise

    def get_popular_price(self):
        try:
            max_likes_num_index = self.get_popular_price_range()

            if max_likes_num_index is not None:
                self.get_popular_price_detail(max_likes_num_index)

        except Exception:
            raise

    def get_market_price(self):
        try:
            max_items_num_index = self.get_market_price_range()

            if max_items_num_index is not None:
                self.get_market_price_detail(max_items_num_index)

        except Exception:
            raise

    async def execute(self):
        try:
            cors = [self.scrape(u) for u in self.urls]
            await asyncio.gather(*cors)

            if self.platform == 'mercari' and self.price_type == 'popular':
                self.get_popular_price()
            else:
                self.get_market_price()

            return self.data

        except Exception:
            raise
