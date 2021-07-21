import os
import sys
import json
import asyncio
# 絶対パスでのインポートのためにモジュール探索パスを追加
pydir_path = os.path.dirname(__file__)
if pydir_path not in sys.path:
    sys.path.append(pydir_path)
import services.search_service as search


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

        data = asyncio.run(search.search(form))

        print(json.dumps({
            'status': 'success',
            'result': data,
            'error': ''
        }, ensure_ascii=False))

    except Exception:
        raise


if __name__ == '__main__':
    main()
