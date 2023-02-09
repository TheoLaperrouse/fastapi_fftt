import hmac
import hashlib
import random
import time
import requests
from dotenv import dotenv_values
import xml.etree.ElementTree as ET

config = dotenv_values(".env")


def random_str(length):
    result = ""
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    characters_length = len(characters)
    for i in range(length):
        result += characters[random.randint(0, characters_length - 1)]
    return result


def sign_hmac_sha1(key, string):
    hmac_object = hmac.new(key.encode(
        'utf-8'), string.encode('utf-8'), hashlib.sha1)
    return hmac_object.hexdigest()


def connexion_api(api, params=None):
    ID = config['ID_FFTT']
    key = hashlib.md5(config['KEY_FFTT'].encode('utf-8')).hexdigest()
    serie = random_str(15)
    tm = int(round(time.time() * 1000))
    tmc = sign_hmac_sha1(key, str(tm))
    url = "http://www.fftt.com/mobile/pxml/{}.php?serie={}&tm={}&tmc={}&id={}".format(
        api, serie, tm, tmc, ID)
    if params is not None:
        url = "{}&{}".format(url, params)
    try:
        response = requests.get(url)
        root = ET.fromstring(response.text)
        return root
    except requests.exceptions.RequestException as e:
        print(e)
        return None
