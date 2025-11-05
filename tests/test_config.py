"""Tests for config loading."""

import pytest

from bitbot.core.config import load_config
from bitbot.core.errors import ConfigurationError


def test_load_config_returns_result(monkeypatch):
    """Test load_config returns a Result type."""
    # Use actual config file
    result = load_config()
    
    # Should return Result (Ok or Err)
    assert hasattr(result, 'is_ok')
    assert hasattr(result, 'is_err')


def test_load_config_missing_file(tmp_path, monkeypatch):
    """Test load_config returns Err when file missing."""
    config_file = tmp_path / "nonexistent.toml"
    monkeypatch.setattr("bitbot.paths.CONFIG_FILE", config_file)
    
    result = load_config()
    
    assert result.is_err()
    error = result.unwrap_err()
    assert isinstance(error, ConfigurationError)


def test_load_config_invalid_toml(tmp_path, monkeypatch):
    """Test load_config returns Err on invalid TOML."""
    config_file = tmp_path / "config.toml"
    config_file.write_text("invalid toml {{{")
    monkeypatch.setattr("bitbot.paths.CONFIG_FILE", config_file)
    
    result = load_config()
    
    assert result.is_err()
    assert isinstance(result.unwrap_err(), ConfigurationError)
