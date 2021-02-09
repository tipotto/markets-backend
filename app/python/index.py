import sys
import json
import asyncio_search as search


def main():

    # loads関数：文字列として受け取ったデータを辞書型に変換（デコード）
    form = json.loads(sys.stdin.readline())
    query = form['query']
    platforms = form['platforms']

    if not query or len(platforms) == 0:
        print(json.dumps([]))
        return

    results = search.execute(form)
    print(json.dumps(list(results), ensure_ascii=False))


if __name__ == '__main__':
    main()
