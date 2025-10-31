"""XOR encoding/decoding for BitBot crypto."""

import base64

import deal
from beartype import beartype


@deal.pre(lambda text, key: len(key) > 0)  # type: ignore[misc]
@deal.post(lambda result: len(result) > 0)  # type: ignore[misc]
@beartype  # type: ignore[misc]
def xor_and_b64_encode(text: str, key: str) -> str:
    """Performs an XOR operation and then Base64 encodes the result."""
    key_bytes = key.encode("latin-1")
    text_bytes = text.encode("latin-1")
    xor_result = bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(text_bytes)])
    return base64.b64encode(xor_result).decode("utf-8")


@deal.pre(lambda b64, key: len(b64) > 0)  # type: ignore[misc]
@deal.pre(lambda b64, key: len(key) > 0)  # type: ignore[misc]
@deal.post(lambda result: len(result) >= 0)  # type: ignore[misc]
@beartype  # type: ignore[misc]
def b64_decode_and_xor(b64: str, key: str) -> str:
    """Decodes a Base64 string and then performs an XOR operation."""
    key_bytes = key.encode("latin-1")
    decoded_bytes = base64.b64decode(b64)
    xor_result = bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(decoded_bytes)])
    return xor_result.decode("latin-1")
