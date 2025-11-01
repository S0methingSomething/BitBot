"""Key obfuscation for BitBot crypto."""

import deal
from beartype import beartype

from crypto.constants import OBF_CHAR_MAP


@deal.pre(lambda key: len(key) > 0)
@deal.post(lambda result: len(result) > 0)
@beartype
def get_obfuscated_key(key: str) -> str:
    """Applies a simple character substitution obfuscation to the cipher key."""
    o_key = ""
    for char in key.lower():
        code = ord(char)
        o_key += chr(OBF_CHAR_MAP.get(code, code))
    return o_key
