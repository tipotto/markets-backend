import os
import sys
import asyncio
# from asyncio import AbstractEventLoop
import json
pydir_path = os.path.dirname(__file__)
if pydir_path not in sys.path:
    sys.path.append(pydir_path)
from services.search_service import SearchService
# from exceptions.input_error import InputError
# from types.search_service_type import SearchItemType, SearchFormType
# from typing import Tuple


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

        # if not form['keyword']:
        #     raise InputError('Keyword', 'Keyword is necessary.')

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
