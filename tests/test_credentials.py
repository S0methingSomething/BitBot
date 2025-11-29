"""Tests for credentials module."""

import pytest

from bitbot.core.credentials import (
    get_github_output,
    get_github_token,
    get_reddit_client_id,
    get_reddit_client_secret,
    get_reddit_password,
    get_reddit_user_agent,
    get_reddit_username,
)


def test_get_github_token_success(monkeypatch):
    """Test get_github_token returns token when set."""
    monkeypatch.setenv("GITHUB_TOKEN", "test-token-123")
    assert get_github_token() == "test-token-123"


def test_get_github_token_missing(monkeypatch):
    """Test get_github_token raises when not set."""
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    with pytest.raises(ValueError, match="GITHUB_TOKEN"):
        get_github_token()


def test_get_github_output_success(monkeypatch):
    """Test get_github_output returns path when set."""
    monkeypatch.setenv("GITHUB_OUTPUT", "/var/output")
    assert get_github_output() == "/var/output"


def test_get_github_output_empty_valid(monkeypatch):
    """Test get_github_output returns empty string when not set (valid)."""
    monkeypatch.delenv("GITHUB_OUTPUT", raising=False)
    assert get_github_output() == ""


def test_get_reddit_client_id_success(monkeypatch):
    """Test get_reddit_client_id returns value when set."""
    monkeypatch.setenv("REDDIT_CLIENT_ID", "client-id-123")
    assert get_reddit_client_id() == "client-id-123"


def test_get_reddit_client_id_missing(monkeypatch):
    """Test get_reddit_client_id raises when not set."""
    monkeypatch.delenv("REDDIT_CLIENT_ID", raising=False)
    with pytest.raises(ValueError, match="REDDIT_CLIENT_ID"):
        get_reddit_client_id()


def test_get_reddit_client_secret_success(monkeypatch):
    """Test get_reddit_client_secret returns value when set."""
    monkeypatch.setenv("REDDIT_CLIENT_SECRET", "secret-123")
    assert get_reddit_client_secret() == "secret-123"


def test_get_reddit_client_secret_missing(monkeypatch):
    """Test get_reddit_client_secret raises when not set."""
    monkeypatch.delenv("REDDIT_CLIENT_SECRET", raising=False)
    with pytest.raises(ValueError, match="REDDIT_CLIENT_SECRET"):
        get_reddit_client_secret()


def test_get_reddit_username_success(monkeypatch):
    """Test get_reddit_username returns value when set."""
    monkeypatch.setenv("REDDIT_USERNAME", "testuser")
    assert get_reddit_username() == "testuser"


def test_get_reddit_username_missing(monkeypatch):
    """Test get_reddit_username raises when not set."""
    monkeypatch.delenv("REDDIT_USERNAME", raising=False)
    with pytest.raises(ValueError, match="REDDIT_USERNAME"):
        get_reddit_username()


def test_get_reddit_password_success(monkeypatch):
    """Test get_reddit_password returns value when set."""
    monkeypatch.setenv("REDDIT_PASSWORD", "password123")
    assert get_reddit_password() == "password123"


def test_get_reddit_password_missing(monkeypatch):
    """Test get_reddit_password raises when not set."""
    monkeypatch.delenv("REDDIT_PASSWORD", raising=False)
    with pytest.raises(ValueError, match="REDDIT_PASSWORD"):
        get_reddit_password()


def test_get_reddit_user_agent_from_env(monkeypatch):
    """Test get_reddit_user_agent returns env value when no config."""
    monkeypatch.setenv("REDDIT_USER_AGENT", "TestBot/1.0")
    assert get_reddit_user_agent() == "TestBot/1.0"


def test_get_reddit_user_agent_missing(monkeypatch):
    """Test get_reddit_user_agent raises when not set and no config."""
    monkeypatch.delenv("REDDIT_USER_AGENT", raising=False)
    with pytest.raises(ValueError, match="REDDIT_USER_AGENT"):
        get_reddit_user_agent()
