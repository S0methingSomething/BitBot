"""Reddit state management.

Architecture:
- releases.json = source of truth for what versions exist
- Local DB = our record of what we've announced (not parsed from Reddit)
- Reddit = output destination, verified but not parsed for data

We don't parse versions from Reddit posts. Instead:
1. Local DB tracks what we've announced
2. We verify Reddit post exists and content matches
3. If state is wrong, user can --reset and re-announce
"""

import hashlib
from dataclasses import dataclass

import praw
from beartype import beartype
from returns.result import Failure, Result, Success

from bitbot.config_models import Config
from bitbot.core import db
from bitbot.core.errors import RedditAPIError
from bitbot.reddit.posts import get_bot_posts


@dataclass
class PostStatus:
    """Status of the Reddit post."""

    exists: bool
    accessible: bool
    post_id: str | None
    post_url: str | None
    current_body: str | None
    current_hash: str | None
    is_removed: bool
    removal_reason: str | None


@dataclass
class StateCheck:
    """Result of state verification."""

    post_ok: bool
    content_matches: bool
    stored_hash: str | None
    current_hash: str | None
    issues: list[str]


@beartype
def compute_content_hash(body: str) -> str:
    """Compute hash of post body for change detection."""
    # Normalize: lowercase, collapse whitespace
    normalized = " ".join(body.lower().split())
    return hashlib.sha256(normalized.encode()).hexdigest()[:16]


@beartype
def check_post_exists(reddit: praw.Reddit, post_id: str) -> PostStatus:
    """Check if a Reddit post exists and is accessible."""
    try:
        submission = reddit.submission(id=post_id)
        # Access an attribute to trigger the fetch
        _ = submission.selftext

        is_removed = bool(submission.removed_by_category)
        removal_reason = submission.removed_by_category if is_removed else None

        return PostStatus(
            exists=True,
            accessible=not is_removed,
            post_id=post_id,
            post_url=submission.url,
            current_body=submission.selftext,
            current_hash=compute_content_hash(submission.selftext),
            is_removed=is_removed,
            removal_reason=removal_reason,
        )
    except Exception:
        return PostStatus(
            exists=False,
            accessible=False,
            post_id=post_id,
            post_url=None,
            current_body=None,
            current_hash=None,
            is_removed=False,
            removal_reason=None,
        )


@beartype
def verify_state(
    reddit: praw.Reddit,
    account_id: int,
    expected_body: str | None = None,
) -> StateCheck:
    """Verify local state against Reddit.

    Checks:
    1. Does the active post exist?
    2. Is it accessible (not removed)?
    3. Does content hash match what we stored?
    """
    issues: list[str] = []

    # Get stored state
    meta_result = db.get_account(account_id)
    if isinstance(meta_result, Failure):
        return StateCheck(
            post_ok=False,
            content_matches=False,
            stored_hash=None,
            current_hash=None,
            issues=["Failed to get account metadata"],
        )

    meta = meta_result.unwrap()
    active_post_id = meta.get("active_post_id")
    stored_hash = meta.get("content_hash")

    if not active_post_id:
        return StateCheck(
            post_ok=True,  # No post is OK - we'll create one
            content_matches=True,
            stored_hash=stored_hash,
            current_hash=None,
            issues=[],
        )

    # Check post on Reddit
    status = check_post_exists(reddit, active_post_id)

    if not status.exists:
        issues.append(f"Post {active_post_id} no longer exists on Reddit")
        return StateCheck(
            post_ok=False,
            content_matches=False,
            stored_hash=stored_hash,
            current_hash=None,
            issues=issues,
        )

    if status.is_removed:
        issues.append(f"Post was removed: {status.removal_reason}")
        return StateCheck(
            post_ok=False,
            content_matches=False,
            stored_hash=stored_hash,
            current_hash=status.current_hash,
            issues=issues,
        )

    # Check content hash
    content_matches = True
    if stored_hash and status.current_hash:
        if stored_hash != status.current_hash:
            issues.append("Post content was modified externally")
            content_matches = False

    # If we have expected body, check against that too
    if expected_body:
        expected_hash = compute_content_hash(expected_body)
        if status.current_hash != expected_hash:
            issues.append("Post content differs from expected")
            content_matches = False

    return StateCheck(
        post_ok=True,
        content_matches=content_matches,
        stored_hash=stored_hash,
        current_hash=status.current_hash,
        issues=issues,
    )


@beartype
def get_current_post(
    reddit: praw.Reddit, config: Config
) -> Result[PostStatus | None, RedditAPIError]:
    """Get the current active post from Reddit."""
    try:
        posts_result = get_bot_posts(reddit, config)
        if isinstance(posts_result, Failure):
            return Failure(posts_result.failure())

        posts = posts_result.unwrap()
        if not posts:
            return Success(None)

        latest = posts[0]
        is_removed = bool(latest.removed_by_category)

        return Success(PostStatus(
            exists=True,
            accessible=not is_removed,
            post_id=latest.id,
            post_url=latest.url,
            current_body=latest.selftext,
            current_hash=compute_content_hash(latest.selftext),
            is_removed=is_removed,
            removal_reason=latest.removed_by_category if is_removed else None,
        ))
    except Exception as e:
        return Failure(RedditAPIError(f"Failed to get current post: {e}"))


@beartype
def handle_state_issues(
    account_id: int,
    state_check: StateCheck,
    auto_fix: bool = False,
) -> list[str]:
    """Handle state issues, optionally auto-fixing.

    Returns list of actions taken.
    """
    actions: list[str] = []

    if not state_check.post_ok:
        if auto_fix:
            # Clear the invalid post ID so we create a new one
            db.update_account(account_id, active_post_id="")
            actions.append("Cleared invalid post ID - will create new post")
        else:
            actions.append("Post is invalid - use --reset to clear state")

    if not state_check.content_matches and state_check.post_ok:
        if auto_fix:
            actions.append("Content mismatch detected - will update post")
        else:
            actions.append("Content mismatch - use --refresh to update")

    return actions
