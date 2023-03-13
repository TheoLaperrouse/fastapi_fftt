import hmac
import hashlib
import random
import string
import time
import requests
import xmltodict
from dotenv import dotenv_values

config = dotenv_values(".env")
BASE_URL = 'http://www.fftt.com/mobile/pxml'

def sign_hmac_sha1(key, time_str):
    '''Sign with sha1'''
    hmac_object = hmac.new(key.encode('utf-8'), time_str.encode('utf-8'), hashlib.sha1)
    return hmac_object.hexdigest()


def connect_api(api, params=None):
    '''Connect to the FFTT database'''
    id_fftt = config['ID_FFTT']
    key = hashlib.md5(config['KEY_FFTT'].encode('utf-8')).hexdigest()
    serie = ''.join(random.choices(
        string.ascii_letters + string.digits, k=15)).upper()
    timestamp = int(round(time.time() * 1000))
    tmc = sign_hmac_sha1(key, str(timestamp))
    url = f"{BASE_URL}/{api}.php?serie={serie}&tm={timestamp}&tmc={tmc}&id={id_fftt}"
    if params is not None:
        url = f"{url}&{params}"
    try:
        response = requests.get(url, timeout=60)
        return xmltodict.parse(response.text).get('liste')
    except requests.exceptions.Timeout:
        print("Request timed out")
        return None
    except requests.exceptions.HTTPError as error:
        print(f"HTTP error occurred: {error}")
        return None
