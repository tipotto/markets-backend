import sys
import traceback
import re
import hashlib
# import time
from selenium import webdriver
import pandas
from selenium.webdriver.chrome.options import Options
from sqlalchemy import create_engine
from constants import search


class SearchService:
    __keyword = None
    __hashKeyword = None

    def __init__(self, param):
        self.proxy = param['proxy']
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
    def __moldKeyword(cls, keyword):
        return re.sub(r"\s+", "_", keyword)

    @classmethod
    def setKeyword(cls, keyword):
        cls.__keyword = keyword
        cls.__hashKeyword = cls.__moldKeyword(keyword)

    def __quitBrowser(self):
        self.browser.quit()

    def __setBrowser(self):
        options = Options()
        options.binary_location = '/usr/bin/google-chrome'
        options.add_argument('--headless')
        options.add_argument(f'--proxy-server={self.proxy}')

        browser = webdriver.Chrome('chromedriver', options=options)
        browser.implicitly_wait = 10
        self.browser = browser

    def __extract(self, item, hash_digest):

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
            'platform': platform,
            'hash': hash_digest
        }

        return data

    def __generateHash(self):
        byte_char = SearchService.__hashKeyword + \
            self.platform + "s5x9fpUD4k6SkDx8hgN6rMCP"
        return hashlib.sha1(byte_char.encode()).hexdigest()

    def search(self):

        # ハッシュの生成
        hash_digest = self.__generateHash()

        # Chromeの設定、起動
        self.__setBrowser()

        # インスタンスメソッド内でクラス変数のkeywordにアクセス
        # self.keywordとしても可能
        site_url = self.url.format(SearchService.__keyword)

        self.browser.get(site_url)

        # 全てのアイテムを取得
        # time.sleep(1)
        items = self.browser.find_elements_by_css_selector(self.itemsSelector)

        item_num = 0
        item_limit = 3
        resultArray = []
        try:
            for item in items:
                if item_num > item_limit:
                    break

                # 各アイテムから必要なデータを抽出
                resultObj = self.__extract(item, hash_digest)
                resultArray.append(resultObj)

                item_num += 1

                # 例外処理の挙動を確認するために、故意に例外を発生させる。
                # raise Exception

        except Exception as e:
            with open(r"./app/log/error.log", 'a') as f:
                traceback.print_exc(file=f)

            print(
                "Error occurred! Process was cancelled but the added items will be exported to database.")

        # Chromeの終了
        self.__quitBrowser()
        return resultArray
