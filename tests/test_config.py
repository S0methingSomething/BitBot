"""Tests for config loading."""

from returns.result import Failure, Success

from bitbot.core.config import load_config
from bitbot.core.errors import ConfigurationError


def test_load_config_returns_result(monkeypatch):
    """Test load_config returns a Result type."""
    # Use actual config file
    result = load_config()

    # Should return Result (Success or Failure)
    assert isinstance(result, (Success, Failure))


def test_load_config_missing_file(tmp_path, monkeypatch):
    """Test load_config returns Failure when file missing."""
    config_file = tmp_path / "nonexistent.toml"
    monkeypatch.setattr("bitbot.paths.CONFIG_FILE", config_file)

    result = load_config()

    assert isinstance(result, Failure)
    error = result.failure()
    assert isinstance(error, ConfigurationError)


def test_load_config_invalid_toml(tmp_path, monkeypatch):
    """Test load_config returns Failure on invalid TOML."""
    config_file = tmp_path / "config.toml"
    config_file.write_text("invalid toml {{{")
    monkeypatch.setattr("bitbot.paths.CONFIG_FILE", config_file)

    result = load_config()

    assert isinstance(result, Failure)
    assert isinstance(result.failure(), ConfigurationError)
