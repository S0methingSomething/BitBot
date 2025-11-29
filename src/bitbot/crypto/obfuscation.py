"""Key obfuscation for game asset encryption.

NOTE: OBF_CHAR_MAP only handles lowercase a-z. Uppercase letters, numbers,
and special characters pass through unchanged.
"""

import icontract
from beartype import beartype

from bitbot.crypto.constants import OBF_CHAR_MAP


@icontract.require(lambda key: len(key) > 0, description="Key cannot be empty")
@icontract.ensure(lambda result: len(result) > 0, description="Obfuscated key cannot be empty")
@beartype
def get_obfuscated_key(key: str) -> str:
    """Apply character substitution obfuscation to cipher key.

    Converts key to lowercase and applies character mapping.
    Only lowercase a-z are obfuscated; other characters pass through.

    Args:
        key: Original cipher key (must contain at least one a-z character)

    Returns:
        Obfuscated key

    Raises:
        ValueError: If obfuscated key equals input (no a-z chars to obfuscate)
    """
    key_lower = key.lower()
    o_key = "".join(chr(OBF_CHAR_MAP.get(ord(char), ord(char))) for char in key_lower)

    if o_key == key_lower:
        msg = f"Key '{key}' contains no a-z characters to obfuscate"
        raise ValueError(msg)

    return o_key
