"""Tests for Pydantic models."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from models import AppConfig, BotState, Config, GitHubConfig, RedditConfig


def test_config_validation():
    """Test Config model validation."""
    valid_config = {
        "github": {"sourceRepo": "test/repo", "botRepo": "bot/repo"},
        "reddit": {"subreddit": "test", "postMode": "direct", "postIdentifier": "test"},
    }
    config = Config(**valid_config)
    assert config.github.source_repo == "test/repo"


def test_config_invalid_raises():
    """Test invalid config raises ValidationError."""
    with pytest.raises(Exception):  # pydantic.ValidationError
        Config(invalid="data")


def test_bot_state_validation():
    """Test BotState model validation."""
    valid_state = {
        "online": {"lastPostedVersions": {}},
        "offline": {"lastGeneratedVersions": {}},
    }
    state = BotState(**valid_state)
    assert state.online is not None


def test_github_config():
    """Test GitHubConfig model."""
    config = GitHubConfig(sourceRepo="test/repo", botRepo="bot/repo")
    assert config.source_repo == "test/repo"


def test_reddit_config():
    """Test RedditConfig model."""
    config = RedditConfig(subreddit="test", postMode="direct", postIdentifier="[Test]")
    assert config.subreddit == "test"


def test_app_config():
    """Test AppConfig model."""
    app = AppConfig(id="test", displayName="Test App")
    assert app.id == "test"
    assert app.display_name == "Test App"
