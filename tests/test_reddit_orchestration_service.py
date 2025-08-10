"""Tests for the RedditOrchestrationService.

The tests are structured to reflect the service's architecture, which separates
the decision-making logic from the action-taking (dispatcher) logic.
"""

from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock

import pytest

from src.bitbot.models.changelog import Changelog, ChangelogEntry
from src.bitbot.models.post_action import CreatePost, UpdatePost
from src.bitbot.models.state import BotState
from src.bitbot.services.reddit_orchestration_service import RedditOrchestrationService


@pytest.fixture
def mock_services(mocker):
    """Fixture to create mocked services for initializing the service."""
    return {
        "logging_service": mocker.MagicMock(),
        "state_service": mocker.MagicMock(),
        "reddit_service": mocker.MagicMock(),
        "reddit_post_service": mocker.MagicMock(),
    }


# --- Tests for the Decision-Making Logic (_determine_action) ---


def test_determine_action_returns_create_when_no_active_post(mock_services):
    """
    Given: The bot state has no active_post_id.
    When: _determine_action is called.
    Then: It should return a CreatePost action.
    """
    # Arrange
    service = RedditOrchestrationService(**mock_services)
    state = BotState(active_post_id=None, last_major_post_timestamp=datetime.now(timezone.utc))

    # Act
    action = service._determine_action(state)

    # Assert
    assert isinstance(action, CreatePost)


def test_determine_action_returns_create_when_no_timestamp(mock_services):
    """
    Given: The bot state has no last_major_post_timestamp.
    When: _determine_action is called.
    Then: It should return a CreatePost action.
    """
    # Arrange
    service = RedditOrchestrationService(**mock_services)
    state = BotState(active_post_id="some_id", last_major_post_timestamp=None)

    # Act
    action = service._determine_action(state)

    # Assert
    assert isinstance(action, CreatePost)


def test_determine_action_returns_create_when_post_is_old(mock_services):
    """
    Given: The active post is older than the TTL.
    When: _determine_action is called.
    Then: It should return a CreatePost action.
    """
    # Arrange
    service = RedditOrchestrationService(**mock_services)
    eight_days_ago = datetime.now(timezone.utc) - timedelta(days=8)
    state = BotState(active_post_id="old_post", last_major_post_timestamp=eight_days_ago)

    # Act
    action = service._determine_action(state)

    # Assert
    assert isinstance(action, CreatePost)


def test_determine_action_returns_update_when_post_is_recent(mock_services):
    """
    Given: The active post is recent.
    When: manage_reddit_post is called.
    Then: The existing post should be updated.
    """
    # Arrange
    six_days_ago = datetime.now(timezone.utc) - timedelta(days=6)
    state = BotState(active_post_id="recent_post", last_major_post_timestamp=six_days_ago)
    
    mock_services["state_service"].load_bot_state.return_value = state
    mock_services["reddit_post_service"].generate_post.return_value = MagicMock()
    
    service = RedditOrchestrationService(**mock_services)
    changelog = Changelog(added=[ChangelogEntry(app_id="test", version="1.0", asset_name="test.zip")])

    # Act
    service.manage_reddit_post(changelog)

    # Assert
    mock_services["reddit_service"].update_post.assert_called_once()
    mock_services["state_service"].save_bot_state.assert_not_called()


# --- Tests for the Dispatcher Logic (manage_reddit_post) ---


def test_dispatcher_does_nothing_for_empty_changelog(mock_services, mocker):
    """
    Given: The changelog is empty.
    When: manage_reddit_post is called.
    Then: No action should be determined or executed.
    """
    # Arrange
    service = RedditOrchestrationService(**mock_services)
    changelog = Changelog()  # Empty changelog
    determine_action_mock = mocker.patch.object(service, "_determine_action")

    # Act
    service.manage_reddit_post(changelog)

    # Assert
    determine_action_mock.assert_not_called()
    mock_services["reddit_service"].create_post.assert_not_called()
    mock_services["reddit_service"].update_post.assert_not_called()


def test_dispatcher_executes_create_post_action(mock_services, mocker):
    """
    Given: The decision is to create a post.
    When: manage_reddit_post is called.
    Then: It should generate a post, create it, and save the new state.
    """
    # Arrange
    service = RedditOrchestrationService(**mock_services)
    changelog = Changelog(added=[ChangelogEntry(app_id="test", version="1.0", asset_name="test.zip")])
    mocker.patch.object(service, "_determine_action", return_value=CreatePost())
    mock_services["reddit_service"].create_post.return_value = "new_post_id"

    # Act
    service.manage_reddit_post(changelog)

    # Assert
    mock_services["reddit_post_service"].generate_post.assert_called_once_with(changelog)
    mock_services["reddit_service"].create_post.assert_called_once()
    mock_services["state_service"].save_bot_state.assert_called_once()
    saved_state = mock_services["state_service"].save_bot_state.call_args[0][0]
    assert saved_state.active_post_id == "new_post_id"


def test_dispatcher_executes_update_post_action(mock_services, mocker):
    """
    Given: The decision is to update a post.
    When: manage_reddit_post is called.
    Then: It should generate a post and update the existing one.
    """
    # Arrange
    service = RedditOrchestrationService(**mock_services)
    changelog = Changelog(updated=[ChangelogEntry(app_id="test", version="1.1", asset_name="test.zip")])
    mock_post_object = MagicMock()
    mock_services["reddit_post_service"].generate_post.return_value = mock_post_object
    mocker.patch.object(service, "_determine_action", return_value=UpdatePost(post_id="existing_post_id"))

    # Act
    service.manage_reddit_post(changelog)

    # Assert
    mock_services["reddit_post_service"].generate_post.assert_called_once_with(changelog)
    mock_services["reddit_service"].update_post.assert_called_once_with("existing_post_id", mock_post_object)
    mock_services["state_service"].save_bot_state.assert_not_called()
