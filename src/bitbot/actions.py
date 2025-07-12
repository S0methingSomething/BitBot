import logging
import re
from pathlib import Path
from typing import Any, cast

import semver
from requests import HTTPError

from . import crypto
from .clients import GitHubClient, RedditClient
from .config import Config

STATE_FILE = Path("latest_postid.txt")

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def _get_active_post_id() -> str | None:
    """Reads the active post ID from the state file.
    Returns None if the file is missing, empty, or contains only whitespace.
    """
    try:
        content = STATE_FILE.read_text(encoding="utf-8").strip()
        if content:
            return content
        logging.warning(f"State file '{STATE_FILE}' was found but is empty.")
        return None
    except FileNotFoundError:
        return None


def _save_active_post_id(post_id: str) -> None:
    """Saves a valid, non-empty post ID to the state file."""
    if not post_id:
        logging.error("Attempted to save an empty post ID. Aborting.")
        return
    STATE_FILE.write_text(post_id + "\n", encoding="utf-8")
    logging.info(f"State file '{STATE_FILE}' updated with new post ID: {post_id}")


def _recover_active_post_id(reddit: RedditClient) -> str | None:
    """Recovers the active post ID by finding the latest post on Reddit and
    creating the state file if it's missing or invalid.
    """
    logging.warning("State file is missing or invalid. Attempting to recover from Reddit.")
    latest_posts = reddit.get_bot_submissions(limit=1)

    if not latest_posts:
        logging.error("Recovery failed: Could not find any previous posts by the bot.")
        return None

    latest_post_id = cast(str, latest_posts[0].id)
    if latest_post_id:
        logging.info(f"Recovery successful. Found latest post: {latest_post_id}")
        _save_active_post_id(latest_post_id)
        return latest_post_id

    logging.error("Recovery failed: Found a post but its ID was empty.")
    return None


def _parse_version_from_release(release_data: dict[str, Any]) -> str | None:
    """Parses version from release tag or body, preferring the tag."""
    if not release_data:
        return None
    tag_name = cast(str, release_data.get("tag_name", ""))
    if tag_name and (tag := tag_name.lstrip("v")) and semver.Version.is_valid(tag):
        return tag
    body = cast(str, release_data.get("body", ""))
    if body and (match := re.search(r"v(\d+\.\d+\.\d+)", body)):
        return match.group(1)
    return None


def _parse_version_from_title(title: str) -> str | None:
    """Parses a version string from a Reddit post title."""
    if match := re.search(r"v(\d+\.\d+\.\d+)", title):
        return match.group(1)
    return None


def _get_versions(
    gh: GitHubClient, reddit: RedditClient, config: Config
) -> tuple[semver.Version | None, semver.Version]:
    """Fetch and parse the latest source and posted versions."""
    source_release = gh.get_latest_release(config.github.source_repo)
    source_version_str = _parse_version_from_release(source_release) if source_release else None
    source_version = semver.Version.parse(source_version_str) if source_version_str else None

    latest_reddit_post = reddit.get_bot_submissions(limit=1)
    latest_posted_version_str = "0.0.0"
    if latest_reddit_post:
        title = latest_reddit_post[0].title
        parsed_version = _parse_version_from_title(title)
        if parsed_version:
            latest_posted_version_str = parsed_version
            logging.info(f"Latest post on Reddit is for version: v{parsed_version}")
        else:
            logging.warning(f"Could not parse version from Reddit post title: '{title}'")
    else:
        logging.info("No previous posts found on Reddit.")
    latest_posted_version = semver.Version.parse(latest_posted_version_str)

    return source_version, latest_posted_version


def _manage_github_release(
    gh: GitHubClient,
    config: Config,
    source_version: semver.Version,
    patched_content_bytes: bytes,
) -> dict[str, Any] | None:
    """Manage the GitHub release: create or update, and upload the asset."""
    tag_name = f"v{source_version}"
    release_data = gh.get_release_by_tag(tag_name)

    if release_data:
        logging.info(f"Release {tag_name} already exists. Using it.")
        existing_asset = next(
            (asset for asset in release_data.get("assets", []) if asset["name"] == config.github.asset_file_name),
            None,
        )
        if existing_asset:
            logging.info(f"Asset '{config.github.asset_file_name}' already exists. " "Deleting it first.")
            gh.delete_asset(existing_asset["id"])
    else:
        logging.info(f"Creating new GitHub release: {tag_name}")
        release_title = config.messages.release_title.replace("{{version}}", str(source_version))
        release_body = config.messages.release_description
        release_data = gh.create_release(tag_name, release_title, release_body)

    if not release_data:
        logging.error(f"Failed to get or create release '{tag_name}'.")
        return None

    try:
        logging.info("Uploading patched asset...")
        gh.upload_asset(
            release_data["upload_url"],
            config.github.asset_file_name,
            patched_content_bytes,
        )
    except HTTPError as e:
        logging.critical(f"Failed to upload asset. Status: {e.response.status_code}", exc_info=True)
        return None

    return gh.get_release_by_tag(tag_name)


def _publish_to_reddit(
    reddit: RedditClient,
    config: Config,
    source_version: semver.Version,
    release_data: dict[str, Any],
) -> None:
    """Compose and submit the new post to Reddit, then update old posts."""
    asset_url = release_data["assets"][0]["browser_download_url"]
    # *** FIX STARTS HERE: The corrected line that was too long ***
    initial_status_text = config.feedback.labels.unknown
    initial_status_line = config.feedback.status_line_format.replace("{{status}}", initial_status_text)
    # *** FIX ENDS HERE ***
    post_context = {
        "asset_name": config.github.asset_file_name,
        "version": str(source_version),
        "direct_download_url": asset_url,
        "creator_username": config.reddit.creator,
        "bot_repo": config.github.bot_repo,
        "bot_name": config.reddit.bot_name,
        "initial_status": initial_status_line,
    }
    post_title = config.reddit.post_title.replace("{{version}}", str(source_version)).replace(
        "{{asset_name}}", config.github.asset_file_name
    )
    post_body = reddit._process_template(str(config.reddit.template_file), post_context)

    logging.info(f"Submitting new post to r/{config.reddit.subreddit}...")
    old_posts = reddit.get_bot_submissions(limit=20)
    new_submission = reddit.submit_post(title=post_title, selftext=post_body)
    _save_active_post_id(new_submission.id)

    if old_posts:
        latest_post_details = {
            "version": str(source_version),
            "title": new_submission.title,
            "url": new_submission.shortlink,
        }
        for post in old_posts:
            if post.id != new_submission.id:
                reddit.update_post(post, latest_post_details)


def run_release_and_post(config: Config, gh: GitHubClient, reddit: RedditClient) -> None:
    """The main application function to check, patch, release, and post."""
    logging.info("--- Starting Release & Post Cycle ---")

    source_version, latest_posted_version = _get_versions(gh, reddit, config)

    if not source_version:
        logging.error("Could not determine source version. Aborting.")
        return

    logging.info(f"Source: v{source_version} | Reddit: v{latest_posted_version}")
    if source_version <= latest_posted_version:
        logging.info("Reddit post is up to date. No new release needed.")
        return

    logging.info(f"Newer version v{source_version} found. Proceeding with release.")

    source_release = gh.get_latest_release(config.github.source_repo)
    patched_content_bytes = _download_and_patch_asset(gh, source_release, config)
    if not patched_content_bytes:
        return

    release_data = _manage_github_release(gh, config, source_version, patched_content_bytes)
    if not release_data or not release_data.get("assets"):
        logging.critical("Failed to create release or upload asset. Aborting.")
        return

    _publish_to_reddit(reddit, config, source_version, release_data)

    logging.info("Marking old GitHub releases as outdated...")
    gh.mark_old_releases_outdated()

    logging.info("--- Release & Post Cycle Complete ---")


def _download_and_patch_asset(gh: GitHubClient, source_release: dict[str, Any] | None, config: Config) -> bytes | None:
    """Download the specified asset from the source release and patch it."""
    if not source_release:
        logging.error("Cannot download asset: source release is missing.")
        return None

    asset_to_download = next(
        (asset for asset in source_release.get("assets", []) if asset["name"] == config.github.asset_file_name),
        None,
    )
    if not asset_to_download:
        logging.error("Asset '%s' not found in source release.", config.github.asset_file_name)
        return None

    logging.info("Downloading original asset...")
    original_content_bytes = gh.download_asset(asset_to_download["url"])
    original_content = original_content_bytes.decode("utf-8")

    logging.info("Patching asset content...")
    obfuscated_key = crypto.get_obfuscated_key(crypto.DEFAULT_CIPHER_KEY)
    decrypted_data = crypto.decrypt(original_content, obfuscated_key)
    modified_data = crypto.modify(decrypted_data)
    patched_content = crypto.encrypt(modified_data, obfuscated_key)
    return patched_content.encode("utf-8")


def run_comment_check(config: Config, gh: GitHubClient, reddit: RedditClient) -> None:
    """Checks for comments on the active post and updates status."""
    logging.info("--- Starting Comment Check Cycle ---")
    active_post_id = _get_active_post_id() or _recover_active_post_id(reddit)

    if not active_post_id:
        logging.warning("No active post ID found and could not recover. Skipping comment check.")
        return

    logging.info(f"Performing check on active post: {active_post_id}")
    try:
        submission = reddit.reddit.submission(id=active_post_id)
        submission.comments.replace_more(limit=0)
        comments = submission.comments.list()

        working_kw = re.compile("|".join(config.feedback.working_keywords), re.I)
        not_working_kw = re.compile("|".join(config.feedback.not_working_keywords), re.I)
        positive_score = sum(1 for c in comments if working_kw.search(c.body))
        negative_score = sum(1 for c in comments if not_working_kw.search(c.body))
        logging.info(f"Comment analysis: Positive={positive_score}, Negative={negative_score}")

        threshold = config.feedback.min_feedback_count
        net_score = positive_score - negative_score
        if net_score >= threshold:
            new_status_text = config.feedback.labels.working
        elif net_score <= -threshold:
            new_status_text = config.feedback.labels.broken
        else:
            new_status_text = config.feedback.labels.unknown

        new_status_line = config.feedback.status_line_format.replace("{{status}}", new_status_text)
        status_regex = re.compile(config.feedback.status_line_regex, re.MULTILINE)
        if status_regex.search(submission.selftext) and new_status_line not in submission.selftext:
            updated_body = status_regex.sub(new_status_line, submission.selftext)
            submission.edit(body=updated_body)
            logging.info(f"Post status updated to: '{new_status_text}'")
        else:
            logging.info("Post status is already correct or status line is missing.")

    except Exception as e:
        logging.error(f"An error occurred during comment check: {e}", exc_info=True)

    logging.info("--- Comment Check Cycle Complete ---")
