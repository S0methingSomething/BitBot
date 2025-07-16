"""Tests for the history module."""

import json
from unittest.mock import MagicMock, mock_open, patch

from bitbot import history


@patch(
    "os.environ",
    {
        "GITHUB_TOKEN": "test",
        "REDDIT_CLIENT_ID": "test",
        "REDDIT_CLIENT_SECRET": "test",
        "REDDIT_USER_AGENT": "test",
        "REDDIT_USERNAME": "test",
        "REDDIT_PASSWORD": "test",
    },
)
@patch("requests.get")
@patch("praw.Reddit")
@patch("bitbot.history._get_latest_bot_release")
def test_sync_history_no_posts(
    mock_get_latest_bot_release: MagicMock,
    mock_reddit: MagicMock,
    mock_get: MagicMock,
) -> None:
    """Test the sync_history function when no posts exist."""
    mock_get_latest_bot_release.return_value = {
        "version": "1.0.0",
        "url": "test_url",
    }
    mock_submission = MagicMock()
    mock_submission.shortlink = "test_url"
    mock_submission.id = "test_id"
    mock_reddit.return_value.subreddit.return_value.submit.return_value = (
        mock_submission
    )
    mock_reddit.return_value.user.me.return_value.submissions.new.return_value = []

    read_data = {
        "github": {"assetFileName": "test.txt"},
        "reddit": {
            "templateFile": "test.md",
            "postTitle": "Test Post v{{version}}",
            "subreddit": "test",
        },
        "feedback": {
            "statusLineFormat": "Status: {{status}}",
            "labels": {"unknown": "unknown"},
        },
        "apps": [],
        "skipContent": {},
        "outdatedPostHandling": {},
    }
    with patch(
        "builtins.open",
        mock_open(read_data=json.dumps(read_data)),
    ):
        history.sync_history()

    mock_reddit.return_value.subreddit.return_value.submit.assert_called_once()


@patch(
    "os.environ",
    {
        "GITHUB_TOKEN": "test",
        "REDDIT_CLIENT_ID": "test",
        "REDDIT_CLIENT_SECRET": "test",
        "REDDIT_USER_AGENT": "test",
        "REDDIT_USERNAME": "test",
        "REDDIT_PASSWORD": "test",
    },
)
@patch("requests.get")
@patch("praw.Reddit")
@patch("bitbot.history._get_latest_bot_release")
def test_sync_history_up_to_date(
    mock_get_latest_bot_release: MagicMock,
    mock_reddit: MagicMock,
    mock_get: MagicMock,
) -> None:
    """Test the sync_history function when the latest post is up to date."""
    mock_get_latest_bot_release.return_value = {
        "version": "1.0.0",
        "url": "test_url",
    }
    mock_post = MagicMock()
    mock_post.title = "Test Post v1.0.0"
    mock_post.id = "test_id"
    mock_reddit.return_value.user.me.return_value.submissions.new.return_value = [
        mock_post
    ]

    read_data = {
        "github": {"assetFileName": "test.txt"},
        "reddit": {
            "postTitle": "Test Post v{{version}}",
            "subreddit": "test",
        },
    }
    with patch(
        "builtins.open",
        mock_open(read_data=json.dumps(read_data)),
    ):
        history.sync_history()

    mock_reddit.return_value.subreddit.return_value.submit.assert_not_called()
