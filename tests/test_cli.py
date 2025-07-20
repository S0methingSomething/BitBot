"""Tests for the cli module."""

from unittest.mock import MagicMock, patch

from bitbot import cli

from .base import BaseTestCase


class TestCli(BaseTestCase):
    """Tests for the cli module."""

    @patch("sys.argv", ["bitbot", "sync"])
    @patch("bitbot.cli.sync_history")
    def test_main_sync(self, mock_sync_history: MagicMock) -> None:
        """Test the main function with the sync command."""
        cli.main()
        mock_sync_history.assert_called_once()

    @patch("sys.argv", ["bitbot", "pulse"])
    @patch("bitbot.cli.check_comments")
    def test_main_pulse(self, mock_check_comments: MagicMock) -> None:
        """Test the main function with the pulse command."""
        cli.main()
        mock_check_comments.assert_called_once()

    @patch("sys.argv", ["bitbot"])
    @patch("argparse.ArgumentParser.print_help")
    def test_main_no_command(self, mock_print_help: MagicMock) -> None:
        """Test the main function with no command."""
        cli.main()
        mock_print_help.assert_called_once()
