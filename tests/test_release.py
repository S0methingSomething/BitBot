"""Tests for the release module."""

import asyncio

from bitbot import release

from .base import BaseTestCase


class TestRelease(BaseTestCase):
    """Tests for the release module."""

    def test_check_new_release(self) -> None:
        """Test the check_new_release function."""
        self.mock_github_manager.get_latest_release.return_value.version = "1.0.0"
        self.mock_state_manager.load_state.return_value.activePostId = "test_id"
        self.mock_reddit_manager.get_post_by_id.return_value.title = "Test Post v0.9.0"

        asyncio.run(
            release.check_new_release(
                config_manager=self.mock_config_manager,
                state_manager=self.mock_state_manager,
                github_manager=self.mock_github_manager,
                reddit_manager=self.mock_reddit_manager,
            )
        )

        self.mock_reddit_manager.submit_post.assert_called_once()
