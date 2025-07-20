"""Tests for the debug module."""

from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from bitbot.debug import pretty_print_json


class TestDebug(TestCase):
    """Tests for the debug module."""

    @patch("sys.stdout", new_callable=StringIO)
    def test_pretty_print_json(self, mock_stdout: StringIO) -> None:
        """Test the pretty_print_json function."""
        data = {"a": 1, "b": 2}
        pretty_print_json(data)
        self.assertEqual(mock_stdout.getvalue(), '{\n  "a": 1,\n  "b": 2\n}\n')
