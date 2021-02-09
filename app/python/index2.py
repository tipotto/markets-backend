# import sys
# import json
from scrapy import signals
from scrapy.signalmanager import dispatcher
from scrapy.crawler import CrawlerProcess
# from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
# from scrapy.utils.serialize import ScrapyJSONEncoder
from scrapy_files.scrapy_files.spiders.search import SearchSpider


def spider_results():

    # loads関数：文字列として受け取ったデータを辞書型に変換（デコード）
    # form = json.loads(sys.stdin.readline())
    # query = form['query']
    # platforms = form['platforms']

    # if not query or len(platforms) == 0:
    #     print(json.dumps([]))
    #     return

    form = {
        'query': '日向坂46 斎藤京子',
        # platforms: mercari, rakuma, paypay
        'platforms': ['rakuma'],
        'minPrice': '1000',
        'maxPrice': '10000',
        'productStatus': ['brand_new', 'no_scratches_or_stains'],
        'salesStatus': 'selling',
        'deliveryCost': 'free',
        'sortOrder': 'asc'
    }

    platforms = form['platforms']

    results = []

    def crawler_results(signal, sender, item, response, spider):
        print('crawler_results', item)
        results.append(item)

    dispatcher.connect(crawler_results, signal=signals.item_scraped)

    process = CrawlerProcess(get_project_settings())
    for p in platforms:
        process.crawl(SearchSpider, platform=p, form=form)
    process.start()

    print("spider_results", results)

    # dumps関数：辞書型として受け取ったデータを文字列に変換（エンコード）
    # print(json.dumps(list(results), ensure_ascii=False))
    # print(json.dumps(results, ensure_ascii=False))


if __name__ == '__main__':
    spider_results()
