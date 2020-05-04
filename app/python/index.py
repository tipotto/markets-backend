import sys
import json
from search import SearchService
from concurrent.futures import ThreadPoolExecutor


def setKeyword(keyword):
    SearchService.setKeyword(keyword)


def search(paramObj):
    return SearchService.init(paramObj).search()


def main():

    # loads関数：文字列として受け取ったデータを辞書型に変換（デコード）
    data = json.loads(sys.stdin.readline())
    paramArr = data['paramArr']
    keyword = data['keyword']

    if len(paramArr) == 0:
        print(json.dumps([]))
        return

    # 検索ワードの設定
    setKeyword(keyword)

    with ThreadPoolExecutor(max_workers=3, thread_name_prefix="thread") as executor:
        results = executor.map(search, paramArr)

    print(json.dumps(list(results), ensure_ascii=False))


if __name__ == '__main__':
    main()
