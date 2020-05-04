import requests
from bs4 import BeautifulSoup
import traceback
from constants import search as const


class SearchService:
    __keyword = None

    def __init__(self, param, hash):
        self.hash = hash
        self.referer = param['header']['referer']
        self.proxy = param['proxy']
        self.platform = param['platform']
        self.url = param['url']
        self.itemsSelector = param['items']['selector']
        self.titleSelector = param['title']['selector']
        self.titleAttr = param['title']['attr']
        self.priceSelector = param['price']['selector']
        self.imageSelector = param['image']['selector']
        self.imageAttr = param['image']['attr']
        self.detailSelector = param['detail']['selector']
        self.detailAttr = param['detail']['attr']

    @staticmethod
    def init(paramObj):
        platform = paramObj['platform']
        param = ''
        if platform == const.MERCARI:
            param = const.MERCARI_PARAM
        elif platform == const.RAKUTEN:
            param = const.RAKUTEN_PARAM
        else:
            param = const.PAYPAY_PARAM

        return SearchService(param, paramObj['hash'])

    @classmethod
    def setKeyword(cls, keyword):
        cls.__keyword = keyword

    def __getTitle(self, item):
        titles = item.select(self.titleSelector)
        if self.platform == const.PAYPAY:
            title = titles[0].get(self.titleAttr)
        else:
            title = titles[0].contents[0]
        return title

    def __getDetailUrl(self, item):
        if self.platform == const.PAYPAY:
            relativePath = item.get(self.detailAttr)
            detailUrl = const.BASE_URL[const.PAYPAY] + relativePath
        else:
            details = item.select(self.detailSelector)
            detailUrl = details[0].get(self.detailAttr)
        return detailUrl

    def __extract(self, item):

        # 商品名の取得
        title = self.__getTitle(item)

        # 金額の取得
        prices = item.select(self.priceSelector)
        price = prices[0].contents[0]
        price = int(price.replace("¥", "").replace(
            " ", "").replace(",", ""))

        # 商品画像URLの取得
        images = item.select(self.imageSelector)
        imageUrl = images[0].get(self.imageAttr)

        # 詳細ページURLの取得
        detailUrl = self.__getDetailUrl(item)

        data = {
            'title': title,
            'price': price,
            'imageUrl': imageUrl,
            'detailUrl': detailUrl,
            'platform': self.platform,
            'hash': self.hash
        }

        return data

    def search(self):

        # インスタンスメソッド内でクラス変数のkeywordにアクセス
        # self.keywordとしても可能
        site_url = self.url.format(SearchService.__keyword)

        # 全てのアイテムを取得
        proxies = {
            'http': self.proxy,
            'https': self.proxy
        }

        # headers = {
        #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        #     'Accept-Encoding': 'gzip, deflate, br',
        #     'Accept-Language': 'ja,en-US;q=0.9,en;q=0.8',
        #     'Referer': self.referer,
        #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        # }

        # Luminatiをプロキシとして使う場合
        html = requests.get(
            site_url, verify='/etc/ssl/certs/ca.pem', proxies=proxies)

        # Multitorをプロキシとして使う場合
        # html = requests.get(site_url, headers=headers, proxies=proxies)
        soup = BeautifulSoup(html.content, "html.parser")

        items = soup.select(self.itemsSelector)

        item_num = 0
        item_limit = 49
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

        return resultArray
