import uuid

alphabet = '123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'


def translator(x): return int(x.replace('-', ''), 16)


def enlarge_uuid(short_uuid):
    base = len(alphabet)
    n = len(short_uuid)
    x = 0
    for i in range(n):
        x += alphabet.index(short_uuid[i]) * (base ** (n-i-1))
    return str(uuid.UUID(int=x, version=4))


def shorten_uuid(uuid_str):
    x = translator(uuid_str)
    base = len(alphabet)
    digits = []
    while x > 0:
        digits.append(alphabet[x % base])
        x //= base
    digits.reverse()
    return ''.join(digits)
