from typing import AnyStr
from os import environ
from functools import wraps
from hashlib import sha256
from itertools import chain


def get_csci_salt() -> bytes:
    """Returns the appropriate salt for CSCI E-29

    :return: salt
    :rtype: bytes
    """
    return bytes.fromhex(environ["CSCI_SALT"])


def str_to_bytes(func):
    """Wrapper decorator to convert string input to bytes input

    wrapper changes all string inputs both in regular and in keyword parameters to bytes
    all other types stay unchanged"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        args = [x.encode() if isinstance(x, str) else x for x in args]
        kwargs = {
            key: (value.encode() if isinstance(value, str) else value)
            for key, value in kwargs.items()
        }
        return func(*args, **kwargs)

    return wrapper


def input_filter(input_type):
    """Decorator that returns a wrapper that filters input for type

    if any input is not of type input_type a TypeError is raised"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for x in chain(args, kwargs.values()):
                if not isinstance(x, input_type):
                    raise TypeError(
                        "Function {} expects {} input but received {}".format(
                            func.__name__, input_type, type(x)
                        )
                    )
            return func(*args, **kwargs)

        return wrapper

    return decorator


@str_to_bytes
@input_filter(bytes)
def hash_str(some_val: AnyStr, salt: AnyStr = ""):
    """Converts strings to hash digest

    See: https://en.wikipedia.org/wiki/Salt_(cryptography)

    :param some_val: str or bytes: thing to hash

    :param salt: str or bytes, Add randomness to the hashing

    :return: hashed output

    :rtype: bytes
    """

    # hash digest concatenation of salt and some_val and return
    return sha256(salt + some_val).digest()


def get_user_id(username: str) -> str:
    """Get last 4 bytes of hashed user id as a hexadecimal string

        :param str username: unhashed username

        :return: last 4 bytes of hashed user id

        :rtype: str
        """
    salt = get_csci_salt()
    return hash_str(username.lower(), salt=salt).hex()[:8]
