import hashlib
import os
from typing import AnyStr


def get_csci_salt() -> bytes:
    """Returns the appropriate salt for CSCI E-29"""
    # Hint: use os.environment and bytes.fromhex
    hex_salt = os.getenv('CSCI_SALT') or "3f87b3a5b7e48ba408964366a7194789249d4ed33b962a9e5d76c5d6122237bc"
    true_salt = bytes.fromhex(hex_salt) if hex_salt else None
    return true_salt


def hash_str(some_val: AnyStr, salt: AnyStr = ""):
    """Converts strings to hash digest

    See: https://en.wikipedia.org/wiki/Salt_(cryptography)

    :param some_val: thing to hash

    :param salt: Add randomness to the hashing
    """
    if isinstance(some_val, str):
        some_val = str.encode(some_val)

    if isinstance(salt, str):
        salt = str.encode(salt)

    var_to_encode = salt + some_val
    result = hashlib.sha256(var_to_encode).digest()
    return result


def get_user_id(username: str) -> str:
    # obtaining the CSCI_salt
    salt = get_csci_salt()
    # returning the hash of the user
    return hash_str(username.lower(), salt=salt).hex()[:8]
