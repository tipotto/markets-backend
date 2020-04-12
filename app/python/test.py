# スリープを使うために必要
import time
# Webブラウザを自動操作する（python -m pip install selenium)
from selenium import webdriver
# import chromedriver_binary

options = webdriver.ChromeOptions()
options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
chrome_driver_binary = "/home/vagrant/.local/lib/python3.6/site-packages/chromedriver_binary/chromedriver"
driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)


# options = webdriver.ChromeOptions()
# # options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
# options.binary_location = "/home/vagrant/.local/lib/python3.6/site-packages/chromedriver_binary/chromedriver"
# # chrome_driver_binary = "/home/vagrant/.local/lib/python3.6/site-packages/chromedriver_binary/chromedriver"

# driver = webdriver.Chrome(options=options)
# driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)

# driver = webdriver.Chrome(
#     executable_path='/home/vagrant/.local/lib/python3.6/site-packages/chromedriver_binary/chromedriver'
# )

driver.get('https://www.google.com/')  # Googleを開く
time.sleep(5)                          # 5秒間待機
