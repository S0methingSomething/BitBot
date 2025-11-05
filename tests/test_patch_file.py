"""Tests for crypto module."""

import pytest

from bitbot.crypto.cipher import decrypt, encrypt
from bitbot.crypto.modifier import unlock_premium_features
from bitbot.crypto.obfuscation import get_obfuscated_key


def test_get_obfuscated_key():
    """Test key obfuscation."""
    result = get_obfuscated_key("test")
    assert len(result) == 4
    assert result != "test"


def test_get_obfuscated_key_no_alpha_raises():
    """Test key with no alpha chars raises error."""
    with pytest.raises(ValueError, match="no a-z characters"):
        get_obfuscated_key("12345")


def test_unlock_premium_features():
    """Test unlock_premium_features changes False to True."""
    data = {"feature1": False, "feature2": True, "feature3": "value"}
    result = unlock_premium_features(data)

    assert result["feature1"] is True
    assert result["feature2"] is True
    assert result["feature3"] == "value"
    # Original unchanged
    assert data["feature1"] is False


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


def test_decrypt_malformed_lines_raises():
    """Test decrypt raises on all malformed lines."""
    with pytest.raises(ValueError, match="All .* lines were malformed"):
        decrypt("invalid_no_colon", "testkey")


def test_encrypt_invalid_type_raises():
    """Test encrypt raises on invalid value types."""
    data = {"key": 123}  # int not allowed
    obf_key = get_obfuscated_key("testkey")

    with pytest.raises(TypeError, match="must be bool or str"):
        encrypt(data, obf_key)
