# tests/test_api_clients.py
"""
Tests for the ApiClientService.
"""
import pytest
from pathlib import Path
import tomlkit
from unittest.mock import AsyncMock

from bitbot.core import ApplicationCore
from bitbot.services.api_clients import ApiClientService
from bitbot.domain.models import GitHubRelease, RedditPost

# Mark all tests in this file as asyncio
pytestmark = pytest.mark.asyncio


@pytest.fixture
def mock_config(tmp_path: Path) -> Path:
    """Creates a dummy config.toml and features.toml file for tests."""
    # Create config.toml
    config_content = {
        "github": {
            "source_repo": "test/source",
            "bot_repo": "test/bot",
            "asset_file_name": "TestAsset",
        },
        "reddit": {
            "subreddit": "testsub",
            "post_style": "landing_page",
            "max_outbound_links_warning": 5,
            "post_title_template": "Test Post",
            "creator_username": "testuser",
        },
        "apps": [{"id": "testapp", "display_name": "Test App"}],
    }
    config_path = tmp_path / "config.toml"
    config_path.write_text(tomlkit.dumps(config_content))

    # Create features.toml
    features_content = {
        "feature": {
            "release_management": {"enabled": True},
            "reddit_poster": {"enabled": True},
        }
    }
    features_path = tmp_path / "features.toml"
    features_path.write_text(tomlkit.dumps(features_content))

    return tmp_path


async def test_get_latest_releases_success(tmp_path: Path, mock_config: Path, mocker):
    """
    Tests that the GitHubClient can successfully fetch and parse releases
    when the broker grants permission and the API call is successful.
    """
    # Arrange
    import os
    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    core = ApplicationCore()
    api_clients = ApiClientService(core)

    # Mock the httpx response
    mock_api_response = [
        {
            "tag_name": "v1.0.0",
            "html_url": "https://github.com/test/source/releases/tag/v1.0.0",
            "body": "Release v1.0.0",
        }
    ]
    
    # Patch the broker's network call to return our mock response
    mocker.patch(
        "bitbot.core.ExecutionBroker.request_network_call",
        return_value=mock_api_response
    )

    # Act
    releases = await api_clients.github.get_latest_releases()

    # Assert
    assert len(releases) == 1
    assert releases[0].tag_name == "v1.0.0"
    assert "Release v1.0.0" in releases[0].body
    
    # Verify the broker was called correctly
    core.broker.request_network_call.assert_called_once_with(
        requester=api_clients.github,
        method="GET",
        url="https://api.github.com/repos/test/source/releases?per_page=30",
    )

    os.chdir(original_cwd)

async def test_create_release_success(tmp_path: Path, mock_config: Path, mocker):
    """
    Tests that the GitHubClient can successfully create a release.
    """
    # Arrange
    import os
    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    core = ApplicationCore()
    api_clients = ApiClientService(core)

    release_to_create = GitHubRelease(
        tag_name="v1.1.0",
        html_url="http://example.com", # This will be replaced by the API response
        body="This is the new release body."
    )

    mock_api_response = {
        "tag_name": "v1.1.0",
        "html_url": "https://github.com/test/bot/releases/tag/v1.1.0",
        "body": "This is the new release body.",
    }

    mocker.patch(
        "bitbot.core.ExecutionBroker.request_network_call",
        return_value=mock_api_response
    )

    # Act
    created_release = await api_clients.github.create_release(release_to_create)

    # Assert
    assert created_release.tag_name == "v1.1.0"
    assert str(created_release.html_url) == "https://github.com/test/bot/releases/tag/v1.1.0"
    
    core.broker.request_network_call.assert_called_once_with(
        requester=api_clients.github,
        method="POST",
        url="https://api.github.com/repos/test/bot/releases",
        json=release_to_create.model_dump(include={"tag_name", "body"}),
    )

    os.chdir(original_cwd)

async def test_submit_post_success(tmp_path: Path, mock_config: Path, mocker):
    """
    Tests that the RedditClient can successfully submit a post.
    """
    # Arrange
    import os
    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    core = ApplicationCore()
    api_clients = ApiClientService(core)

    post_to_submit = RedditPost(
        title="Test Post",
        selftext="This is a test post.",
    )

    mock_api_response = {
        "id": "t3_12345",
    }

    mocker.patch(
        "bitbot.core.ExecutionBroker.request_network_call",
        return_value=mock_api_response
    )

    # Act
    submitted_post = await api_clients.reddit.submit_post(post_to_submit)

    # Assert
    assert submitted_post.id == "t3_12345"
    
    core.broker.request_network_call.assert_called_once_with(
        requester=api_clients.reddit,
        method="POST",
        url="https://oauth.reddit.com/r/testsub/submit",
        json=post_to_submit.model_dump(include={"title", "selftext", "url"}),
    )

    os.chdir(original_cwd)
