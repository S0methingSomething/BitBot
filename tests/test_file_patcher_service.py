"""Tests for the FilePatcherService."""

from hypothesis import given
from hypothesis import strategies as st

from src.bitbot.services.file_patcher_service import FilePatcherService

# A strategy for generating valid Base64 strings for the keys and values
b64_string = st.text(alphabet="abcdefghijklmnopqrstuvwxyz0123456789+/=", min_size=1)

# A strategy for generating the dictionary that represents the decrypted file
data_object_strategy = st.dictionaries(
    keys=b64_string,
    values=st.booleans() | b64_string,
    min_size=1,
)


@given(data=data_object_strategy)
def test_file_patcher_preserves_data_and_sets_false_to_true(data: dict[str, bool | str]) -> None:
    """
    Tests that the patcher correctly sets False to True while preserving all other data.
    This is a property-based test that will run many times with different inputs.
    """
    patcher = FilePatcherService()

    # Create the "original" file content by encrypting the generated data
    obfuscated_key = patcher._get_obfuscated_key(patcher._DEFAULT_CIPHER_KEY)
    original_content = patcher._encrypt(data, obfuscated_key)

    # Run the patcher on the original content
    patched_content = patcher.patch_file_content(original_content)

    # Decrypt the patched content to verify its integrity
    result_data = patcher._decrypt(patched_content, obfuscated_key)

    # Assertions
    assert len(result_data) == len(data), "The number of items should not change."

    for key, original_value in data.items():
        assert key in result_data, f"Key '{key}' should be present in the result."
        new_value = result_data[key]

        if original_value is False:
            assert new_value is True, "False should be converted to True."
        else:
            assert new_value == original_value, "Other values should be preserved."
