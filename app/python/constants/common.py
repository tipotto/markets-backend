PROXY = "http://127.0.0.1:16379"

HTML_PARSER = "html.parser"

ITEM_NUMBER = 100

OS_LIST = ['win', 'mac']
BROWSER_LIST = ['chrome', 'firefox']
# OS_LIST = ['win', 'mac', 'lin']
# BROWSER_LIST = ['chrome', 'firefox', 'opera']

HEADERS_DICT = {
    "mac-firefox": {
        "User-Agent": "",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "ja,en-US,en;q=0.5",
        "Referer": "",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    },
    "win-firefox": {
        "User-Agent": "",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "ja,en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    },
    "mac-chrome": {
        "Connection": "keep-alive",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Dest": "document",
        "Referer": "",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ja,en-GB,en-US;q=0.9,en;q=0.8"
    },
    "win-chrome": {
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Referer": "",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ja,en-US,en;q=0.9"
    }
}