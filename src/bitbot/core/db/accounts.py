"""Account-related database operations."""

from __future__ import annotations

import sqlite3
from typing import Any, TypedDict

import icontract
from beartype import beartype
from returns.result import Failure, Result, Success

from bitbot.core.db import conn, db_fail
from bitbot.core.errors import StateError


class AccountMeta(TypedDict):
    """Account metadata from database."""

    active_post_id: str | None
    last_check_timestamp: str | None
    check_interval_seconds: int | None
    last_comment_count: int | None


@icontract.require(lambda username: len(username) > 0)
@icontract.require(lambda subreddit: len(subreddit) > 0)
@beartype
def get_or_create_account(username: str, subreddit: str) -> Result[int, StateError]:
    """Get or create account, return ID."""
    try:
        with conn() as c:
            c.execute(
                "INSERT OR IGNORE INTO accounts (username, subreddit) VALUES (?, ?)",
                (username, subreddit),
            )
            row = c.execute(
                "SELECT id FROM accounts WHERE username = ? AND subreddit = ?",
                (username, subreddit),
            ).fetchone()
            if not row:
                return Failure(StateError("Failed to create/get account"))
            return Success(row["id"])
    except sqlite3.Error as e:
        return db_fail("Failed to get/create account", e)


@icontract.require(lambda account_id: account_id > 0)
@beartype
def get_posted_versions(account_id: int) -> Result[dict[str, str], StateError]:
    """Get posted versions for an account."""
    try:
        with conn() as c:
            rows = c.execute(
                "SELECT app_id, version FROM posted_versions WHERE account_id = ?",
                (account_id,),
            ).fetchall()
        return Success({r["app_id"]: r["version"] for r in rows})
    except sqlite3.Error as e:
        return db_fail("Failed to get posted versions", e)


@icontract.require(lambda account_id: account_id > 0)
@beartype
def set_posted_version(account_id: int, app_id: str, version: str) -> Result[None, StateError]:
    """Set posted version for an app."""
    try:
        with conn() as c:
            c.execute(
                """INSERT OR REPLACE INTO posted_versions (account_id, app_id, version)
                   VALUES (?, ?, ?)""",
                (account_id, app_id, version),
            )
        return Success(None)
    except sqlite3.Error as e:
        return db_fail("Failed to set posted version", e)


@icontract.require(lambda account_id: account_id > 0)
@beartype
def get_account(account_id: int) -> Result[AccountMeta, StateError]:
    """Get account metadata."""
    try:
        with conn() as c:
            row = c.execute(
                """SELECT active_post_id, last_check_timestamp,
                          check_interval_seconds, last_comment_count
                   FROM accounts WHERE id = ?""",
                (account_id,),
            ).fetchone()
        if not row:
            return Failure(StateError(f"Account {account_id} not found"))
        return Success({
            "active_post_id": row["active_post_id"],
            "last_check_timestamp": row["last_check_timestamp"],
            "check_interval_seconds": row["check_interval_seconds"],
            "last_comment_count": row["last_comment_count"],
        })
    except sqlite3.Error as e:
        return db_fail("Failed to get account", e)


_UPDATE_COLS = {
    "active_post_id": "active_post_id = ?",
    "last_check_timestamp": "last_check_timestamp = ?",
    "check_interval_seconds": "check_interval_seconds = ?",
    "last_comment_count": "last_comment_count = ?",
}


@icontract.require(lambda account_id: account_id > 0)
@beartype
def update_account(
    account_id: int,
    *,
    active_post_id: str | None = None,
    last_check_timestamp: str | None = None,
    check_interval_seconds: int | None = None,
    last_comment_count: int | None = None,
) -> Result[None, StateError]:
    """Update account metadata."""
    updates: list[str] = []
    params: list[Any] = []

    if active_post_id is not None:
        updates.append(_UPDATE_COLS["active_post_id"])
        params.append(active_post_id)
    if last_check_timestamp is not None:
        updates.append(_UPDATE_COLS["last_check_timestamp"])
        params.append(last_check_timestamp)
    if check_interval_seconds is not None:
        updates.append(_UPDATE_COLS["check_interval_seconds"])
        params.append(check_interval_seconds)
    if last_comment_count is not None:
        updates.append(_UPDATE_COLS["last_comment_count"])
        params.append(last_comment_count)

    if not updates:
        return Success(None)

    try:
        params.append(account_id)
        with conn() as c:
            c.execute(f"UPDATE accounts SET {', '.join(updates)} WHERE id = ?", params)  # noqa: S608 - cols whitelisted
        return Success(None)
    except sqlite3.Error as e:
        return db_fail("Failed to update account", e)


@icontract.require(lambda account_id: account_id > 0)
@beartype
def get_post_ids(account_id: int) -> Result[list[str], StateError]:
    """Get all post IDs for an account in insertion order."""
    try:
        with conn() as c:
            rows = c.execute(
                "SELECT post_id FROM post_ids WHERE account_id = ? ORDER BY rowid",
                (account_id,),
            ).fetchall()
        return Success([r["post_id"] for r in rows])
    except sqlite3.Error as e:
        return db_fail("Failed to get post IDs", e)


@icontract.require(lambda account_id: account_id > 0)
@icontract.require(lambda post_id: len(post_id) > 0)
@beartype
def add_post_id(account_id: int, post_id: str) -> Result[None, StateError]:
    """Add a post ID for an account."""
    try:
        with conn() as c:
            c.execute(
                "INSERT OR IGNORE INTO post_ids (post_id, account_id) VALUES (?, ?)",
                (post_id, account_id),
            )
        return Success(None)
    except sqlite3.Error as e:
        return db_fail("Failed to add post ID", e)


@icontract.require(lambda username: len(username) > 0)
@icontract.require(lambda subreddit: len(subreddit) > 0)
@beartype
def export_account_json(username: str, subreddit: str) -> Result[dict[str, Any], StateError]:
    """Export account state as JSON-compatible dict for other projects."""
    account_result = get_or_create_account(username, subreddit)
    if isinstance(account_result, Failure):
        return Failure(account_result.failure())

    account_id = account_result.unwrap()

    versions = get_posted_versions(account_id)
    if isinstance(versions, Failure):
        return Failure(versions.failure())

    meta = get_account(account_id)
    if isinstance(meta, Failure):
        return Failure(meta.failure())

    posts = get_post_ids(account_id)
    if isinstance(posts, Failure):
        return Failure(posts.failure())

    m = meta.unwrap()
    return Success({
        "online": versions.unwrap(),
        "activePostId": m["active_post_id"],
        "lastCheckTimestamp": m["last_check_timestamp"],
        "currentIntervalSeconds": m["check_interval_seconds"],
        "allPostIds": posts.unwrap(),
    })
