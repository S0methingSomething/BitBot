# tests/test_workspace.py
"""
Tests for the WorkspaceService.
"""

from pathlib import Path

import pytest
import tomlkit
from bitbot.core import ApplicationCore
from bitbot.services.workspace import WorkspaceService

# Mark all tests in this file as asyncio
pytestmark = pytest.mark.asyncio


class UnauthorizedService:
    """A fake service that should not have file-reading permissions."""

    pass


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


async def test_get_template_success(tmp_path: Path, mock_config: Path):
    """
    Tests that the WorkspaceService can successfully read a template file
    when the broker grants permission.
    """
    # Arrange
    # We need to temporarily change the working directory so the broker finds the file
    import os

    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    core = ApplicationCore()
    workspace = WorkspaceService(core)

    # Create a fake template file
    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    template_file = template_dir / "test_template.md"
    template_file.write_text("Hello, {{name}}!")

    # Act
    content = await workspace.get_template("test_template.md")

    # Revert CWD
    os.chdir(original_cwd)

    # Assert
    assert content == "Hello, {{name}}!"


async def test_get_template_permission_denied(tmp_path: Path, mock_config: Path):
    """
    Tests that the broker correctly denies a file-read request from an
    unauthorized service.
    """
    # Arrange
    import os

    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    core = ApplicationCore()
    unauthorized_service = UnauthorizedService()

    # Act & Assert
    with pytest.raises(PermissionError) as exc_info:
        # We are directly calling the broker to simulate an unauthorized request
        await core.broker.request_file_read(
            requester=unauthorized_service, path="templates/any.md"
        )

    os.chdir(original_cwd)
    assert "Permission denied" in str(exc_info.value)


async def test_get_template_file_not_found(tmp_path: Path, mock_config: Path):
    """
    Tests that the service correctly raises FileNotFoundError for a missing file.
    """
    # Arrange
    import os

    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    core = ApplicationCore()
    workspace = WorkspaceService(core)

    # Act & Assert
    with pytest.raises(FileNotFoundError):
        await workspace.get_template("non_existent_template.md")

    os.chdir(original_cwd)


async def test_save_state_success(tmp_path: Path, mock_config: Path):
    """
    Tests that the WorkspaceService can successfully write the state file.
    """
    # Arrange
    import os
    import json

    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    core = ApplicationCore()
    workspace = WorkspaceService(core)
    state_data = {"activePostId": "12345", "lastCommentCount": 10}
    state_file_path = tmp_path / "bot_state.json"

    # Act
    await workspace.save_state(state_data)

    # Assert
    assert state_file_path.exists()
    saved_data = json.loads(state_file_path.read_text())
    assert saved_data["activePostId"] == "12345"
    assert saved_data["lastCommentCount"] == 10

    os.chdir(original_cwd)


async def test_save_state_permission_denied_wrong_path(
    tmp_path: Path, mock_config: Path
):
    """
    Tests that the broker denies WorkspaceService from writing to a forbidden path.
    """
    # Arrange
    import os

    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    core = ApplicationCore()
    workspace = WorkspaceService(core)

    # Act & Assert
    with pytest.raises(PermissionError):
        # We directly call the broker to simulate the service trying to be malicious
        await core.broker.request_file_write(
            requester=workspace, path="config.toml", content="{}"
        )

    os.chdir(original_cwd)


async def test_save_state_permission_denied_unauthorized_service(
    tmp_path: Path, mock_config: Path
):
    """
    Tests that the broker denies an unauthorized service from writing ANY file.
    """
    # Arrange
    import os

    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    core = ApplicationCore()
    unauthorized_service = UnauthorizedService()

    # Act & Assert
    with pytest.raises(PermissionError):
        await core.broker.request_file_write(
            requester=unauthorized_service, path="bot_state.json", content="{}"
        )

    os.chdir(original_cwd)

async def test_get_state_success(tmp_path: Path, mock_config: Path):
    """
    Tests that the WorkspaceService can successfully read the state file.
    """
    # Arrange
    import os
    import json

    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    core = ApplicationCore()
    workspace = WorkspaceService(core)
    state_data = {"last_known_release_tag": "v1.0.0"}
    state_file_path = tmp_path / "bot_state.json"
    state_file_path.write_text(json.dumps(state_data))

    # Act
    read_state = await workspace.get_state()

    # Assert
    assert read_state["last_known_release_tag"] == "v1.0.0"

    os.chdir(original_cwd)