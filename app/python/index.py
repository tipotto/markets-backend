import sys
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from search import SearchService

# loads関数：文字列として受け取ったデータを辞書型に変換（デコード）
data = json.loads(sys.stdin.readline())
pfArray = data['pfArray']
keyword = data['keyword']

# ChromeDriverのセットアップ
SearchService.setScraping(keyword)

for platform in pfArray:
    resultJson = SearchService.init(platform).search()

    # dumps関数：辞書型のデータを文字列に変換（エンコード）
    print(json.dumps(resultJson, ensure_ascii=False))

# ChromeDriverの終了
SearchService.quitScraping()
