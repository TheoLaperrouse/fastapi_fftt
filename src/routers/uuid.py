import uuid
from fastapi import APIRouter

ALPHABET = '123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'

router = APIRouter(tags=["uuid"])


@router.get("/short_uuid_to_uuid/{short_uuid}")
def short_uuid_to_uuid(short_uuid):
    '''Convert short UUID to an UUID'''
    base = len(ALPHABET)
    uuid_int = sum(ALPHABET.index(c) * base ** i for i,
                   c in enumerate(reversed(short_uuid)))
    return str(uuid.UUID(int=uuid_int, version=4))


@router.get("/uuid_to_short_uuid/{uuidv4}")
def uuid_to_short_uuid(uuidv4):
    '''Convert an UUID to short UUID'''
    uuid_int = int(uuidv4.replace('-', ''), 16)
    base = len(ALPHABET)
    digits = []
    while uuid_int:
        uuid_int, remainder = divmod(uuid_int, base)
        digits.append(ALPHABET[remainder])
    return ''.join(reversed(digits))
