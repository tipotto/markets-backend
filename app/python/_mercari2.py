import sys
import time
from selenium import webdriver
import pandas
from selenium.webdriver.chrome.options import Options

options = Options()
options.binary_location = '/usr/bin/google-chrome'
options.add_argument('--headless')
options.add_argument('--window-size=1280,1024')

# 引数から取得 実行例：python merscraping.py
args = sys.argv
query = args[1]

# 別途ダウンロードしたchromedriver.exeの場所を指定
browser = webdriver.Chrome('chromedriver', options=options)
browser.implicitly_wait = 10

url_site = "https://www.mercari.com/jp/search/?keyword={}&status_on_sale=1".format(
    query)
browser.get(url_site)

page = 1
item_num = 0
urls = []

# 個別商品ページのURLを全取得
while True:
    print("Getting the page {}...".format(page))
    time.sleep(1)
    items = browser.find_elements_by_css_selector(".items-box")
    for item in items:
        item_num += 1
        item_url = item.find_element_by_css_selector("a").get_attribute("href")
        print("item{0} url:{1}".format(item_num, item_url))
        urls.append(item_url)

    page += 1
    try:
        next = browser.find_element_by_css_selector(
            "li.pager-next .pager-cell:nth-child(1) a").get_attribute("href")
        print("next url:{}".format(next))
        print("Moving to the next page...")
        browser.get(next)
    except:
        print("Last page!")
        break

# 取得した全URLをfor文で回す
item_num = 0
columns = ["title", "cat1", "cat2", "cat3", "brand", "state", "price", "url"]
df = pandas.DataFrame(columns=columns)

try:  # エラーで途中終了しても途中までの分をcsvに書き出したいのでtry～except文
    for url in urls:
        item_num += 1
        print("Moving to the item{}...".format(item_num))
        time.sleep(1)
        browser.get(url)

        title = browser.find_element_by_css_selector("h1.item-name").text
        print("Getting the information of {}...".format(title))

        cat1_css = "table.item-detail-table tbody tr:nth-child(2) td a:nth-child(1) div"
        cat2_css = "table.item-detail-table tbody tr:nth-child(2) td a:nth-child(2) div"
        cat3_css = "table.item-detail-table tbody tr:nth-child(2) td a:nth-child(3) div"

        cat1 = browser.find_element_by_css_selector(cat1_css).text
        cat2 = browser.find_element_by_css_selector(cat2_css).text
        cat3 = browser.find_element_by_css_selector(cat3_css).text
        try:  # 存在しない⇒a, divタグがない場合があるのでtry～except文
            brand = browser.find_element_by_css_selector(
                "table.item-detail-table tbody tr:nth-child(3) td a div").text
        except:
            brand = ""
        state = browser.find_element_by_css_selector(
            "table.item-detail-table tbody tr:nth-child(4) td").text
        price = browser.find_element_by_xpath(
            "//div[1]/section/div[2]/span[1]").text  # PC表示
        price = price.replace("¥", "").replace(" ", "").replace(",", "")

        print(cat1)
        print(cat2)
        print(cat3)
        print(brand)
        print(state)
        print(price)
        print(url)

        se = pandas.Series([title, cat1, cat2, cat3, brand,
                            state, price, url], columns)
        df = df.append(se, ignore_index=True)

        print("Item {} added!".format(item_num))
except:
    print("Error occurred! Process cancelled but the added items will be exported to .csv")

df.to_csv("{}.csv".format(query), index=False, encoding="utf_8_sig")
browser.quit()
print("Done!")
