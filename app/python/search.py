import traceback
import sys
# import time
from selenium import webdriver
import pandas
from selenium.webdriver.chrome.options import Options
from sqlalchemy import create_engine
from constants import search


class SearchService:
    browser = None
    keyword = None

    def __init__(self, param):
        self.socks = param['socks']
        self.platform = param['platform']
        self.url = param['url']
        self.itemsSelector = param['items']['selector']
        self.titleSelector = param['title']['selector']
        self.priceSelector = param['price']['selector']
        self.imageSelector = param['image']['selector']
        self.imageAttr = param['image']['attr']
        self.detailSelector = param['detail']['selector']
        self.detailAttr = param['detail']['attr']

    @staticmethod
    def init(platform):
        param = ''
        if platform == 'mercari':
            param = search.MERCARI

        elif platform == 'rakuten':
            param = search.RAKUTEN

        return SearchService(param)

    @classmethod
    def quitScraping(cls):
        cls.browser.quit()

    @classmethod
    def setScraping(cls, keyword):

        socks = 'socks5://127.0.0.1:9000'

        options = Options()
        options.binary_location = '/usr/bin/google-chrome'
        options.add_argument('--headless')
        options.add_argument('--window-size=1280,1024')
        options.add_argument(f'--proxy-server={socks}')

        browser = webdriver.Chrome('chromedriver', options=options)
        browser.implicitly_wait = 10

        cls.browser = browser
        cls.keyword = keyword

    def extract(self, item):

        # 商品名の取得
        title = item.find_element_by_css_selector(
            self.titleSelector).text

        # 金額の取得
        price = item.find_element_by_css_selector(
            self.priceSelector).text
        price = int(price.replace("¥", "").replace(
            " ", "").replace(",", ""))

        # 商品画像URLの取得
        imageUrl = item.find_element_by_css_selector(
            self.imageSelector).get_attribute(self.imageAttr)

        # 詳細ページURLの取得
        detailUrl = item.find_element_by_css_selector(
            self.detailSelector).get_attribute(self.detailAttr)

        # プラットフォーム名の設定
        platform = self.platform

        data = {
            'title': title,
            'price': price,
            'imageUrl': imageUrl,
            'detailUrl': detailUrl,
            'platform': platform
        }

        return data

    def search(self):
        url_site = self.url.format(SearchService.keyword)

        # インスタンスメソッド内でクラス変数にアクセス（selfからでも可能）
        browser = SearchService.browser
        browser.get(url_site)

        # 全てのアイテムを取得
        # time.sleep(1)
        items = browser.find_elements_by_css_selector(self.itemsSelector)

        item_num = 0
        item_limit = 2
        resultArray = []
        try:
            for item in items:
                if item_num > item_limit:
                    break

                # 各アイテムから必要なデータを抽出
                resultObj = self.extract(item)
                resultArray.append(resultObj)

                item_num += 1

                # 例外処理の挙動を確認するために、故意に例外を発生させる。
                # raise Exception

        except Exception as e:
            with open(r"./app/log/error.log", 'a') as f:
                traceback.print_exc(file=f)

            print(
                "Error occurred! Process was cancelled but the added items will be exported to database.")

        return resultArray
