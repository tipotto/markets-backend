import sys
import json
import search


def main():

    # loads関数：文字列として受け取ったデータを辞書型に変換（デコード）
    data = json.loads(sys.stdin.readline())
    query = data['query']
    platforms = data['platforms']

    if len(platforms) == 0:
        print(json.dumps([]))
        return

    results = search.execute(query, platforms)
    print(json.dumps(list(results), ensure_ascii=False))


if __name__ == '__main__':
    main()
