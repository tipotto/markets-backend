from scrapy import Spider, Request
from bs4 import BeautifulSoup
from scrapy_search import generate_url, generate_headers, extract
from constants import common


class SearchSpider(Spider):
    name = 'search'
    # 設定しなくても問題ない？
    # allowed_domains = ['www.mercari.com']

    def __init__(self, platform, form={}, *args, **kwargs):
        # print('__init__ start')
        super(SearchSpider, self).__init__(*args, **kwargs)
        const, url = generate_url(form, platform)
        self.const = const
        self.url = url
        self.headers = generate_headers(const)

        # プロキシを使用する場合は以下を追加
        # self.proxy = {'proxy': common.PROXY}

    def start_requests(self):
        # print('start_requests start')

        # プロキシを使用する場合は以下と差し替え
        # yield Request(self.url, headers=self.headers, meta=self.proxy)
        yield Request(self.url, headers=self.headers)


def parse(self, response):
    # print('parse start')

    soup = BeautifulSoup(response.text, common.HTML_PARSER)
    items = soup.select(self.const['items']['selector'])
    # items = soup.select(self.const['items']['selector'],
    #                     limit=common.ITEM_NUMBER)
    for item in items:
        yield extract(self.const, item)
