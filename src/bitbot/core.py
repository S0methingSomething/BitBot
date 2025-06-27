import base64
import binascii  # <-- FIX: Import binascii to handle its specific error

_B64_NET_BOOLEAN_TRUE = (
    "AAEAAAD/////AQAAAAAAAAAEAQAAAA5TeXN0ZW0uQm9vbGVhbgEAAAAHbV92YWx1ZQABAQs="
)
_B64_NET_BOOLEAN_FALSE = (
    "AAEAAAD/////AQAAAAAAAAAEAQAAAA5TeXN0ZW0uQm9vbGVhbgEAAAAHbV92YWx1ZQABAAw="
)
_OBF_CHAR_MAP = {
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
_CIPHER_KEY = "com.wtfapps.apollo16"


def _get_obfuscated_key(key: str) -> str:
    """Applies the known character substitution to the key."""
    return "".join(chr(_OBF_CHAR_MAP.get(ord(char), ord(char))) for char in key.lower())


def _xor_and_b64_encode(text: str, key: str) -> str:
    """Performs a repeating-key XOR and then Base64 encodes the result."""
    xored_bytes = bytes(
        [ord(text[i]) ^ ord(key[i % len(key)]) for i in range(len(text))]
    )
    return base64.b64encode(xored_bytes).decode("ascii")


def _b64_decode_and_xor(b64_text: str, key: str) -> str:
    """Decodes a Base64 string and then performs a repeating-key XOR."""
    decoded_bytes = base64.b64decode(b64_text)
    return "".join(
        chr(decoded_bytes[i] ^ ord(key[i % len(key)]))
        for i in range(len(decoded_bytes))
    )


def patch_monetization_vars(content: str) -> str:
    """
    Reads the raw, obfuscated content of a MonetizationVars file,
    sets all boolean 'false' values to 'true', and returns the re-obfuscated content.
    """
    obfuscated_key = _get_obfuscated_key(_CIPHER_KEY)
    lines = []

    for line in content.strip().split("\n"):
        line = line.strip()  # <-- FIX: Remove whitespace that causes test failures
        if ":" not in line:
            continue
        try:
            enc_key, enc_val = line.split(":", 1)
            dec_key = _b64_decode_and_xor(enc_key, obfuscated_key)
            dec_val_b64 = _b64_decode_and_xor(enc_val, obfuscated_key)

            if dec_val_b64 == _B64_NET_BOOLEAN_FALSE:
                dec_val_b64 = _B64_NET_BOOLEAN_TRUE

            lines.append((dec_key, dec_val_b64))
        # <-- FIX: Catch the correct exception type -->
        except (ValueError, IndexError, binascii.Error):
            continue

    output_lines = []
    for dec_key, dec_val_b64 in lines:
        enc_key = _xor_and_b64_encode(dec_key, obfuscated_key)
        enc_val = _xor_and_b64_encode(dec_val_b64, obfuscated_key)
        output_lines.append(f"{enc_key}:{enc_val}")

    return "\n".join(output_lines)
