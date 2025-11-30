"""Release-related database operations."""

from __future__ import annotations

import sqlite3
from typing import TypedDict

import icontract
from beartype import beartype
from returns.result import Failure, Result, Success

from bitbot.core.db import conn, db_fail
from bitbot.core.errors import StateError


class PendingRelease(TypedDict):
    """Pending release from queue."""

    release_id: int
    app_id: str
    display_name: str
    version: str
    tag: str
    asset_name: str | None


@beartype
def get_offline_versions() -> Result[dict[str, str], StateError]:
    """Get offline versions (what's in bot's repo)."""
    try:
        with conn() as c:
            rows = c.execute("SELECT app_id, version FROM offline_versions").fetchall()
        return Success({r["app_id"]: r["version"] for r in rows})
    except sqlite3.Error as e:
        return db_fail("Failed to get offline versions", e)


@icontract.require(lambda app_id: len(app_id) > 0)
@icontract.require(lambda version: len(version) > 0)
@beartype
def set_offline_version(app_id: str, version: str) -> Result[None, StateError]:
    """Set offline version for an app."""
    try:
        with conn() as c:
            c.execute(
                "INSERT OR REPLACE INTO offline_versions (app_id, version) VALUES (?, ?)",
                (app_id, version),
            )
        return Success(None)
    except sqlite3.Error as e:
        return db_fail("Failed to set offline version", e)


@beartype
def get_processed_releases() -> Result[set[int], StateError]:
    """Get processed source release IDs."""
    try:
        with conn() as c:
            rows = c.execute("SELECT release_id FROM processed_releases").fetchall()
        return Success({r["release_id"] for r in rows})
    except sqlite3.Error as e:
        return db_fail("Failed to get processed releases", e)


@icontract.require(lambda release_id: release_id > 0)
@beartype
def add_processed_release(release_id: int) -> Result[None, StateError]:
    """Mark a source release as processed."""
    try:
        with conn() as c:
            c.execute(
                "INSERT OR IGNORE INTO processed_releases (release_id) VALUES (?)",
                (release_id,),
            )
        return Success(None)
    except sqlite3.Error as e:
        return db_fail("Failed to add processed release", e)


@beartype
def get_pending_releases() -> Result[list[PendingRelease], StateError]:
    """Get pending releases from queue in insertion order."""
    try:
        with conn() as c:
            rows = c.execute(
                """SELECT release_id, app_id, display_name, version, tag, asset_name
                   FROM pending_releases ORDER BY rowid"""
            ).fetchall()
        releases: list[PendingRelease] = [
            {
                "release_id": r["release_id"],
                "app_id": r["app_id"],
                "display_name": r["display_name"],
                "version": r["version"],
                "tag": r["tag"],
                "asset_name": r["asset_name"],
            }
            for r in rows
        ]
        return Success(releases)
    except sqlite3.Error as e:
        return db_fail("Failed to get pending releases", e)


@icontract.require(lambda release_id: release_id > 0)
@icontract.require(lambda app_id: len(app_id) > 0)
@icontract.require(lambda version: len(version) > 0)
@icontract.require(lambda tag: len(tag) > 0)
@beartype
def add_pending_release(  # noqa: PLR0913
    release_id: int,
    app_id: str,
    display_name: str,
    version: str,
    tag: str,
    asset_name: str | None = None,
) -> Result[None, StateError]:
    """Add a release to the pending queue."""
    try:
        with conn() as c:
            c.execute(
                """INSERT INTO pending_releases
                   (release_id, app_id, display_name, version, tag, asset_name)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (release_id, app_id, display_name, version, tag, asset_name),
            )
        return Success(None)
    except sqlite3.IntegrityError:
        return Failure(StateError(f"Release {release_id} already in queue"))
    except sqlite3.Error as e:
        return db_fail("Failed to add pending release", e)


@icontract.require(lambda release_id: release_id > 0)
@beartype
def remove_pending_release(release_id: int) -> Result[None, StateError]:
    """Remove a release from the pending queue."""
    try:
        with conn() as c:
            c.execute("DELETE FROM pending_releases WHERE release_id = ?", (release_id,))
        return Success(None)
    except sqlite3.Error as e:
        return db_fail("Failed to remove pending release", e)


@beartype
def clear_pending_releases() -> Result[None, StateError]:
    """Clear all pending releases."""
    try:
        with conn() as c:
            c.execute("DELETE FROM pending_releases")
        return Success(None)
    except sqlite3.Error as e:
        return db_fail("Failed to clear pending releases", e)
