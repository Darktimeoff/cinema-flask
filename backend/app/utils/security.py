import calendar
import datetime
import hmac
from base64 import b64decode, b64encode
from hashlib import pbkdf2_hmac

import jwt

from .main import get_env


def str_to_hashfunc(s: str) -> str:
    hash_digest = pbkdf2_hmac(
        get_env('HASH_ALG'),
        s.encode('utf-8'),
        get_env('SALT'),
        get_env('HASH_ITR'),
    )

    return b64encode(hash_digest)


def compare_hashfunc(hash_func: str, s2: str) -> bool:
    hash_func2 = b64decode(str_to_hashfunc(s2))
    hash_func = b64decode(hash_func)

    return hmac.compare_digest(hash_func, hash_func2)


def generate_jwt(data: dict, delta) -> str:
    timedelta = datetime.datetime.utcnow() + delta

    delta['exp'] = calendar.timegm(timedelta.timetuple())

    return jwt.encode(
        payload=data,
        key=get_env('JWT_SECRET'),
        algorithm=get_env('JWT_ALG')
    )


def decode_jwt(token: str) -> dict:
    return jwt.decode(token, get_env('JWT_SECRET'), get_env('JWT_ALG'))


def get_access_token(data):
    delta = datetime.timedelta(minutes=int(get_env('TOKEN_EXPIRE_MINUTES')))

    return generate_jwt(data, delta)


def get_refresh_token(data):
    delta = datetime.timedelta(minutes=int(get_env('TOKEN_EXPIRE_DAYS')))

    return generate_jwt(data, delta)
