import asyncio
from aiohttp import ClientSession
from bs4 import BeautifulSoup
import traceback
from constants import search as const

# get: プロキシを使用する場合、session.getメソッドにproxyプロパティを渡す


async def get(url, headers, **kwargs):
    async with ClientSession(headers=headers) as session:
        async with session.get(url, **kwargs) as resp:
            return (await resp.text())


def checkPlatform(paramObj):
    platform = paramObj['platform']

    if platform == const.MERCARI:
        return const.MERCARI_PARAM
    elif platform == const.RAKUTEN:
        return const.RAKUTEN_PARAM
    else:
        return const.PAYPAY_PARAM


def getTitle(cons, item):
    titles = item.select(cons['title']['selector'])

    if cons['platform'] == const.PAYPAY:
        title = titles[0].get(cons['title']['attr'])
    else:
        title = titles[0].contents[0]
    return title


def getPrice(cons, item):
    prices = item.select(cons['price']['selector'])
    price = prices[0].contents[0]
    return int(price.replace("¥", "").replace(
        " ", "").replace(",", ""))


def getImageUrl(cons, item):
    images = item.select(cons['image']['selector'])
    return images[0].get(cons['image']['attr'])


def getDetailUrl(cons, item):
    platform = cons['platform']
    detailSelector = cons['detail']['selector']
    detailAttr = cons['detail']['attr']
    siteUrl = cons['siteUrl']

    if platform == const.MERCARI:
        details = item.select(detailSelector)
        detailUrl = siteUrl + details[0].get(detailAttr)

    elif platform == const.RAKUTEN:
        details = item.select(detailSelector)
        detailUrl = details[0].get(detailAttr)

    else:
        relativePath = item.get(detailAttr)
        detailUrl = siteUrl + relativePath

    return detailUrl


def extract(paramObj, cons, item):
    # 商品名の取得
    title = getTitle(cons, item)

    # 金額の取得
    price = getPrice(cons, item)

    # 商品画像URLの取得
    imageUrl = getImageUrl(cons, item)

    # 詳細ページURLの取得
    detailUrl = getDetailUrl(cons, item)

    data = {
        'title': title,
        'price': price,
        'imageUrl': imageUrl,
        'detailUrl': detailUrl,
        'platform': cons['platform'],
        'hash': paramObj['hash']
    }

    return data


async def scrape(sem, query, paramObj, hook=None):
    cons = checkPlatform(paramObj)

    url = cons['searchUrl'].format(query)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ja,en-US;q=0.9,en;q=0.8',
        'Referer': cons['header']['referer'],
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    }

    # Aiohttpでは、httpプロキシにしか対応していない（socksプロキシ使用不可）
    # プロキシのURLをStringで渡す
    # proxy = cons['proxy']

    async with sem:
        page = await get(url, headers, compress=True)

    soup = BeautifulSoup(page, "html.parser")
    items = soup.select(cons['items']['selector'])

    item_num = 0
    item_limit = 49
    resultArray = []
    try:
        for item in items:
            if item_num > item_limit:
                break

            # 各アイテムから必要なデータを抽出
            resultObj = extract(paramObj, cons, item)
            resultArray.append(resultObj)

            item_num += 1

            # 例外処理の挙動を確認するために、故意に例外を発生させる。
            # raise Exception

    # except Exception as e:
    except Exception:
        with open(r"./app/log/error.log", 'a') as f:
            traceback.print_exc(file=f)

        print("Error occurred! Process was cancelled but the added items will be exported to database.")

    if hook:
        hook(str(resultArray))

    return resultArray


async def parallel_by_gather(query, paramArr):
    sem = asyncio.Semaphore(5)

    def notify(resultArray):
        print("result >>> " + resultArray)

    cors = [scrape(sem, query, p) for p in paramArr]
    results = await asyncio.gather(*cors)
    return results


def execute(query, paramArr):
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(parallel_by_gather(query, paramArr))
    return results
