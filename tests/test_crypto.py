"""Tests for BitBot crypto module."""

import pytest

from bitbot.crypto.cipher import decrypt, encrypt
from bitbot.crypto.modifier import unlock_premium_features
from bitbot.crypto.obfuscation import get_obfuscated_key


class TestObfuscation:
    """Tests for key obfuscation."""

    def test_obfuscation_changes_key(self):
        """Test that obfuscation produces different output."""
        key = "TestKey123"
        obfuscated = get_obfuscated_key(key)
        assert obfuscated != key

    def test_obfuscation_deterministic(self):
        """Test that same input produces same output."""
        key = "TestKey123"
        assert get_obfuscated_key(key) == get_obfuscated_key(key)

    def test_obfuscation_no_alpha_raises(self):
        """Test that key without letters raises error."""
        with pytest.raises(ValueError, match="no a-z characters"):
            get_obfuscated_key("12345")


class TestModifier:
    """Tests for premium feature unlocking."""

    def test_unlock_premium_features(self):
        """Test unlocking sets all False to True."""
        data = {"premium": False, "ads": True, "feature": False}
        result = unlock_premium_features(data)
        assert result["premium"] is True
        assert result["ads"] is True
        assert result["feature"] is True

    def test_unlock_preserves_non_bool(self):
        """Test non-boolean values are preserved."""
        data = {"name": "test", "count": "5", "enabled": False}
        result = unlock_premium_features(data)
        assert result["name"] == "test"
        assert result["count"] == "5"
        assert result["enabled"] is True


class TestCipher:
    """Tests for encryption/decryption."""

    def test_encrypt_decrypt_roundtrip_bools(self):
        """Test boolean data survives encrypt/decrypt cycle."""
        data = {"premium": True, "ads": False, "feature": True}
        key = "TestKey123"
        obfuscated = get_obfuscated_key(key)

        encrypted = encrypt(data, obfuscated)
        decrypted = decrypt(encrypted, obfuscated)

        assert decrypted == data

    def test_encrypt_decrypt_roundtrip_strings(self):
        """Test string data survives encrypt/decrypt cycle."""
        data = {"name": "test", "value": "hello"}
        key = "TestKey123"
        obfuscated = get_obfuscated_key(key)

        encrypted = encrypt(data, obfuscated)
        decrypted = decrypt(encrypted, obfuscated)

        assert decrypted == data

    def test_decrypt_malformed_raises(self):
        """Test malformed encrypted content raises error."""
        key = "TestKey123"
        obfuscated = get_obfuscated_key(key)

        with pytest.raises(ValueError, match="malformed"):
            decrypt("not:valid:encrypted:content", obfuscated)

    def test_encrypt_nested_dict_raises(self):
        """Test nested dicts raise TypeError."""
        data = {"outer": {"inner": "value"}}
        key = "TestKey123"
        obfuscated = get_obfuscated_key(key)

        with pytest.raises(TypeError, match="must be bool or str"):
            encrypt(data, obfuscated)

    def test_encrypt_int_value_raises(self):
        """Test integer values raise TypeError."""
        data = {"count": 5}
        key = "TestKey123"
        obfuscated = get_obfuscated_key(key)

        with pytest.raises(TypeError, match="must be bool or str"):
            encrypt(data, obfuscated)
