"""Encryption and decryption for BitBot file patching."""

import base64
from typing import Any

import deal
from beartype import beartype

from .constants import B64_NET_BOOLEAN_FALSE, B64_NET_BOOLEAN_TRUE


@beartype
def _xor_and_b64_encode(text: str, key: str) -> str:
    """Perform XOR operation and Base64 encode the result."""
    key_bytes = key.encode("latin-1")
    text_bytes = text.encode("latin-1")
    xor_result = bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(text_bytes)])
    return base64.b64encode(xor_result).decode("utf-8")


@beartype
def _b64_decode_and_xor(b64: str, key: str) -> str:
    """Decode Base64 string and perform XOR operation."""
    key_bytes = key.encode("latin-1")
    decoded_bytes = base64.b64decode(b64)
    xor_result = bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(decoded_bytes)])
    return xor_result.decode("latin-1")


@deal.pre(lambda encrypted_content, _obfuscated_key: len(encrypted_content) > 0)
@deal.pre(lambda _encrypted_content, obfuscated_key: len(obfuscated_key) > 0)
@deal.post(lambda result: isinstance(result, dict))
@beartype
def decrypt(encrypted_content: str, obfuscated_key: str) -> dict[str, Any]:
    """Decrypt asset file content into dictionary."""
    item_map: dict[str, Any] = {}
    for line in encrypted_content.splitlines():
        if not line.strip():
            continue
        parts = line.split(":", 1)
        if len(parts) != 2:
            continue
        enc_key, enc_val = parts
        dec_key = _b64_decode_and_xor(enc_key.strip(), obfuscated_key)
        dec_val_b64 = _b64_decode_and_xor(enc_val.strip(), obfuscated_key)

        if dec_val_b64 == B64_NET_BOOLEAN_TRUE:
            item_map[dec_key] = True
        elif dec_val_b64 == B64_NET_BOOLEAN_FALSE:
            item_map[dec_key] = False
        else:
            item_map[dec_key] = dec_val_b64
    return item_map


@deal.pre(lambda data_object, _obfuscated_key: len(data_object) > 0)
@deal.pre(lambda _data_object, obfuscated_key: len(obfuscated_key) > 0)
@deal.post(lambda result: len(result) > 0)
@beartype
def encrypt(data_object: dict[str, Any], obfuscated_key: str) -> str:
    """Re-encrypt modified data object back into file format."""
    output_lines = []
    for key, value in data_object.items():
        encrypted_key = _xor_and_b64_encode(key, obfuscated_key)

        if value is True:
            value_to_serialize = B64_NET_BOOLEAN_TRUE
        elif value is False:
            value_to_serialize = B64_NET_BOOLEAN_FALSE
        else:
            value_to_serialize = value

        encrypted_value = _xor_and_b64_encode(value_to_serialize, obfuscated_key)
        output_lines.append(f"{encrypted_key}:{encrypted_value}")
    return "\n".join(output_lines)
