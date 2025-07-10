import base64
import logging
import sys
from typing import Any, Union


def get_logger(name: str) -> logging.Logger:
    """Initializes and returns a logger."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


logger = get_logger(__name__)


DEFAULT_CIPHER_KEY = "com.wtfapps.apollo16"
B64_NET_BOOLEAN_TRUE = (
    "AAEAAAD/////AQAAAAAAAAAEAQAAAA5TeXN0ZW0uQm9vbGVhbgEAAAAHbV92YWx1ZQABAQs="
)
B64_NET_BOOLEAN_FALSE = (
    "AAEAAAD/////AQAAAAAAAAAEAQAAAA5TeXN0ZW0uQm9vbGVhbgEAAAAHbV92YWx1ZQABAAw="
)
OBF_CHAR_MAP = {
    0x61: 0x7A,
    0x62: 0x6D,
    0x63: 0x79,
    0x64: 0x6C,
    0x65: 0x78,
    0x66: 0x6B,
    0x67: 0x77,
    0x68: 0x6A,
    0x69: 0x76,
    0x6A: 0x69,
    0x6B: 0x75,
    0x6C: 0x68,
    0x6D: 0x74,
    0x6E: 0x67,
    0x6F: 0x73,
    0x70: 0x66,
    0x71: 0x72,
    0x72: 0x65,
    0x73: 0x71,
    0x74: 0x64,
    0x75: 0x70,
    0x76: 0x63,
    0x77: 0x6F,
    0x78: 0x62,
    0x79: 0x6E,
    0x7A: 0x61,
}


def get_obfuscated_key(key: str) -> str:
    o_key = ""
    for char in key.lower():
        code = ord(char)
        o_key += chr(OBF_CHAR_MAP.get(code, code))
    return o_key


def xor_and_b64_encode(text: str, key: str) -> str:
    xor_result = "".join(
        chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(text)
    )
    return base64.b64encode(xor_result.encode("latin1")).decode("utf-8")


def b64_decode_and_xor(b64: str, key: str) -> str:
    decoded = base64.b64decode(b64).decode("latin1")
    return "".join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(decoded))


def decrypt(encrypted_content: str, obfuscated_key: str) -> dict[str, Union[bool, str]]:
    item_map: dict[str, Union[bool, str]] = {}
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


def modify(data_object: dict[str, Any]) -> dict[str, Any]:
    logger.info("Modifying data: Setting all boolean 'false' values to 'true'.")
    for key, value in data_object.items():
        if value is False:
            data_object[key] = True
    return data_object


def encrypt(data_object: dict[str, Any], obfuscated_key: str) -> str:
    logger.info("Re-encrypting data...")
    output_content = []
    for key, value in data_object.items():
        encrypted_key = xor_and_b64_encode(key, obfuscated_key)

        if value is True:
            value_to_serialize = B64_NET_BOOLEAN_TRUE
        elif value is False:
            value_to_serialize = B64_NET_BOOLEAN_FALSE
        else:
            value_to_serialize = value

        encrypted_value = xor_and_b64_encode(str(value_to_serialize), obfuscated_key)
        output_content.append(f"{encrypted_key}:{encrypted_value}")

    return "\n".join(output_content)


def main() -> None:
    if len(sys.argv) != 3:
        logger.error(
            f"Usage: python {sys.argv[0]} <input-file> <output-file>",
        )
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    logger.info(f"Processing file: {input_file}")
    obfuscated_key = get_obfuscated_key(DEFAULT_CIPHER_KEY)

    with open(input_file, "r", encoding="utf-8") as f:
        encrypted_content = f.read()

    decrypted_data = decrypt(encrypted_content, obfuscated_key)
    modified_data = modify(decrypted_data)
    re_encrypted_content = encrypt(modified_data, obfuscated_key)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(re_encrypted_content)

    logger.info(f"Successfully processed and saved patched file to: {output_file}")


if __name__ == "__main__":
    main()
