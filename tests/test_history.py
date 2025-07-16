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
@patch("bitbot.utils.save_state")
@patch("requests.get")
@patch("praw.Reddit")
@patch("bitbot.history._get_latest_bot_release")
def test_sync_history_no_posts(
    mock_get_latest_bot_release: MagicMock,
    mock_reddit: MagicMock,
    mock_get: MagicMock,
    mock_save_state: MagicMock,
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
            "creator": "test_creator",
            "botName": "test_bot",
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
@patch("bitbot.utils.save_state")
@patch("requests.get")
@patch("praw.Reddit")
@patch("bitbot.history._get_latest_bot_release")
def test_sync_history_up_to_date(
    mock_get_latest_bot_release: MagicMock,
    mock_reddit: MagicMock,
    mock_get: MagicMock,
    mock_save_state: MagicMock,
) -> None:
    """Test the sync_history function when the latest post is up to date."""
    mock_get_latest_bot_release.return_value = {
        "version": "1.0.0",
        "url": "test_url",
    }
    mock_post = MagicMock()
    mock_post.title = "Test Post v1.0.0"
    mock_post.id = "test_id"
    mock_submission = MagicMock()
    mock_reddit.return_value.user.me.return_value.submissions.new.return_value = [
        mock_post
    ]
    mock_reddit.return_value.subreddit.return_value.submit.return_value = (
        mock_submission
    )
    read_data = {
        "github": {"botRepo": "test/repo", "assetFileName": "test.txt"},
        "reddit": {
            "postTitle": "Test Post v{{version}}",
            "subreddit": "test",
            "botName": "test_bot",
            "creator": "test_creator",
        },
        "outdatedPostHandling": {
            "mode": "inject",
            "injectTemplateFile": "test.md",
        },
        "skipContent": {},
        "timing": {},
    }
    with patch(
        "builtins.open",
        mock_open(read_data=json.dumps(read_data)),
    ), patch("bitbot.utils.load_state", return_value={"activePostId": "test_id"}):
        history.sync_history()

    mock_reddit.return_value.subreddit.return_value.submit.assert_not_called()


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
@patch("bitbot.utils.save_state")
@patch("requests.get")
@patch("praw.Reddit")
@patch("bitbot.history._get_latest_bot_release")
def test_sync_history_with_older_posts(
    mock_get_latest_bot_release: MagicMock,
    mock_reddit: MagicMock,
    mock_get: MagicMock,
    mock_save_state: MagicMock,
) -> None:
    """Test the sync_history function with older posts to update."""
    mock_get_latest_bot_release.return_value = {
        "version": "2.0.0",
        "url": "test_url",
    }
    mock_post_1 = MagicMock()
    mock_post_1.title = "Test Post v1.0.0"
    mock_post_1.id = "test_id_1"
    mock_post_1.selftext = "some text"
    mock_post_2 = MagicMock()
    mock_post_2.title = "Test Post v0.9.0"
    mock_post_2.id = "test_id_2"
    mock_post_2.selftext = "some other text"
    mock_submission = MagicMock()
    mock_submission.id = "new_id"
    mock_submission.title = "Test Post v2.0.0"
    mock_submission.shortlink = "new_url"
    mock_reddit.return_value.user.me.return_value.submissions.new.return_value = [
        mock_post_1,
        mock_post_2,
    ]
    mock_reddit.return_value.subreddit.return_value.submit.return_value = (
        mock_submission
    )
    read_data = {
        "github": {"botRepo": "test/repo", "assetFileName": "test.txt"},
        "reddit": {
            "templateFile": "test.md",
            "postTitle": "Test Post v{{version}}",
            "subreddit": "test",
            "botName": "test_bot",
            "creator": "test_creator",
        },
        "feedback": {
            "statusLineFormat": "Status: {{status}}",
            "labels": {"unknown": "unknown"},
        },
        "apps": [],
        "skipContent": {},
        "outdatedPostHandling": {
            "mode": "inject",
            "injectTemplateFile": "test.md",
        },
        "timing": {"firstCheck": 300},
    }
    with patch(
        "builtins.open",
        mock_open(read_data=json.dumps(read_data)),
    ), patch("bitbot.utils.load_state", return_value={"activePostId": "test_id_1"}):
        history.sync_history()

    assert mock_post_1.edit.called
    assert mock_post_2.edit.called
    mock_reddit.return_value.subreddit.return_value.submit.assert_called_once()
    mock_save_state.assert_called_with(
        {
            "activePostId": "new_id",
            "lastCheckTimestamp": "2024-01-01T00:00:00Z",
            "currentIntervalSeconds": 300,
            "lastCommentCount": 0,
        }
    )