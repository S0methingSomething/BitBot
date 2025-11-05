"""Tests for crypto operations."""

import pytest

from bitbot.crypto.cipher import decrypt, encrypt
from bitbot.crypto.modifier import unlock_premium_features
from bitbot.crypto.obfuscation import get_obfuscated_key


def test_obfuscation():
    """Test key obfuscation transforms key."""
    key = "testkey"
    obfuscated = get_obfuscated_key(key)
    
    assert obfuscated != key
    assert len(obfuscated) == len(key)


def test_obfuscation_no_alpha_raises():
    """Test obfuscation raises on non-alpha keys."""
    with pytest.raises(ValueError, match="no a-z characters"):
        get_obfuscated_key("12345")


def test_unlock_premium_features():
    """Test unlock_premium_features changes False to True."""
    data = {
        "feature1": False,
        "feature2": True,
        "feature3": "value",
    }
    
    result = unlock_premium_features(data)
    
    assert result["feature1"] is True
    assert result["feature2"] is True
    assert result["feature3"] == "value"
    # Original unchanged
    assert data["feature1"] is False


def test_decrypt_malformed_lines_raises():
    """Test decrypt raises on all malformed lines."""
    with pytest.raises(ValueError, match="All .* lines were malformed"):
        decrypt("invalid_no_colon", "testkey")


def test_encrypt_decrypt_roundtrip():
    """Test encrypt/decrypt roundtrip preserves data."""
    original = {
        "key1": "value1",
        "key2": True,
        "key3": False,
    }
    obf_key = get_obfuscated_key("testkey")
    
    encrypted = encrypt(original, obf_key)
    decrypted = decrypt(encrypted, obf_key)
    
    assert decrypted == original


def test_encrypt_invalid_type_raises():
    """Test encrypt raises on invalid value types."""
    data = {"key": 123}  # int not allowed
    obf_key = get_obfuscated_key("testkey")
    
    with pytest.raises(TypeError, match="must be bool or str"):
        encrypt(data, obf_key)
