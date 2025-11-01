"""Tests for patch_file module."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from crypto.cipher import decrypt, encrypt
from crypto.encoding import b64_decode_and_xor, xor_and_b64_encode
from crypto.modifier import modify
from crypto.obfuscation import get_obfuscated_key


def test_get_obfuscated_key():
    """Test key obfuscation."""
    result = get_obfuscated_key("test")
    assert len(result) == 4
    assert result != "test"


def test_get_obfuscated_key_empty_raises():
    """Test empty key raises error."""
    with pytest.raises(Exception):
        get_obfuscated_key("")


def test_xor_and_b64_encode():
    """Test XOR encoding."""
    result = xor_and_b64_encode("hello", "key")
    assert len(result) > 0
    assert isinstance(result, str)


def test_b64_decode_and_xor():
    """Test XOR decoding."""
    encoded = xor_and_b64_encode("hello", "key")
    decoded = b64_decode_and_xor(encoded, "key")
    assert decoded == "hello"


def test_modify_sets_false_to_true():
    """Test modify changes false to true."""
    data = {"key1": True, "key2": False, "key3": "value"}
    result = modify(data)
    assert result["key1"] is True
    assert result["key2"] is True
    assert result["key3"] == "value"


def test_encrypt_decrypt_roundtrip():
    """Test encryption and decryption."""
    original = {"test": True, "value": "data"}
    obf_key = get_obfuscated_key("testkey")

    encrypted = encrypt(original, obf_key)
    assert isinstance(encrypted, str)
    assert len(encrypted) > 0

    decrypted = decrypt(encrypted, obf_key)
    assert decrypted["test"] is True
    assert decrypted["value"] == "data"
