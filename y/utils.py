import hashlib
import random


def hash_string(string: str) -> str:
    if not string:
        return string

    return hashlib.sha512(string.encode()).hexdigest()


def make_salt() -> str:
    return hash_string(str(random.random()))
