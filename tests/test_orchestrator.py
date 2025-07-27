# tests/test_orchestrator.py
"""
Tests for the OrchestrationService.
"""

import pytest
from pathlib import Path
import tomlkit
from unittest.mock import AsyncMock, MagicMock

from bitbot.core import ApplicationCore
from bitbot.services.orchestrator import OrchestrationService
from bitbot.services.api_clients import ApiClientService
from bitbot.services.workspace import WorkspaceService
from bitbot.services.patcher import PatcherService
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
            "post_title_template": "New Release: {version}",
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

@pytest.fixture
def mock_core(mock_config: Path) -> ApplicationCore:
    """Provides a mocked ApplicationCore."""
    import os
    original_cwd = os.getcwd()
    os.chdir(mock_config)
    core = ApplicationCore()
    os.chdir(original_cwd)
    return core

@pytest.fixture
def mock_api_clients(mocker) -> ApiClientService:
    """Provides a mocked ApiClientService."""
    mock = MagicMock(spec=ApiClientService)
    mock.github = MagicMock()
    mock.reddit = MagicMock()
    mock.github.get_latest_releases = AsyncMock()
    mock.github.create_release = AsyncMock()
    mock.reddit.submit_post = AsyncMock()
    return mock

@pytest.fixture
def mock_workspace(mocker) -> WorkspaceService:
    """Provides a mocked WorkspaceService."""
    mock = MagicMock(spec=WorkspaceService)
    mock.get_state = AsyncMock()
    mock.save_state = AsyncMock()
    return mock

@pytest.fixture
def mock_patcher(mocker) -> PatcherService:
    """Provides a mocked PatcherService."""
    mock = MagicMock(spec=PatcherService)
    mock.patch_file_content = MagicMock(return_value="patched content")
    return mock


async def test_manage_releases_new_release_found(
    mock_core: ApplicationCore,
    mock_api_clients: ApiClientService,
    mock_workspace: WorkspaceService,
    mock_patcher: PatcherService,
):
    """
    Tests the full orchestration workflow when a new release is found.
    """
    # Arrange
    orchestrator = OrchestrationService(mock_core, mock_api_clients, mock_workspace, mock_patcher)

    # Mock data
    source_releases = [
        GitHubRelease(tag_name="v1.1.0", html_url="http://example.com/v1.1.0", body="Release v1.1.0"),
        GitHubRelease(tag_name="v1.0.0", html_url="http://example.com/v1.0.0", body="Release v1.0.0"),
    ]
    created_release = GitHubRelease(tag_name="v1.1.0", html_url="http://bot.com/v1.1.0", body="patched content")
    submitted_post = RedditPost(id="t3_12345", title="New Release: v1.1.0", selftext="...")

    # Mock service calls
    mock_api_clients.github.get_latest_releases.return_value = source_releases
    mock_workspace.get_state.return_value = {"last_known_release_tag": "v1.0.0"}
    mock_api_clients.github.create_release.return_value = created_release
    mock_api_clients.reddit.submit_post.return_value = submitted_post

    # Act
    await orchestrator.manage_releases()

    # Assert
    mock_api_clients.github.get_latest_releases.assert_called_once()
    mock_workspace.get_state.assert_called_once()
    mock_patcher.patch_file_content.assert_called_once_with("Release v1.1.0")
    mock_api_clients.github.create_release.assert_called_once()
    mock_api_clients.reddit.submit_post.assert_called_once()
    mock_workspace.save_state.assert_called_once_with({"last_known_release_tag": "v1.1.0"})

async def test_manage_releases_no_new_release(
    mock_core: ApplicationCore,
    mock_api_clients: ApiClientService,
    mock_workspace: WorkspaceService,
    mock_patcher: PatcherService,
):
    """
    Tests that the workflow exits early when no new release is found.
    """
    # Arrange
    orchestrator = OrchestrationService(mock_core, mock_api_clients, mock_workspace, mock_patcher)
    source_releases = [GitHubRelease(tag_name="v1.0.0", html_url="http://example.com/v1.0.0", body="...")]
    mock_api_clients.github.get_latest_releases.return_value = source_releases
    mock_workspace.get_state.return_value = {"last_known_release_tag": "v1.0.0"}

    # Act
    await orchestrator.manage_releases()

    # Assert
    mock_api_clients.github.get_latest_releases.assert_called_once()
    mock_workspace.get_state.assert_called_once()
    mock_patcher.patch_file_content.assert_not_called()
    mock_api_clients.github.create_release.assert_not_called()
    mock_api_clients.reddit.submit_post.assert_not_called()
    mock_workspace.save_state.assert_not_called()

async def test_manage_releases_no_prior_state(
    mock_core: ApplicationCore,
    mock_api_clients: ApiClientService,
    mock_workspace: WorkspaceService,
    mock_patcher: PatcherService,
):
    """
    Tests that the workflow correctly processes only the latest release
    when no prior state is found.
    """
    # Arrange
    orchestrator = OrchestrationService(mock_core, mock_api_clients, mock_workspace, mock_patcher)
    source_releases = [
        GitHubRelease(tag_name="v1.1.0", html_url="http://example.com/v1.1.0", body="..."),
        GitHubRelease(tag_name="v1.0.0", html_url="http://example.com/v1.0.0", body="..."),
    ]
    created_release = GitHubRelease(tag_name="v1.1.0", html_url="http://bot.com/v1.1.0", body="patched content")
    submitted_post = RedditPost(id="t3_12345", title="New Release: v1.1.0", selftext="...")

    mock_api_clients.github.get_latest_releases.return_value = source_releases
    mock_workspace.get_state.side_effect = FileNotFoundError
    mock_api_clients.github.create_release.return_value = created_release
    mock_api_clients.reddit.submit_post.return_value = submitted_post

    # Act
    await orchestrator.manage_releases()

    # Assert
    mock_patcher.patch_file_content.assert_called_once_with("...")
    mock_api_clients.github.create_release.assert_called_once()
    # Ensure it was called with the *latest* release
    call_args = mock_api_clients.github.create_release.call_args[0][0]
    assert call_args.tag_name == "v1.1.0"
    assert call_args.body == "patched content"
    mock_workspace.save_state.assert_called_once_with({"last_known_release_tag": "v1.1.0"})