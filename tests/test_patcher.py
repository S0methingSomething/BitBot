# tests/test_patcher.py
"""
Tests for the PatcherService.
"""

import pytest
from bitbot.services.patcher import PatcherService

@pytest.fixture
def patcher() -> PatcherService:
    return PatcherService()

def test_patcher_e2e(patcher: PatcherService):
    """
    Tests the full decrypt-modify-encrypt cycle.
    """
    # This is the Base64 representation of a simple key-value file
    # with one boolean `false` value.
    # Original data:
    # my_feature: false
    # another_setting: some_value
    
    # The key and value are XORed with the obfuscated key and then Base64 encoded.
    # The line format is `B64(XOR(key)):B64(XOR(B64(value)))`
    
    # Let's create the encrypted content manually to test the patcher
    obfuscated_key = patcher._get_obfuscated_key(patcher.DEFAULT_CIPHER_KEY)
    
    original_data = {
        "my_feature": False,
        "another_setting": "some_value"
    }
    
    encrypted_content = patcher.encrypt(original_data, obfuscated_key)
    
    # Now, patch the content
    patched_content = patcher.patch_file_content(encrypted_content)
    
    # Decrypt the patched content to verify the change
    decrypted_patched_data = patcher.decrypt(patched_content, obfuscated_key)
    
    # Assert that the boolean `false` was changed to `true`
    assert decrypted_patched_data["my_feature"] is True
    # Assert that other values remain unchanged
    assert decrypted_patched_data["another_setting"] == "some_value"

def test_obfuscated_key(patcher: PatcherService):
    """
    Tests the key obfuscation logic.
    """
    key = "com.wtfapps.apollo16"
    expected = "yst.odkzffq.zfshhs16"
    assert patcher._get_obfuscated_key(key) == expected
