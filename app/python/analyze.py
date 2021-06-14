import sys
import json
import asyncio_analyze as analyze


def main():

    # loads関数：文字列として受け取ったデータを辞書型に変換（デコード）
    form = json.loads(sys.stdin.readline())
    keyword = form['keyword']
    platforms = form['platforms']

    if not keyword or len(platforms) == 0:
        print(json.dumps({
            'status': 'failure',
            'results': [],
            'error': 'Necessary parameters, keyword and platforms, are not in the request.'
        }))
        return

    results = analyze.execute(form)
    # ensure_ascii=False: JSONの仕様により日本語が文字化けするのを防ぐ
    print(json.dumps(results, ensure_ascii=False))


if __name__ == '__main__':
    main()
