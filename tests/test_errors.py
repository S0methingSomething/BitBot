"""Tests for the errors module."""

from unittest import TestCase

from bitbot import errors


class TestErrors(TestCase):
    """Tests for the errors module."""

    def test_bitbot_error(self) -> None:
        """Test the BitBotError exception."""
        with self.assertRaises(errors.BitBotError):
            raise errors.BitBotError

    def test_github_error(self) -> None:
        """Test the GitHubError exception."""
        with self.assertRaises(errors.GitHubError):
            raise errors.GitHubError

    def test_reddit_error(self) -> None:
        """Test the RedditError exception."""
        with self.assertRaises(errors.RedditError):
            raise errors.RedditError
