from hashlib import pbkdf2_hmac
from .main import get_env
from base64 import b64encode, b64decode
import hmac

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