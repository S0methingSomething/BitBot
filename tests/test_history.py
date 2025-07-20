"""Tests for the history module."""

import asyncio
from unittest.mock import MagicMock

from bitbot import history

from .base import BaseTestCase


class TestHistory(BaseTestCase):
    """Tests for the history module."""

    def setUp(self) -> None:
        """Sets up the test case."""
        super().setUp()

    def test_sync_history_no_posts(self) -> None:
        """Test the sync_history function when no posts exist."""
        self.mock_github_manager.get_latest_release.return_value.version = "1.0.0"
        self.mock_reddit_manager.get_recent_bot_posts.return_value = []
        self.mock_reddit_manager.submit_post.return_value.id = "new_post_id"

        asyncio.run(
            history.sync_history(
                config_manager=self.mock_config_manager,
                state_manager=self.mock_state_manager,
                github_manager=self.mock_github_manager,
                reddit_manager=self.mock_reddit_manager,
                template_manager=self.mock_template_manager,
            )
        )

        self.mock_reddit_manager.submit_post.assert_called_once()

    def test_sync_history_up_to_date(self) -> None:
        """Test the sync_history function when the latest post is up to date."""
        self.mock_github_manager.get_latest_release.return_value.version = "1.0.0"
        mock_post = MagicMock()
        mock_post.title = "Test Post v1.0.0"
        mock_post.id = "test_id"
        self.mock_reddit_manager.get_recent_bot_posts.return_value = [mock_post]

        asyncio.run(
            history.sync_history(
                config_manager=self.mock_config_manager,
                state_manager=self.mock_state_manager,
                github_manager=self.mock_github_manager,
                reddit_manager=self.mock_reddit_manager,
                template_manager=self.mock_template_manager,
            )
        )

        self.mock_reddit_manager.submit_post.assert_not_called()

    def test_sync_history_with_older_posts(self) -> None:
        """Test the sync_history function with older posts to update."""
        self.mock_github_manager.get_latest_release.return_value.version = "2.0.0"
        mock_post_1 = MagicMock()
        mock_post_1.title = "Test Post v1.0.0"
        mock_post_1.id = "test_id_1"
        mock_post_1.body = "some text"
        mock_post_2 = MagicMock()
        mock_post_2.title = "Test Post v0.9.0"
        mock_post_2.id = "test_id_2"
        mock_post_2.body = "some other text"
        self.mock_reddit_manager.get_recent_bot_posts.return_value = [
            mock_post_1,
            mock_post_2,
        ]
        self.mock_reddit_manager.submit_post.return_value.id = "new_post_id"
        self.mock_reddit_manager.submit_post.return_value.url = "new_post_url"
        self.mock_reddit_manager.submit_post.return_value.title = "New Post Title"

        asyncio.run(
            history.sync_history(
                config_manager=self.mock_config_manager,
                state_manager=self.mock_state_manager,
                github_manager=self.mock_github_manager,
                reddit_manager=self.mock_reddit_manager,
                template_manager=self.mock_template_manager,
            )
        )

        self.mock_reddit_manager.update_post_body.assert_any_call(
            "test_id_1",
            "# Injected Banner\n\nLatest version: 2.0.0\n\n\n---\n\nsome text",
        )
        self.mock_reddit_manager.update_post_body.assert_any_call(
            "test_id_2",
            "# Injected Banner\n\nLatest version: 2.0.0\n\n\n---\n\nsome other text",
        )
        self.mock_reddit_manager.submit_post.assert_called_once()
