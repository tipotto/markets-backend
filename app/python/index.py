import sys
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from search import SearchService
# import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

# # loads関数：文字列として受け取ったデータを辞書型に変換（デコード）
# data = json.loads(sys.stdin.readline())
# pfArray = data['pfArray']
# keyword = data['keyword']

# # 検索ワードの設定
# SearchService.setKeyword(keyword)

# for platform in pfArray:
#     resultJson = SearchService.init(platform).search()

#     # dumps関数：辞書型のデータを文字列に変換（エンコード）
#     print(json.dumps(resultJson, ensure_ascii=False))

# 検索ワードの設定
# SearchService.setKeyword(keyword)

# resultArray = []
# for platform in pfArray:
#     resultJson = SearchService.init(platform).search()
#     resultArray.append(resultJson)

# print(json.dumps(resultArray, ensure_ascii=False))


def setKeyword(keyword):
    SearchService.setKeyword(keyword)


def search(platform):
    return SearchService.init(platform).search()


def main():

    # loads関数：文字列として受け取ったデータを辞書型に変換（デコード）
    data = json.loads(sys.stdin.readline())
    pfArray = data['pfArray']
    keyword = data['keyword']

    # 検索ワードの設定
    setKeyword(keyword)

    with ThreadPoolExecutor(max_workers=2, thread_name_prefix="thread") as executor:
        results = executor.map(search, pfArray)

    print(json.dumps(list(results), ensure_ascii=False))


if __name__ == '__main__':
    main()
