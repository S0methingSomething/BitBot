"""SQLite database for BitBot state management."""

from __future__ import annotations

import sqlite3
from collections.abc import Iterator  # noqa: TC003
from contextlib import contextmanager

from beartype import beartype
from returns.result import Failure, Result, Success

from bitbot import paths
from bitbot.core.errors import StateError

DB_PATH = paths.DATABASE_FILE


def db_fail(msg: str, e: sqlite3.Error) -> Failure[StateError]:
    """Create a Failure with StateError for database errors."""
    return Failure(StateError(f"{msg}: {e}"))


_SCHEMA = """
CREATE TABLE IF NOT EXISTS offline_versions (
    app_id TEXT PRIMARY KEY,
    version TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS processed_releases (
    release_id INTEGER PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS pending_releases (
    release_id INTEGER PRIMARY KEY,
    app_id TEXT NOT NULL,
    display_name TEXT NOT NULL,
    version TEXT NOT NULL,
    tag TEXT NOT NULL,
    asset_name TEXT
);

CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    subreddit TEXT NOT NULL,
    active_post_id TEXT,
    last_check_timestamp TEXT,
    check_interval_seconds INTEGER,
    last_comment_count INTEGER DEFAULT 0,
    content_hash TEXT,
    UNIQUE(username, subreddit)
);

CREATE TABLE IF NOT EXISTS posted_versions (
    account_id INTEGER NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
    app_id TEXT NOT NULL,
    version TEXT NOT NULL,
    PRIMARY KEY (account_id, app_id)
);

CREATE TABLE IF NOT EXISTS post_ids (
    post_id TEXT PRIMARY KEY,
    account_id INTEGER NOT NULL REFERENCES accounts(id) ON DELETE CASCADE
);
"""

# Migration to add content_hash column if missing
_MIGRATIONS = [
    "ALTER TABLE accounts ADD COLUMN content_hash TEXT",
]


@contextmanager
@beartype
def conn() -> Iterator[sqlite3.Connection]:
    """Database connection context manager with auto-commit."""
    connection = sqlite3.connect(DB_PATH, timeout=30.0)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA journal_mode=WAL")
    connection.execute("PRAGMA foreign_keys=ON")
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


@beartype
def _run_migrations(c: sqlite3.Connection) -> None:
    """Run schema migrations."""
    for migration in _MIGRATIONS:
        try:
            c.execute(migration)
        except sqlite3.OperationalError:
            # Column already exists or migration already applied
            pass


@beartype
def init() -> Result[None, StateError]:
    """Initialize database schema."""
    try:
        with conn() as c:
            c.executescript(_SCHEMA)
            _run_migrations(c)
        return Success(None)
    except sqlite3.Error as e:
        return db_fail("DB init failed", e)


@beartype
def clear_posted_versions(account_id: int) -> Result[None, StateError]:
    """Clear all posted versions for an account (for reset)."""
    try:
        with conn() as c:
            c.execute("DELETE FROM posted_versions WHERE account_id = ?", (account_id,))
        return Success(None)
    except sqlite3.Error as e:
        return db_fail("Failed to clear posted versions", e)


@beartype
def reset_account_state(account_id: int) -> Result[None, StateError]:
    """Reset account state (clear versions, post ID, hash)."""
    try:
        with conn() as c:
            c.execute("DELETE FROM posted_versions WHERE account_id = ?", (account_id,))
            c.execute(
                "UPDATE accounts SET active_post_id = NULL, content_hash = NULL WHERE id = ?",
                (account_id,),
            )
        return Success(None)
    except sqlite3.Error as e:
        return db_fail("Failed to reset account state", e)


from bitbot.core.db.accounts import (  # noqa: E402
    AccountMeta,
    add_post_id,
    export_account_json,
    get_account,
    get_or_create_account,
    get_post_ids,
    get_posted_versions,
    set_posted_version,
    update_account,
)
from bitbot.core.db.releases import (  # noqa: E402
    PendingRelease,
    add_pending_release,
    add_processed_release,
    clear_pending_releases,
    get_offline_versions,
    get_pending_releases,
    get_processed_releases,
    remove_pending_release,
    set_offline_version,
)

__all__ = [
    "DB_PATH",
    "AccountMeta",
    "PendingRelease",
    "add_pending_release",
    "add_post_id",
    "add_processed_release",
    "clear_pending_releases",
    "clear_posted_versions",
    "conn",
    "export_account_json",
    "get_account",
    "get_offline_versions",
    "get_or_create_account",
    "get_pending_releases",
    "get_post_ids",
    "get_posted_versions",
    "get_processed_releases",
    "init",
    "remove_pending_release",
    "reset_account_state",
    "set_offline_version",
    "set_posted_version",
    "update_account",
]
