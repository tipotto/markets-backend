import sys
import json
import search


def main():

    # loads関数：文字列として受け取ったデータを辞書型に変換（デコード）
    data = json.loads(sys.stdin.readline())
    paramArr = data['paramArr']
    query = data['keyword']

    if len(paramArr) == 0:
        print(json.dumps([]))
        return

    results = search.execute(query, paramArr)
    print(json.dumps(list(results), ensure_ascii=False))


if __name__ == '__main__':
    main()
