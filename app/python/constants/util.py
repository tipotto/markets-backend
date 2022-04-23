PLATFORM_TYPE_WEB = 'web'
PLATFORM_TYPE_API = 'api'
HTML_PARSER = 'html.parser'
LOGGER_NAME = 'refresh_token'
STATUS_SUCCESS = 'success'
STATUS_ERROR = 'error'
CLOUD_FUNCTION_URL = 'https://us-central1-markets-jp.cloudfunctions.net/markets-refresh-token-slack-notifier'
# PRICE_ASC_DESC_ITEM_NUMBER = 12
# PRICE_LIKES_ITEM_NUMBER = 30
OS_LIST = ['win', 'mac']
BROWSER_LIST = ['chrome', 'firefox']
SEARCH_BLACKLIST = [
    'type',
    'platforms',
    'sortOrder'
]
ANALYZE_BLACKLIST = [
    'page',
    'platform',
    'sortOrder'
]

# PROXY = "http://127.0.0.1:16379"
# OS_LIST = ['win', 'mac', 'lin']
# BROWSER_LIST = ['chrome', 'firefox', 'opera']
# ALL_ITEM_NUMBER = 100
# LIKES_ITEM_NUMBER = 30

# 検索キーワードに関する正規表現
# 全角スペース、半角スペース、タブ文字（\t）
# 改行コード（\n, \r）、改ページ（\f）を含む
KEYWORD_REG_EXP = r'\s+'
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
