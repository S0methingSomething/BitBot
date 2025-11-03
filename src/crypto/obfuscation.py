"""Key obfuscation for BitBot crypto."""

from beartype import beartype

from .constants import OBF_CHAR_MAP


@beartype
def get_obfuscated_key(key: str) -> str:
    """Apply character substitution obfuscation to cipher key."""
    o_key = ""
    for char in key.lower():
        code = ord(char)
        o_key += chr(OBF_CHAR_MAP.get(code, code))
    return o_key
