"""Tests for the crypto module."""

from pathlib import Path
from unittest import TestCase

from bitbot.crypto import get_file_sha256


class TestCrypto(TestCase):
    """Tests for the crypto module."""

    def test_get_file_sha256(self) -> None:
        """Test the get_file_sha256 function."""
        # Create a dummy file
        file_path = Path("test.txt")
        with file_path.open("w") as f:
            f.write("test")

        # Calculate the hash
        file_hash = get_file_sha256(file_path)

        # Check the hash
        self.assertEqual(
            file_hash,
            "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
        )

        # Clean up the dummy file
        file_path.unlink()
