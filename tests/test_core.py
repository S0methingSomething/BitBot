from pathlib import Path

from bitbot.core import patch_monetization_vars

# Define the paths to your test data files
TEST_DATA_DIR = Path(__file__).parent / "data"
ORIGINAL_VARS_PATH = TEST_DATA_DIR / "original_vars.txt"
PATCHED_VARS_PATH = TEST_DATA_DIR / "patched_vars.txt"


def test_patch_monetization_vars():
    """
    Tests that the core patching logic correctly transforms the
    MonetizationVars file.
    """
    # 1. Read the input and expected output from your data files
    original_content = ORIGINAL_VARS_PATH.read_text().strip()
    expected_patched_content = PATCHED_VARS_PATH.read_text().strip()

    # 2. Run the function that you want to test
    actual_patched_content = patch_monetization_vars(original_content)

    # 3. Assert that the result is what you expect
    # We compare line by line for easier debugging if it fails
    assert actual_patched_content.splitlines() == expected_patched_content.splitlines()
