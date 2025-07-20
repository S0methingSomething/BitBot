"""Tests for the comments module."""

import asyncio
from unittest.mock import MagicMock

from bitbot import comments

from .base import BaseTestCase


class TestComments(BaseTestCase):
    """Tests for the comments module."""

    def test_check_comments_no_update(self) -> None:
        """Test the check_comments function when no update is needed."""
        self.mock_state_manager.load_state.return_value.lastCommentCount = 0
        mock_post = MagicMock()
        mock_post.id = "initial_post"
        mock_post.body = "Status: unknown"
        self.mock_reddit_manager.get_post_by_id.return_value = mock_post
        self.mock_reddit_manager.get_comments.return_value = []

        asyncio.run(
            comments.check_comments(
                config_manager=self.mock_config_manager,
                state_manager=self.mock_state_manager,
                reddit_manager=self.mock_reddit_manager,
            )
        )

        self.mock_reddit_manager.update_post_body.assert_not_called()

    def test_check_comments_positive_feedback(self) -> None:
        """Test the check_comments function with positive feedback."""
        self.mock_state_manager.load_state.return_value.lastCommentCount = 0
        mock_post = MagicMock()
        mock_post.id = "initial_post"
        mock_post.body = "Status: initial"
        self.mock_reddit_manager.get_post_by_id.return_value = mock_post
        mock_comment = MagicMock()
        mock_comment.body = "working"
        self.mock_reddit_manager.get_comments.return_value = [
            mock_comment,
            mock_comment,
        ]

        asyncio.run(
            comments.check_comments(
                config_manager=self.mock_config_manager,
                state_manager=self.mock_state_manager,
                reddit_manager=self.mock_reddit_manager,
            )
        )

        self.mock_reddit_manager.update_post_body.assert_called_once_with(
            "initial_post", "Status: working"
        )

    def test_check_comments_negative_feedback(self) -> None:
        """Test the check_comments function with negative feedback."""
        self.mock_state_manager.load_state.return_value.lastCommentCount = 0
        mock_post = MagicMock()
        mock_post.id = "initial_post"
        mock_post.body = "Status: initial"
        self.mock_reddit_manager.get_post_by_id.return_value = mock_post
        mock_comment = MagicMock()
        mock_comment.body = "broken"
        self.mock_reddit_manager.get_comments.return_value = [
            mock_comment,
            mock_comment,
        ]

        asyncio.run(
            comments.check_comments(
                config_manager=self.mock_config_manager,
                state_manager=self.mock_state_manager,
                reddit_manager=self.mock_reddit_manager,
            )
        )

        self.mock_reddit_manager.update_post_body.assert_called_once_with(
            "initial_post", "Status: broken"
        )

    def test_check_comments_no_active_post(self) -> None:
        """Test the check_comments function when there is no active post."""
        self.mock_state_manager.load_state.return_value.activePostId = None

        result = asyncio.run(
            comments.check_comments(
                config_manager=self.mock_config_manager,
                state_manager=self.mock_state_manager,
                reddit_manager=self.mock_reddit_manager,
            )
        )
        self.assertFalse(result)
