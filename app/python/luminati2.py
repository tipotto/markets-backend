from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
PROXY = '127.0.0.1:24000'
# PROXY_AUTH = '{userid}:{password}'
options.binary_location = '/usr/bin/google-chrome'
options.add_argument('--headless')
options.add_argument('--proxy-server=http://%s' % PROXY)
# options.add_argument(f'--proxy-server=http://{PROXY}')
# option.add_argument('--proxy-auth=%s' % PROXY_AUTH)

browser = webdriver.Chrome('chromedriver', options=options)
browser.implicitly_wait = 10

data = browser.get('http://lumtest.com/myip.json')
print(data)

browser.quit()
