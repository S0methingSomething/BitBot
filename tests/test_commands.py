"""Tests for BitBot CLI commands."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from returns.result import Failure, Success
from typer.testing import CliRunner

runner = CliRunner()


class TestPatchCommand:
    """Tests for patch command."""

    def test_patch_missing_input_file(self, tmp_path):
        """Test patch with missing input file."""
        from bitbot.commands.patch import app

        mock_container = MagicMock()
        mock_container.console.return_value = MagicMock()
        mock_container.logger.return_value = MagicMock()

        result = runner.invoke(
            app,
            [str(tmp_path / "nonexistent.txt"), str(tmp_path / "output.txt")],
            obj={"container": mock_container},
        )

        assert result.exit_code == 1

    def test_patch_input_is_directory(self, tmp_path):
        """Test patch with directory as input."""
        from bitbot.commands.patch import app

        input_dir = tmp_path / "inputdir"
        input_dir.mkdir()

        mock_container = MagicMock()
        mock_container.console.return_value = MagicMock()
        mock_container.logger.return_value = MagicMock()

        result = runner.invoke(
            app,
            [str(input_dir), str(tmp_path / "output.txt")],
            obj={"container": mock_container},
        )

        assert result.exit_code == 1

    def test_patch_success(self, tmp_path):
        """Test successful patch."""
        from bitbot.commands.patch import app

        input_file = tmp_path / "input.txt"
        input_file.write_text("test content")
        output_file = tmp_path / "output.txt"

        mock_container = MagicMock()
        mock_container.console.return_value = MagicMock()
        mock_container.logger.return_value = MagicMock()

        with patch("bitbot.commands.patch.process_file") as mock_process:
            mock_process.return_value = Success(None)

            result = runner.invoke(
                app,
                [str(input_file), str(output_file)],
                obj={"container": mock_container},
            )

        assert result.exit_code == 0

    def test_patch_process_failure(self, tmp_path):
        """Test patch with processing failure."""
        from bitbot.commands.patch import app

        input_file = tmp_path / "input.txt"
        input_file.write_text("test content")
        output_file = tmp_path / "output.txt"

        mock_container = MagicMock()
        mock_container.console.return_value = MagicMock()
        mock_container.logger.return_value = MagicMock()

        with patch("bitbot.commands.patch.process_file") as mock_process:
            mock_process.return_value = Failure("Processing error")

            result = runner.invoke(
                app,
                [str(input_file), str(output_file)],
                obj={"container": mock_container},
            )

        assert result.exit_code == 1


class TestPostCommandHelpers:
    """Tests for post command helper functions."""

    def test_build_changelog_data_added(self):
        """Test changelog detects added apps."""
        from bitbot.commands.post import _build_changelog_data

        releases_data = {
            "newapp": {
                "display_name": "New App",
                "latest_release": {"version": "1.0.0", "download_url": "http://example.com"},
                "previous_releases": [],
            }
        }
        online_versions: dict[str, str] = {}

        changelog = _build_changelog_data(releases_data, online_versions)

        assert "newapp" in changelog["added"]
        assert changelog["added"]["newapp"]["version"] == "1.0.0"

    def test_build_changelog_data_updated(self):
        """Test changelog detects updated apps."""
        from bitbot.commands.post import _build_changelog_data

        releases_data = {
            "app1": {
                "display_name": "App 1",
                "latest_release": {"version": "2.0.0", "download_url": "http://example.com"},
                "previous_releases": [],
            }
        }
        online_versions = {"app1": "1.0.0"}

        changelog = _build_changelog_data(releases_data, online_versions)

        assert "app1" in changelog["updated"]
        assert changelog["updated"]["app1"]["old"] == "1.0.0"
        assert changelog["updated"]["app1"]["new"]["version"] == "2.0.0"

    def test_build_changelog_data_removed(self):
        """Test changelog detects removed apps."""
        from bitbot.commands.post import _build_changelog_data

        releases_data: dict = {}
        online_versions = {"oldapp": "1.0.0"}

        changelog = _build_changelog_data(releases_data, online_versions)

        assert "oldapp" in changelog["removed"]

    def test_build_changelog_data_no_changes(self):
        """Test changelog with no changes."""
        from bitbot.commands.post import _build_changelog_data

        releases_data = {
            "app1": {
                "display_name": "App 1",
                "latest_release": {"version": "1.0.0", "download_url": "http://example.com"},
                "previous_releases": [],
            }
        }
        online_versions = {"app1": "1.0.0"}

        changelog = _build_changelog_data(releases_data, online_versions)

        assert len(changelog["added"]) == 0
        assert len(changelog["updated"]) == 0
        assert len(changelog["removed"]) == 0
