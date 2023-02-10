import hmac
import hashlib
import random
import time
import string
import requests
from dotenv import dotenv_values
import xmltodict

config = dotenv_values(".env")


def sign_hmac_sha1(key, string):
    hmac_object = hmac.new(key.encode(
        'utf-8'), string.encode('utf-8'), hashlib.sha1)
    return hmac_object.hexdigest()


def connexion_api(api, params=None):
    ID = config['ID_FFTT']
    key = hashlib.md5(config['KEY_FFTT'].encode('utf-8')).hexdigest()
    serie = ''.join(random.choices(
        string.ascii_letters + string.digits, k=15)).upper()
    tm = round(time.time() * 1000)
    tmc = sign_hmac_sha1(key, str(tm))
    url = f"http://www.fftt.com/mobile/pxml/{api}.php?serie={serie}&tm={tm}&tmc={tmc}&id={ID}"

    if params is not None:
        url = f"{url}&{params}"
    try:
        response = requests.get(url)
        return xmltodict.parse(response.text)['liste']
    except requests.exceptions.RequestException as e:
        print(e)
        return None
