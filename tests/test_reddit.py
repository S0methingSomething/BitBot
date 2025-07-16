"""Tests for the reddit module."""

import json
from unittest.mock import MagicMock, mock_open, patch

from bitbot import reddit


@patch(
    "os.environ",
    {
        "REDDIT_CLIENT_ID": "test",
        "REDDIT_CLIENT_SECRET": "test",
        "REDDIT_USER_AGENT": "test",
        "REDDIT_USERNAME": "test",
        "REDDIT_PASSWORD": "test",
    },
)
@patch("praw.Reddit")
def test_post_new_release(mock_reddit: MagicMock) -> None:
    """Test the post_new_release function."""
    mock_reddit.return_value.user.me.return_value.submissions.new.return_value = []
    mock_submission = MagicMock()
    mock_submission.shortlink = "test_url"
    mock_submission.id = "test_id"
    mock_reddit.return_value.subreddit.return_value.submit.return_value = (
        mock_submission
    )

    read_data = {
        "reddit": {
            "templateFile": "test.md",
            "postTitle": "Test Post v{{version}}",
            "subreddit": "test",
        },
        "github": {"assetFileName": "test.txt"},
        "feedback": {
            "statusLineFormat": "Status: {{status}}",
            "labels": {"unknown": "unknown"},
        },
        "apps": [{"id": "bitlife"}, {"id": "bitlife_go"}],
        "skipContent": {},
        "outdatedPostHandling": {},
    }
    with patch(
        "builtins.open",
        mock_open(read_data=json.dumps(read_data)),
    ):
        reddit.post_new_release(
            "1.0.0", '{"bitlife": "test_url", "bitlife_go": "test_url"}'
        )

    mock_reddit.return_value.subreddit.return_value.submit.assert_called_once()


@patch("bitbot.reddit._get_bot_posts_on_subreddit")
@patch(
    "os.environ",
    {
        "REDDIT_CLIENT_ID": "test",
        "REDDIT_CLIENT_SECRET": "test",
        "REDDIT_USER_AGENT": "test",
        "REDDIT_USERNAME": "test",
        "REDDIT_PASSWORD": "test",
    },
)
@patch("praw.Reddit")
def test_post_new_release_with_older_posts(
    mock_reddit: MagicMock, mock_get_bot_posts_on_subreddit: MagicMock
) -> None:
    """Test the post_new_release function when older posts exist."""
    mock_get_bot_posts_on_subreddit.return_value = [MagicMock()]
    mock_old_post = MagicMock()
    mock_reddit.return_value.user.me.return_value.submissions.new.return_value = [
        mock_old_post
    ]
    mock_submission = MagicMock()
    mock_submission.shortlink = "test_url"
    mock_submission.id = "test_id"
    mock_reddit.return_value.subreddit.return_value.submit.return_value = (
        mock_submission
    )

    read_data = {
        "reddit": {
            "templateFile": "test.md",
            "postTitle": "Test Post v{{version}}",
            "subreddit": "test",
        },
        "github": {"assetFileName": "test.txt"},
        "feedback": {
            "statusLineFormat": "Status: {{status}}",
            "labels": {"unknown": "unknown"},
        },
        "apps": [{"id": "bitlife"}, {"id": "bitlife_go"}],
        "skipContent": {},
        "outdatedPostHandling": {
            "mode": "inject",
            "injectTemplateFile": "inject.md",
        },
    }
    with patch(
        "builtins.open",
        mock_open(read_data=json.dumps(read_data)),
    ), patch("bitbot.reddit._update_older_posts") as mock_update_older_posts:
        reddit.post_new_release(
            "1.0.0", '{"bitlife": "test_url", "bitlife_go": "test_url"}'
        )

    mock_update_older_posts.assert_called_once()
