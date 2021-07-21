import os
import sys
import json
import asyncio
# 絶対パスでのインポートのためにモジュール探索パスを追加
pydir_path = os.path.dirname(__file__)
if pydir_path not in sys.path:
    sys.path.append(pydir_path)
import services.analyze_service as analyze


def main():
    try:
        # loads関数：文字列として受け取ったデータを辞書型に変換（デコード）
        form = json.loads(sys.stdin.readline())
        data = asyncio.run(analyze.analyze(form))

        print(json.dumps({
            'status': 'success',
            'result': data,
            'error': ''
        }, ensure_ascii=False))

    except Exception:
        raise

# def test():
#     form = {
#         # 'page': 1,
#         # 'searchType': 'market',
#         'keyword': 'PS5 本体',
#         'platforms': ['mercari'],
#         # 'platforms': ['mercari', 'rakuma', 'paypay'],
#         'productStatus': ['all'],
#         'deliveryCost': 'all',
#         'keywordFilter': 'use',
#     }

#     try:
#         if not form['keyword']:
#             raise InputError('Keyword', 'Keyword is necessary.')

#         loop = asyncio.get_event_loop()
#         data = loop.run_until_complete(analyze(form))
#         print('-- main --')
#         print(data[0])

#     except InputError as e:
#         print('error', e.message)

#     except Exception as e:
#         print('error', e)


if __name__ == "__main__":
    main()
