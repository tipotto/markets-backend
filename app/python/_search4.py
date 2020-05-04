# import sys
import traceback
# import time
from selenium import webdriver
# import pandas
from selenium.webdriver.chrome.options import Options
# from sqlalchemy import create_engine
from constants import search
from selenium.webdriver.common.proxy import Proxy, ProxyType
# from selenium.webdriver.common.proxy import *


class SearchService:
    __keyword = None

    def __init__(self, param, hash):
        self.hash = hash
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
    def init(paramObj):
        param = ''
        if paramObj['platform'] == 'mercari':
            param = search.MERCARI

        elif paramObj['platform'] == 'rakuten':
            param = search.RAKUTEN

        return SearchService(param, paramObj['hash'])

    @classmethod
    def setKeyword(cls, keyword):
        cls.__keyword = keyword

    def __quitBrowser(self):
        self.browser.quit()

    # def __setBrowser(self):
    #     options = Options()
    #     options.binary_location = '/usr/bin/google-chrome'
    #     options.add_argument('--headless')
    #     options.add_argument('--ignore-certificate-errors')
    #     options.add_argument(f'--proxy-server={self.proxy}')

    #     browser = webdriver.Chrome('chromedriver', options=options)
    #     browser.implicitly_wait = 10
    #     self.browser = browser

    def __setBrowser(self):
        options = Options()
        options.binary_location = '/usr/bin/google-chrome'
        options.add_argument('--headless')
        options.add_argument('--ignore-certificate-errors')

        proxy = Proxy()
        proxy.proxy_type = ProxyType.MANUAL
        proxy.http_proxy = self.proxy
        proxy.ftp_proxy = self.proxy
        proxy.sslProxy = self.proxy

        capabilities = webdriver.DesiredCapabilities.CHROME
        proxy.add_to_capabilities(capabilities)

        browser = webdriver.Chrome(
            'chromedriver', options=options, desired_capabilities=capabilities)
        browser.implicitly_wait = 10
        self.browser = browser

    def __extract(self, item):

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
            'hash': self.hash
        }

        return data

    def search(self):

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
        item_limit = 29
        resultArray = []
        try:
            for item in items:
                if item_num > item_limit:
                    break

                # 各アイテムから必要なデータを抽出
                resultObj = self.__extract(item)
                resultArray.append(resultObj)

                item_num += 1

                # 例外処理の挙動を確認するために、故意に例外を発生させる。
                # raise Exception

        # except Exception as e:
        except Exception:
            with open(r"./app/log/error.log", 'a') as f:
                traceback.print_exc(file=f)

            print(
                "Error occurred! Process was cancelled but the added items will be exported to database.")

        # Chromeの終了
        self.__quitBrowser()
        return resultArray
