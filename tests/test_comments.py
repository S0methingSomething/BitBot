"""Tests for the comments module."""

import json
from unittest.mock import MagicMock, mock_open, patch

from bitbot import comments


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
@patch("bitbot.utils.load_state")
def test_check_comments_no_update(
    mock_load_state: MagicMock, mock_reddit: MagicMock
) -> None:
    """Test the check_comments function when no update is needed."""
    mock_load_state.return_value = {
        "activePostId": "test_post",
        "lastCheckTimestamp": "2020-01-01T00:00:00Z",
        "currentIntervalSeconds": 0,
        "lastCommentCount": 0,
    }
    mock_submission = MagicMock()
    mock_submission.selftext = "Status: unknown"
    mock_submission.comments.list.return_value = []
    mock_reddit.return_value.submission.return_value = mock_submission

    read_data = {
        "feedback": {
            "statusLineRegex": r"^Status:.*",
            "workingKeywords": ["working"],
            "notWorkingKeywords": [],
            "labels": {
                "broken": "broken",
                "working": "working",
                "unknown": "unknown",
            },
            "statusLineFormat": "Status: {{status}}",
            "minFeedbackCount": 1,
        },
        "timing": {"firstCheck": 0, "maxWait": 0, "increaseBy": 0},
    }
    with patch(
        "builtins.open",
        mock_open(read_data=json.dumps(read_data)),
    ), patch("bitbot.utils.save_state"):
        comments.check_comments()

    mock_submission.edit.assert_not_called()


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
@patch("bitbot.utils.load_state")
def test_check_comments_positive_feedback(
    mock_load_state: MagicMock, mock_reddit: MagicMock
) -> None:
    """Test the check_comments function with positive feedback."""
    mock_load_state.return_value = {
        "activePostId": "test_post",
        "lastCheckTimestamp": "2020-01-01T00:00:00Z",
        "currentIntervalSeconds": 0,
        "lastCommentCount": 0,
    }
    mock_submission = MagicMock()
    mock_submission.selftext = "Status: unknown"
    mock_comment = MagicMock()
    mock_comment.body = "working"
    mock_submission.comments.list.return_value = [mock_comment]
    mock_reddit.return_value.submission.return_value = mock_submission

    read_data = {
        "feedback": {
            "statusLineRegex": r"^Status:.*",
            "workingKeywords": ["working"],
            "notWorkingKeywords": [],
            "labels": {
                "broken": "broken",
                "working": "working",
                "unknown": "unknown",
            },
            "statusLineFormat": "Status: {{status}}",
            "minFeedbackCount": 1,
        },
        "timing": {"firstCheck": 0, "maxWait": 0, "increaseBy": 0},
    }
    with patch(
        "builtins.open",
        mock_open(read_data=json.dumps(read_data)),
    ), patch("bitbot.utils.save_state"):
        comments.check_comments()

    mock_submission.edit.assert_called_once_with(body="Status: working")


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
@patch("bitbot.utils.load_state")
def test_check_comments_negative_feedback(
    mock_load_state: MagicMock, mock_reddit: MagicMock
) -> None:
    """Test the check_comments function with negative feedback."""
    mock_load_state.return_value = {
        "activePostId": "test_post",
        "lastCheckTimestamp": "2020-01-01T00:00:00Z",
        "currentIntervalSeconds": 0,
        "lastCommentCount": 0,
    }
    mock_submission = MagicMock()
    mock_submission.selftext = "Status: unknown"
    mock_comment = MagicMock()
    mock_comment.body = "broken"
    mock_submission.comments.list.return_value = [mock_comment]
    mock_reddit.return_value.submission.return_value = mock_submission

    read_data = {
        "feedback": {
            "statusLineRegex": r"^Status:.*",
            "workingKeywords": [],
            "notWorkingKeywords": ["broken"],
            "labels": {
                "broken": "broken",
                "working": "working",
                "unknown": "unknown",
            },
            "statusLineFormat": "Status: {{status}}",
            "minFeedbackCount": 1,
        },
        "timing": {"firstCheck": 0, "maxWait": 0, "increaseBy": 0},
    }
    with patch(
        "builtins.open",
        mock_open(read_data=json.dumps(read_data)),
    ), patch("bitbot.utils.save_state"):
        comments.check_comments()

    mock_submission.edit.assert_called_once_with(body="Status: broken")


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
@patch("bitbot.utils.load_state")
def test_check_comments_no_active_post(
    mock_load_state: MagicMock, mock_reddit: MagicMock
) -> None:
    """Test the check_comments function when there is no active post."""
    mock_load_state.return_value = {
        "activePostId": None,
        "lastCheckTimestamp": "2020-01-01T00:00:00Z",
        "currentIntervalSeconds": 0,
        "lastCommentCount": 0,
    }
    mock_submission = MagicMock()
    mock_submission.selftext = ""
    mock_reddit.return_value.submission.return_value = mock_submission
    with patch("sys.exit") as mock_exit:
        comments.check_comments()
        mock_exit.assert_called_once_with(0)
