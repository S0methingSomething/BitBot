"""Tests for database error handling paths."""

import pytest
from returns.result import Failure, Success

from bitbot.core import db
from bitbot.core.db.accounts import (
    export_account_json,
    get_account,
    get_or_create_account,
    update_account,
)
from bitbot.core.db.releases import add_pending_release


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    """Setup temporary database."""
    test_db = tmp_path / "test.db"
    monkeypatch.setattr(db, "DB_PATH", str(test_db))
    db.init()
    return test_db


class TestPendingReleases:
    """Tests for pending releases error handling."""

    def test_add_pending_release_duplicate(self, temp_db):
        """Test adding duplicate pending release."""
        # Add first time - should succeed
        result1 = add_pending_release(
            release_id=1, app_id="test", display_name="Test", version="1.0", tag="v1.0"
        )
        assert isinstance(result1, Success)

        # Add duplicate - should fail
        result2 = add_pending_release(
            release_id=1, app_id="test", display_name="Test", version="1.0", tag="v1.0"
        )
        assert isinstance(result2, Failure)
        assert "already in queue" in str(result2.failure())


class TestAccountErrors:
    """Tests for account database error handling."""

    def test_get_account_not_found(self, temp_db):
        """Test getting non-existent account."""
        result = get_account(99999)
        assert isinstance(result, Failure)
        assert "not found" in str(result.failure())

    def test_update_account_no_changes(self, temp_db):
        """Test update with no changes returns success."""
        # Create account
        account_result = get_or_create_account("testuser", "testsub")
        account_id = account_result.unwrap()

        # Update with no params - should succeed
        result = update_account(account_id)
        assert isinstance(result, Success)

    def test_export_account_json(self, temp_db):
        """Test exporting account as JSON."""
        get_or_create_account("testuser", "testsub")

        result = export_account_json("testuser", "testsub")
        assert isinstance(result, Success)
        data = result.unwrap()
        assert "online" in data
        assert "activePostId" in data
