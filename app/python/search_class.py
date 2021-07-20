import os
import sys
import asyncio
# from asyncio import AbstractEventLoop
# 絶対パスでのインポートのためにモジュール探索パスを追加
import json
pydir_path = os.path.dirname(__file__)
if pydir_path not in sys.path:
    sys.path.append(pydir_path)
from services.search_service_class import SearchService

async def search(form):
    try:
        platforms = form['platforms']
        SearchService.set_class_properties(form)
        cors = [SearchService.init(p).scrape() for p in platforms]
        return await asyncio.gather(*cors)

    except Exception:
        raise


def main():
    try:
        # loads関数：文字列として受け取ったデータを辞書型に変換（デコード）
        form = json.loads(sys.stdin.readline())

        # form = {
        #     'page': 1,
        #     'category': {'main': '', 'sub': ''},
        #     'keyword': '浜辺美波　写真集',
        #     'negKeyword': '',
        #     # platforms: mercari, rakuma, paypay
        #     'platforms': ['mercari'],
        #     'minPrice': 0,
        #     'maxPrice': 0,
        #     'productStatus': ['all'],
        #     'salesStatus': 'all',
        #     'deliveryCost': 'all',
        #     'sortOrder': 'asc',
        #     'keywordFilter': 'use'
        # }

        arr = asyncio.run(search(form))

        print(json.dumps({
            'status': 'success',
            'result': arr,
            'error': ''
        }, ensure_ascii=False))

    except Exception:
        raise


if __name__ == '__main__':
    main()
