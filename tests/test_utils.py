"""Tests for the utils module."""

from unittest import TestCase
from unittest.mock import mock_open, patch

from bitbot import utils


class TestUtils(TestCase):
    """Tests for the utils module."""

    def test_load_config(self) -> None:
        """Test the load_config function."""
        with patch("builtins.open", mock_open(read_data="test = 1")):
            config = utils.load_config()
        self.assertEqual(config, {"test": 1})

    def test_load_state(self) -> None:
        """Test the load_state function."""
        with patch("builtins.open", mock_open(read_data='{"test": 1}')):
            state = utils.load_state()
        self.assertEqual(state, {"test": 1})

    def test_save_state(self) -> None:
        """Test the save_state function."""
        mock_file = mock_open()
        with patch("builtins.open", mock_file):
            utils.save_state({"test": 1})
        mock_file.assert_called_once_with("data/bot_state.json", "w")
        mock_file().write.assert_called_once_with('{\n  "test": 1\n}')
