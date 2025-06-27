from pathlib import Path

import pytest

from bitbot.core import patch_monetization_vars

# Define the path to the test data directory
DATA_DIR = Path(__file__).parent / "data"


@pytest.fixture
def original_vars_content() -> str:
    """Fixture to load the original MonetizationVars content from a file."""
    return (DATA_DIR / "original_vars.txt").read_text().strip()


@pytest.fixture
def patched_vars_content() -> str:
    """Fixture to load the expected patched MonetizationVars content from a file."""
    return (DATA_DIR / "patched_vars.txt").read_text().strip()


def test_full_transformation(original_vars_content, patched_vars_content):
    """
    Validates that processing the original file content exactly matches the
    expected patched content.
    """
    result = patch_monetization_vars(original_vars_content)
    assert result == patched_vars_content


def test_idempotency(patched_vars_content):
    """
    Tests that running the patcher on already-patched data results in no changes.
    """
    result = patch_monetization_vars(patched_vars_content)
    assert result == patched_vars_content


def test_malformed_input_handling():
    """
    Tests that garbage input does not cause crashes and is handled gracefully.
    """
    malformed_content = (
        "this is not valid content\n"
        "another line without a colon\n"
        "invalid:base64:string\n"
        "\n" # Empty line
    )
    # The function should process valid lines and ignore invalid ones.
    # In this case, no lines are valid, so it should return an empty string.
    result = patch_monetization_vars(malformed_content)
    assert result == ""
