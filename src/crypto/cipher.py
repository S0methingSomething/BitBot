"""Encryption/decryption for BitBot crypto."""

import deal
from beartype import beartype

from crypto.constants import B64_NET_BOOLEAN_FALSE, B64_NET_BOOLEAN_TRUE
from crypto.encoding import b64_decode_and_xor, xor_and_b64_encode


@deal.pre(lambda encrypted_content, obfuscated_key: len(encrypted_content) > 0)  # type: ignore[misc]
@deal.pre(lambda encrypted_content, obfuscated_key: len(obfuscated_key) > 0)  # type: ignore[misc]
@deal.post(lambda result: isinstance(result, dict))  # type: ignore[misc]
@beartype  # type: ignore[misc]
def decrypt(encrypted_content: str, obfuscated_key: str) -> dict[str, str | bool]:
    """Decrypts the content of the asset file into a Python dictionary."""
    item_map: dict[str, str | bool] = {}
    for line in encrypted_content.splitlines():
        if not line.strip():
            continue
        parts = line.split(":", 1)
        if len(parts) != 2:
            continue
        enc_key, enc_val = parts
        dec_key = b64_decode_and_xor(enc_key.strip(), obfuscated_key)
        dec_val_b64 = b64_decode_and_xor(enc_val.strip(), obfuscated_key)

        if dec_val_b64 == B64_NET_BOOLEAN_TRUE:
            item_map[dec_key] = True
        elif dec_val_b64 == B64_NET_BOOLEAN_FALSE:
            item_map[dec_key] = False
        else:
            item_map[dec_key] = dec_val_b64
    return item_map


@deal.pre(lambda data_object, obfuscated_key: isinstance(data_object, dict))  # type: ignore[misc]
@deal.pre(lambda data_object, obfuscated_key: len(obfuscated_key) > 0)  # type: ignore[misc]
@deal.post(lambda result: len(result) > 0)  # type: ignore[misc]
@beartype  # type: ignore[misc]
def encrypt(data_object: dict[str, str | bool], obfuscated_key: str) -> str:
    """Re-encrypts the modified data object back into the file format."""
    output_lines = []
    for key, value in data_object.items():
        encrypted_key = xor_and_b64_encode(key, obfuscated_key)

        if value is True:
            value_to_serialize = B64_NET_BOOLEAN_TRUE
        elif value is False:
            value_to_serialize = B64_NET_BOOLEAN_FALSE
        else:
            value_to_serialize = value

        encrypted_value = xor_and_b64_encode(value_to_serialize, obfuscated_key)
        output_lines.append(f"{encrypted_key}:{encrypted_value}")
    return "\n".join(output_lines)
