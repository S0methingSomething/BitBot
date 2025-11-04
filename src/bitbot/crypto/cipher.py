"""Encryption and decryption for game asset file patching.

This module handles the decrypt → modify → re-encrypt workflow for game
configuration files to unlock premium features.
"""

import base64
import binascii
import logging
from typing import Any

import deal
from beartype import beartype

from .constants import B64_NET_BOOLEAN_FALSE, B64_NET_BOOLEAN_TRUE

logger = logging.getLogger(__name__)


@beartype
def _xor_and_b64_encode(text: str, key: str) -> str:
    """Perform XOR operation and Base64 encode the result."""
    key_bytes = key.encode("latin-1")
    text_bytes = text.encode("latin-1")
    xor_result = bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(text_bytes)])
    return base64.b64encode(xor_result).decode("utf-8")


@beartype
def _b64_decode_and_xor(b64: str, key: str) -> str | None:
    """Decode Base64 string and perform XOR operation.

    Returns None if decoding fails.
    """
    try:
        key_bytes = key.encode("latin-1")
        decoded_bytes = base64.b64decode(b64)
        xor_result = bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(decoded_bytes)])
        return xor_result.decode("latin-1")
    except (binascii.Error, UnicodeDecodeError) as e:
        logger.warning("Failed to decode/XOR: %s", e)
        return None


@deal.pre(lambda encrypted_content, _obfuscated_key: len(encrypted_content) > 0)
@deal.pre(lambda _encrypted_content, obfuscated_key: len(obfuscated_key) > 0)
@deal.post(lambda result: isinstance(result, dict) and len(result) > 0)
@beartype
def decrypt(encrypted_content: str, obfuscated_key: str) -> dict[str, Any]:
    """Decrypt game asset file content into dictionary.

    Raises:
        ValueError: If all lines are malformed and result would be empty.
    """
    item_map: dict[str, Any] = {}
    skipped_lines = 0

    for line_num, line in enumerate(encrypted_content.splitlines(), 1):
        if not line.strip():
            continue

        parts = line.split(":", 1)
        if len(parts) != 2:
            logger.warning("Line %d: Invalid format (missing colon)", line_num)
            skipped_lines += 1
            continue

        enc_key, enc_val = parts
        dec_key = _b64_decode_and_xor(enc_key.strip(), obfuscated_key)
        if dec_key is None:
            logger.warning("Line %d: Failed to decrypt key", line_num)
            skipped_lines += 1
            continue

        dec_val_b64 = _b64_decode_and_xor(enc_val.strip(), obfuscated_key)
        if dec_val_b64 is None:
            logger.warning("Line %d: Failed to decrypt value", line_num)
            skipped_lines += 1
            continue

        if dec_val_b64 == B64_NET_BOOLEAN_TRUE:
            item_map[dec_key] = True
        elif dec_val_b64 == B64_NET_BOOLEAN_FALSE:
            item_map[dec_key] = False
        else:
            item_map[dec_key] = dec_val_b64

    if not item_map:
        msg = f"All {skipped_lines} lines were malformed - cannot decrypt file"
        raise ValueError(msg)

    if skipped_lines > 0:
        logger.info(
            "Successfully decrypted %d items, skipped %d malformed lines",
            len(item_map),
            skipped_lines,
        )

    return item_map


@deal.pre(lambda data_object, _obfuscated_key: len(data_object) > 0)
@deal.pre(lambda _data_object, obfuscated_key: len(obfuscated_key) > 0)
@deal.post(lambda result: len(result) > 0)
@beartype
def encrypt(data_object: dict[str, Any], obfuscated_key: str) -> str:
    """Re-encrypt modified data object back into game asset file format.

    Raises:
        TypeError: If data_object contains non-serializable values.
    """
    output_lines = []
    for key, value in data_object.items():
        # Validate key is string
        if not isinstance(key, str):
            msg = f"Key must be string, got {type(key)}"
            raise TypeError(msg)

        encrypted_key = _xor_and_b64_encode(key, obfuscated_key)

        # Handle boolean values
        if value is True:
            value_to_serialize = B64_NET_BOOLEAN_TRUE
        elif value is False:
            value_to_serialize = B64_NET_BOOLEAN_FALSE
        elif isinstance(value, str):
            value_to_serialize = value
        else:
            msg = f"Value for key '{key}' must be bool or str, got {type(value)}"
            raise TypeError(msg)

        encrypted_value = _xor_and_b64_encode(value_to_serialize, obfuscated_key)
        output_lines.append(f"{encrypted_key}:{encrypted_value}")
    return "\n".join(output_lines)
