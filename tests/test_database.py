"""Tests for SQLite database module."""

import sqlite3
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
from returns.result import Success

from bitbot.core import db


@pytest.fixture
def temp_db():
    """Use temporary database file for tests."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        temp_path = Path(f.name)
    with patch.object(db, "DB_PATH", temp_path):
        db.init()
        yield temp_path
    temp_path.unlink(missing_ok=True)


class TestInit:
    """Tests for database initialization."""

    def test_init_creates_tables(self, temp_db):
        """init() creates all required tables."""
        conn = sqlite3.connect(temp_db)
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {row[0] for row in cursor.fetchall()}
        conn.close()

        assert "offline_versions" in tables
        assert "processed_releases" in tables
        assert "pending_releases" in tables
        assert "accounts" in tables
        assert "posted_versions" in tables
        assert "post_ids" in tables


class TestOfflineVersions:
    """Tests for offline_versions table operations."""

    def test_get_empty(self, temp_db):
        """get_offline_versions returns empty dict initially."""
        result = db.get_offline_versions()
        assert isinstance(result, Success)
        assert result.unwrap() == {}

    def test_set_and_get(self, temp_db):
        """set_offline_version stores and retrieves correctly."""
        db.set_offline_version("app1", "1.0.0")
        db.set_offline_version("app2", "2.0.0")

        result = db.get_offline_versions()
        assert result.unwrap() == {"app1": "1.0.0", "app2": "2.0.0"}

    def test_update_existing(self, temp_db):
        """set_offline_version updates existing entry."""
        db.set_offline_version("app1", "1.0.0")
        db.set_offline_version("app1", "1.1.0")

        result = db.get_offline_versions()
        assert result.unwrap() == {"app1": "1.1.0"}


class TestProcessedReleases:
    """Tests for processed_releases table operations."""
    def test_get_empty(self, temp_db):
        """get_processed_releases returns empty set initially."""
        result = db.get_processed_releases()
        assert isinstance(result, Success)
        assert result.unwrap() == set()

    def test_add_and_get(self, temp_db):
        """add_processed_release stores release IDs."""
        db.add_processed_release(100)
        db.add_processed_release(200)

        result = db.get_processed_releases()
        assert result.unwrap() == {100, 200}

    def test_add_duplicate_ignored(self, temp_db):
        """add_processed_release ignores duplicates."""
        db.add_processed_release(100)
        db.add_processed_release(100)

        result = db.get_processed_releases()
        assert result.unwrap() == {100}


class TestPendingReleases:
    """Tests for pending_releases table operations."""
    def test_get_empty(self, temp_db):
        """get_pending_releases returns empty list initially."""
        result = db.get_pending_releases()
        assert isinstance(result, Success)
        assert result.unwrap() == []

    def test_add_and_get(self, temp_db):
        """add_pending_release stores release data."""
        db.add_pending_release(100, "app1", "App One", "1.0.0", "v1.0.0")

        result = db.get_pending_releases()
        releases = result.unwrap()
        assert len(releases) == 1
        assert releases[0]["release_id"] == 100
        assert releases[0]["app_id"] == "app1"
        assert releases[0]["display_name"] == "App One"
        assert releases[0]["version"] == "1.0.0"
        assert releases[0]["tag"] == "v1.0.0"

    def test_remove(self, temp_db):
        """remove_pending_release removes by release_id."""
        db.add_pending_release(100, "app1", "App One", "1.0.0", "v1.0.0")
        db.add_pending_release(200, "app2", "App Two", "2.0.0", "v2.0.0")

        db.remove_pending_release(100)

        result = db.get_pending_releases()
        releases = result.unwrap()
        assert len(releases) == 1
        assert releases[0]["release_id"] == 200

    def test_clear(self, temp_db):
        """clear_pending_releases removes all."""
        db.add_pending_release(100, "app1", "App One", "1.0.0", "v1.0.0")
        db.add_pending_release(200, "app2", "App Two", "2.0.0", "v2.0.0")

        db.clear_pending_releases()

        result = db.get_pending_releases()
        assert result.unwrap() == []


class TestAccounts:
    """Tests for accounts table operations."""
    def test_create_account(self, temp_db):
        """get_or_create_account creates new account."""
        result = db.get_or_create_account("testuser", "testsubreddit")
        assert isinstance(result, Success)
        assert result.unwrap() > 0

    def test_get_existing_account(self, temp_db):
        """get_or_create_account returns existing account."""
        id1 = db.get_or_create_account("testuser", "testsubreddit").unwrap()
        id2 = db.get_or_create_account("testuser", "testsubreddit").unwrap()
        assert id1 == id2

    def test_different_accounts(self, temp_db):
        """Different user/subreddit combos get different IDs."""
        id1 = db.get_or_create_account("user1", "sub1").unwrap()
        id2 = db.get_or_create_account("user2", "sub1").unwrap()
        id3 = db.get_or_create_account("user1", "sub2").unwrap()
        assert id1 != id2 != id3

    def test_update_account(self, temp_db):
        """update_account modifies account metadata."""
        account_id = db.get_or_create_account("testuser", "testsub").unwrap()

        db.update_account(account_id, active_post_id="abc123", check_interval_seconds=300)

        result = db.get_account(account_id)
        meta = result.unwrap()
        assert meta["active_post_id"] == "abc123"
        assert meta["check_interval_seconds"] == 300


class TestPostedVersions:
    """Tests for posted_versions table operations."""
    def test_get_empty(self, temp_db):
        """get_posted_versions returns empty dict initially."""
        account_id = db.get_or_create_account("testuser", "testsub").unwrap()
        result = db.get_posted_versions(account_id)
        assert result.unwrap() == {}

    def test_set_and_get(self, temp_db):
        """set_posted_version stores versions per account."""
        account_id = db.get_or_create_account("testuser", "testsub").unwrap()

        db.set_posted_version(account_id, "app1", "1.0.0")
        db.set_posted_version(account_id, "app2", "2.0.0")

        result = db.get_posted_versions(account_id)
        assert result.unwrap() == {"app1": "1.0.0", "app2": "2.0.0"}

    def test_versions_isolated_per_account(self, temp_db):
        """Posted versions are isolated per account."""
        id1 = db.get_or_create_account("user1", "sub").unwrap()
        id2 = db.get_or_create_account("user2", "sub").unwrap()

        db.set_posted_version(id1, "app1", "1.0.0")
        db.set_posted_version(id2, "app1", "2.0.0")

        assert db.get_posted_versions(id1).unwrap() == {"app1": "1.0.0"}
        assert db.get_posted_versions(id2).unwrap() == {"app1": "2.0.0"}


class TestPostIds:
    """Tests for post_ids table operations."""
    def test_get_empty(self, temp_db):
        """get_post_ids returns empty list initially."""
        account_id = db.get_or_create_account("testuser", "testsub").unwrap()
        result = db.get_post_ids(account_id)
        assert result.unwrap() == []

    def test_add_and_get(self, temp_db):
        """add_post_id stores post IDs."""
        account_id = db.get_or_create_account("testuser", "testsub").unwrap()

        db.add_post_id(account_id, "post1")
        db.add_post_id(account_id, "post2")

        result = db.get_post_ids(account_id)
        assert set(result.unwrap()) == {"post1", "post2"}

    def test_add_duplicate_ignored(self, temp_db):
        """add_post_id ignores duplicates."""
        account_id = db.get_or_create_account("testuser", "testsub").unwrap()

        db.add_post_id(account_id, "post1")
        db.add_post_id(account_id, "post1")

        result = db.get_post_ids(account_id)
        assert result.unwrap() == ["post1"]


class TestExport:
    """Tests for export functionality."""
    def test_export_account_json(self, temp_db):
        """export_account_json returns complete state."""
        account_id = db.get_or_create_account("testuser", "testsub").unwrap()
        db.set_posted_version(account_id, "app1", "1.0.0")
        db.update_account(account_id, active_post_id="abc123", check_interval_seconds=300)
        db.add_post_id(account_id, "abc123")

        result = db.export_account_json("testuser", "testsub")
        data = result.unwrap()

        assert data["online"] == {"app1": "1.0.0"}
        assert data["activePostId"] == "abc123"
        assert data["currentIntervalSeconds"] == 300
        assert "abc123" in data["allPostIds"]
