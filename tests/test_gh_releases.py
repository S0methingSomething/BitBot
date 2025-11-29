"""Tests for GitHub release operations."""

from unittest.mock import MagicMock

from returns.result import Failure, Success

from bitbot.core.errors import GitHubAPIError
from bitbot.gh.releases.fetcher import get_github_data, get_source_releases


def test_get_github_data_success(mocker):
    """Test get_github_data returns Success on success."""
    mock_run = mocker.patch("bitbot.gh.releases.fetcher.run_command")
    mock_process = MagicMock()
    mock_process.stdout = '{"name": "test-repo"}'
    mock_run.return_value = Success(mock_process)

    result = get_github_data("/repos/owner/repo")

    assert isinstance(result, Success)
    data = result.unwrap()
    assert data["name"] == "test-repo"


def test_get_github_data_invalid_json(mocker):
    """Test get_github_data returns Failure on invalid JSON."""
    mock_run = mocker.patch("bitbot.gh.releases.fetcher.run_command")
    mock_process = MagicMock()
    mock_process.stdout = "not valid json{"
    mock_run.return_value = Success(mock_process)

    result = get_github_data("/repos/owner/repo")

    assert isinstance(result, Failure)
    assert "Failed to parse" in str(result.failure())


def test_get_source_releases_success(mocker):
    """Test get_source_releases returns list of releases."""
    mock_get = mocker.patch("bitbot.gh.releases.fetcher.get_github_data")
    mock_get.return_value = Success(
        [
            {"id": 1, "tag_name": "v1.0.0"},
            {"id": 2, "tag_name": "v2.0.0"},
        ]
    )

    result = get_source_releases("owner/repo")

    assert isinstance(result, Success)
    releases = result.unwrap()
    assert len(releases) == 2
    assert releases[0]["tag_name"] == "v1.0.0"


def test_get_source_releases_not_list(mocker):
    """Test get_source_releases returns Failure if response not list."""
    mock_get = mocker.patch("bitbot.gh.releases.fetcher.get_github_data")
    mock_get.return_value = Success({"error": "not a list"})

    result = get_source_releases("owner/repo")

    assert isinstance(result, Failure)
    assert "Expected list" in str(result.failure())


def test_get_github_data_empty_response(mocker):
    """Test get_github_data handles empty JSON object."""
    mock_run = mocker.patch("bitbot.gh.releases.fetcher.run_command")
    mock_process = MagicMock()
    mock_process.stdout = "{}"
    mock_run.return_value = Success(mock_process)

    result = get_github_data("/repos/owner/repo")

    assert isinstance(result, Success)
    assert result.unwrap() == {}


def test_get_github_data_array_response(mocker):
    """Test get_github_data handles JSON array."""
    mock_run = mocker.patch("bitbot.gh.releases.fetcher.run_command")
    mock_process = MagicMock()
    mock_process.stdout = '[{"id": 1}, {"id": 2}]'
    mock_run.return_value = Success(mock_process)

    result = get_github_data("/repos/owner/repo")

    assert isinstance(result, Success)
    data = result.unwrap()
    assert isinstance(data, list)
    assert len(data) == 2


def test_get_source_releases_empty_list(mocker):
    """Test get_source_releases handles empty release list."""
    mock_get = mocker.patch("bitbot.gh.releases.fetcher.get_github_data")
    mock_get.return_value = Success([])

    result = get_source_releases("owner/repo")

    assert isinstance(result, Success)
    assert result.unwrap() == []


def test_get_source_releases_propagates_error(mocker):
    """Test get_source_releases propagates get_github_data errors."""
    mock_get = mocker.patch("bitbot.gh.releases.fetcher.get_github_data")
    mock_get.return_value = Failure(GitHubAPIError("API failed"))

    result = get_source_releases("owner/repo")

    assert isinstance(result, Failure)
    assert "API failed" in str(result.failure())
