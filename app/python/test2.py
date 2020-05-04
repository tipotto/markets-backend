import requests
from bs4 import BeautifulSoup

url = 'https://www.mercari.com/jp/search/?keyword={}&status_on_sale=1'
site_url = url.format('日向坂46 渡邉美穂')

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

proxies = {
    'http': 'http://proxy.-----.co.jp/proxy.pac',
    'https': 'http://proxy.-----.co.jp/proxy.pac'
}

html = requests.get(site_url, proxies=proxies)
soup = BeautifulSoup(html.content, "html.parser")

# html = requests.get(site_url, headers=headers)
# html.raise_for_status()
# soup = BeautifulSoup(html.text, 'html.parser')
# print(soup.prettify())

# items = soup.select('.items-box')
items = soup.find_all("section", class_="items-box")

item_num = 0
item_limit = 9

for item in items:
    if item_num > item_limit:
        break

    item_num += 1

    titles = item.select('a > div.items-box-body > h3')
    title_text = titles[0].contents[0]

    prices = item.select(
        'a > div.items-box-body > div.items-box-num > div.items-box-price')
    price_text = prices[0].contents[0]

    print('title' + title_text)
    print('price' + price_text)
