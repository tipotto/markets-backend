import traceback
import sys
# import time
from selenium import webdriver
import pandas
from selenium.webdriver.chrome.options import Options
from sqlalchemy import create_engine

# データベースの接続情報
# DBの接続処理に時間がかかっている可能性あり。
# TODO 毎回接続するのはコストがかかるので、コネクションプールを利用することを検討。
# TODO DBの接続やchromeDriverの処理は、別ファイルに切り出して共通化することを検討。
db_config = {
    'user': 'tipotto',
    'password': 'L1keana5234',
    'host': 'localhost',
    # 'port': 'ポート番号',  # なくてもOK
    'database': 'my_app'
}

url = 'mysql+pymysql://{user}:{password}@{host}/{database}?charset=utf8'.format(
    **db_config)

engine = create_engine(url, echo=False)

options = Options()
options.binary_location = '/usr/bin/google-chrome'
options.add_argument('--headless')
options.add_argument('--window-size=1280,1024')

# TODO メルカリとラクマでスクレイピング処理を共通化する。
# node.jsからオブジェクトを渡すようにし、cssセレクタやアクセス先のURL、
# プラットフォーム名をconstantsに切り出すようにする。
query = sys.stdin.readline()

# 別途ダウンロードしたchromedriver.exeの場所を指定
browser = webdriver.Chrome('chromedriver', options=options)
browser.implicitly_wait = 10

url_site = "https://www.mercari.com/jp/search/?keyword={}&status_on_sale=1".format(
    query)
browser.get(url_site)

columns = ["title", "price", "imageUrl", "itemUrl", "platform"]
df = pandas.DataFrame(columns=columns)

# 個別商品ページのURLを全取得
# time.sleep(1)
items = browser.find_elements_by_css_selector(".items-box")
item_num = 0
item_limit = 2

try:
    for item in items:
        if item_num > item_limit:
            break

        item_num += 1

        # 商品名の取得
        title = item.find_element_by_css_selector(
            "a > div.items-box-body > h3").text

        # 金額の取得
        price = item.find_element_by_css_selector(
            "a > div.items-box-body > div.items-box-num > div.items-box-price").text
        price = price.replace("¥", "").replace(" ", "").replace(",", "")

        # 商品画像URLの取得
        imageUrl = item.find_element_by_css_selector(
            "a > figure.items-box-photo > img").get_attribute("data-src")

        # 詳細ページURLの取得
        itemUrl = item.find_element_by_css_selector("a").get_attribute("href")

        # プラットフォーム名の設定
        platform = "mercari"

        se = pandas.Series(
            [title, price, imageUrl, itemUrl, platform], columns)
        df = df.append(se, ignore_index=True)

        # 例外処理の挙動を確認するために、故意に例外を発生させる。
        # raise Exception

except Exception as e:
    with open(r"./app/log/error.log", 'a') as f:
        traceback.print_exc(file=f)

    print("Error occurred! Process was cancelled but the added items will be exported to database.")

# df.to_csv("{}.csv".format(query), index=False, encoding="utf_8_sig")
df.to_sql('items', engine, index=False, if_exists='append')
browser.quit()
print("mercari done!")
