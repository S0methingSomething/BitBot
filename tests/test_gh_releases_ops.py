"""Tests for GitHub releases operations (patcher)."""

from pathlib import Path
from unittest.mock import patch

import pytest
from returns.result import Failure, Success

from bitbot.gh.releases.patcher import patch_file


class TestPatcher:
    """Tests for file patching."""

    def test_patch_file_success(self, tmp_path):
        """Test successful file patching."""
        original = tmp_path / "original.txt"
        original.write_text("test content")

        with patch("bitbot.gh.releases.patcher.process_file") as mock_process:
            mock_process.return_value = Success(None)
            with patch("bitbot.gh.releases.patcher.DOWNLOAD_DIR", str(tmp_path)):
                result = patch_file(str(original), "patched.txt")

        assert isinstance(result, Success)
        assert "patched.txt" in result.unwrap()

    def test_patch_file_failure(self, tmp_path):
        """Test patching failure."""
        original = tmp_path / "original.txt"
        original.write_text("test content")

        with patch("bitbot.gh.releases.patcher.process_file") as mock_process:
            mock_process.return_value = Failure("Processing error")
            with patch("bitbot.gh.releases.patcher.DOWNLOAD_DIR", str(tmp_path)):
                result = patch_file(str(original), "patched.txt")

        assert isinstance(result, Failure)
        assert "Failed to patch" in str(result.failure())

    def test_patch_file_empty_path_rejected(self):
        """Test empty original path is rejected."""
        with pytest.raises(Exception):  # icontract violation
            patch_file("", "output.txt")

    def test_patch_file_empty_asset_rejected(self, tmp_path):
        """Test empty asset name is rejected."""
        original = tmp_path / "original.txt"
        original.write_text("test")
        with pytest.raises(Exception):  # icontract violation
            patch_file(str(original), "")
