"""Tests for the crypto module."""

from typing import Dict, Union

from bitbot import crypto


def test_get_obfuscated_key() -> None:
    """Test the get_obfuscated_key function."""
    assert crypto.get_obfuscated_key("abc") == "zmy"
    assert crypto.get_obfuscated_key("xyz") == "bna"
    assert crypto.get_obfuscated_key("123") == "123"
    assert crypto.get_obfuscated_key("") == ""
    assert crypto.get_obfuscated_key("!@#$") == "!@#$"


def test_xor_and_b64_encode() -> None:
    """Test the xor_and_b64_encode function."""
    assert crypto.xor_and_b64_encode("hello", "key") == "AwAVBwo="
    assert crypto.xor_and_b64_encode("", "key") == ""
    assert crypto.xor_and_b64_encode("hello", "") == ""


def test_b64_decode_and_xor() -> None:
    """Test the b64_decode_and_xor function."""
    assert crypto.b64_decode_and_xor("AwAVBwo=", "key") == "hello"
    assert crypto.b64_decode_and_xor("", "key") == ""
    assert crypto.b64_decode_and_xor("aGVsbG8=", "") == ""


def test_encrypt_decrypt() -> None:
    """Test the encrypt and decrypt functions."""
    data: Dict[str, Union[bool, str]] = {"key1": "value1", "key2": True, "key3": False}
    obfuscated_key = crypto.get_obfuscated_key(crypto.DEFAULT_CIPHER_KEY)
    encrypted_data = crypto.encrypt(data, obfuscated_key)
    decrypted_data = crypto.decrypt(encrypted_data, obfuscated_key)
    assert decrypted_data == data


def test_encrypt_decrypt_empty() -> None:
    """Test the encrypt and decrypt functions with empty data."""
    data: Dict[str, Union[bool, str]] = {}
    obfuscated_key = crypto.get_obfuscated_key(crypto.DEFAULT_CIPHER_KEY)
    encrypted_data = crypto.encrypt(data, obfuscated_key)
    decrypted_data = crypto.decrypt(encrypted_data, obfuscated_key)
    assert decrypted_data == data
