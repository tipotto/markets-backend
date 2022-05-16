from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver
import json
import asyncio
from aiohttp import ClientSession
from google.oauth2.id_token import fetch_id_token
from google.auth.transport.requests import Request
from config.log_config import log_info, log_error
from constants.util import STATUS_SUCCESS, STATUS_ERROR, CLOUD_FUNCTION_URL
from constants.mercari import AUTH_TOKEN_PATH


async def fetch_json_by_post(url, hdrs, json_dict):
    async with ClientSession(headers=hdrs) as session:
        async with session.post(url, json=json_dict) as resp:
            return {
                'status': resp.status,
                'json': await resp.json()
            }


def fetch_google_auth_token():
    request = Request()
    id_token = fetch_id_token(request, CLOUD_FUNCTION_URL)
    return id_token


async def notify_status(status, json_dict):
    id_token = fetch_google_auth_token()
    hdrs = {
        'Content-Type': 'application/json',
        'X-Requested-With': 'aiohttp',
        'X-Requested-By': 'markets.jp',
        'Authorization': f'Bearer {id_token}',
    }
    json_dict['status'] = status
    return await fetch_json_by_post(CLOUD_FUNCTION_URL, hdrs, json_dict)


def get_request():
    options = Options()
    options.binary_location = '/usr/bin/google-chrome'
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--remote-debugging-port=9222')

    driver = webdriver.Chrome('/bin/chromedriver', options=options)
    driver.get('https://jp.mercari.com/search?keyword=%E6%B5%9C%E8%BE%BA%E7%BE%8E%E6%B3%A2%E3%80%80%E5%86%99%E7%9C%9F%E9%9B%86')
    req = driver.wait_for_request('https://api.mercari.jp/v2/entities:search', timeout=10)
    driver.quit()
    return req


def write_file(json_dict):
    with open(AUTH_TOKEN_PATH, 'wb') as f:
        json_str = json.dumps(json_dict, indent=4, ensure_ascii=False)
        json_bin = json_str.encode("utf-8")
        f.write(json_bin)


def output_log(res):
    if type(res) is not dict:
        return log_error(res)

    json = res['json']
    if res['status'] != 200:
        return log_error(json['error'])

    log_info(json['message'])


try:
    req = get_request()
    bytes_body = req.body
    body_dict = json.loads(bytes_body.decode('utf-8'))
    json_dict = {
        'dpop': req.headers['dpop'],
        'searchSessionId': body_dict['searchSessionId']
    }

    #print('dpop:', json_dict['dpop'])
    #print('searchSessionId:', json_dict['searchSessionId'])
    write_file(json_dict)
    res = asyncio.run(notify_status(STATUS_SUCCESS, json_dict))
    output_log(res)

except Exception:
    try:
        res = asyncio.run(notify_status(STATUS_ERROR, json_dict))
        output_log(res)

    except Exception as e:
        output_log(e)
