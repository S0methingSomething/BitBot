#!/usr/bin/env python3
"""Migrate JSON state files to SQLite database."""

import json
import re
import sys
from pathlib import Path

from returns.result import Failure

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from bitbot.core import db

ROOT = Path(__file__).parent.parent


def migrate_account_state(filepath: Path) -> None:
    """Migrate a bot_state*.json file."""
    # Extract username/subreddit from filename
    # Format: bot_state_re-{username}_{subreddit}.json or bot_state.json
    name = filepath.stem
    if name == "bot_state":
        username = "BitBot"  # default
        subreddit = "BitLifeRebels"  # default from config
    else:
        match = re.match(r"bot_state_re-(.+)_(.+)", name)
        if not match:
            print(f"  Skipping {filepath.name} - unknown format")
            return
        username, subreddit = match.groups()

    with filepath.open() as f:
        data = json.load(f)

    # Get or create account
    result = db.get_or_create_account(username, subreddit)
    if isinstance(result, Failure):
        print(f"  Error creating account: {result.failure()}")
        return
    account_id = result.unwrap()

    # Import posted versions
    online = data.get("online", {})
    for app_id, version in online.items():
        db.set_posted_version(account_id, app_id, version)

    # Import account metadata
    db.update_account(
        account_id,
        active_post_id=data.get("activePostId"),
        last_check_timestamp=data.get("lastCheckTimestamp"),
        check_interval_seconds=data.get("currentIntervalSeconds"),
    )

    # Import post IDs
    for post_id in data.get("allPostIds", []):
        db.add_post_id(account_id, post_id)

    print(f"  ✓ {username}/{subreddit}: {len(online)} versions, {len(data.get('allPostIds', []))} posts")


def migrate_release_state(filepath: Path) -> None:
    """Migrate release_state.json (processed release IDs)."""
    with filepath.open() as f:
        release_ids = json.load(f)

    for rid in release_ids:
        db.add_processed_release(rid)

    print(f"  ✓ {len(release_ids)} processed releases")


def main() -> None:
    """Run migration."""
    print("Initializing database...")
    db.init()

    print("\nMigrating account states...")
    for f in ROOT.glob("bot_state*.json"):
        migrate_account_state(f)

    print("\nMigrating release state...")
    release_state = ROOT / "release_state.json"
    if release_state.exists():
        migrate_release_state(release_state)
    else:
        print("  No release_state.json found")

    print("\n✓ Migration complete!")
    print(f"  Database: {db.DB_PATH}")


if __name__ == "__main__":
    main()
