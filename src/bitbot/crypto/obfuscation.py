"""Key obfuscation for BitBot crypto."""

import deal
from beartype import beartype

from bitbot.crypto.constants import OBF_CHAR_MAP


@deal.pre(lambda key: len(key) > 0, message="Key cannot be empty")
@deal.post(lambda result: len(result) > 0)
@beartype
def get_obfuscated_key(key: str) -> str:
    """Apply character substitution obfuscation to cipher key."""
    o_key = ""
    for char in key.lower():
        code = ord(char)
        o_key += chr(OBF_CHAR_MAP.get(code, code))
    return o_key
