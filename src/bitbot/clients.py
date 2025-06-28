import logging
import re
from pathlib import Path
from typing import Any, cast

import semver
from praw.models import Submission

from .clients import GitHubClient, RedditClient
from .config import Config
from .core import patch_monetization_vars

STATE_FILE = Path("latest_postid.txt")

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def _get_active_post_id() -> str | None:
    """
    Reads the active post ID from the state file.
    Returns None if the file is missing, empty, or contains only whitespace.
    """
    try:
        content = STATE_FILE.read_text(encoding="utf-8").strip()
        if content:  # Explicitly check if the string is not empty
            return content
        # If content is empty or just whitespace, treat it as invalid
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
    """
    Recovers the active post ID by finding the latest post on Reddit and
    creating the state file if it's missing or invalid.
    """
    logging.warning(
        "State file is missing or invalid. Attempting to recover from Reddit."
    )
    latest_posts = reddit.get_bot_submissions(limit=1)

    if not latest_posts:
        logging.error("Recovery failed: Could not find any previous posts by the bot.")
        return None

    # Use cast to inform mypy that submission.id is a string
    latest_post_id = cast(str, latest_posts[0].id)
    if latest_post_id:
        logging.info(f"Recovery successful. Found latest post: {latest_post_id}")
        _save_active_post_id(latest_post_id)
        return latest_post_id

    logging.error("Recovery failed: Found a post but its ID was empty.")
    return None


def _render_template(
    template_name: str, context: dict[str, Any], config: Config
) -> str:
    """Loads and renders a template from the templates directory."""
    try:
        template_path = Path(__file__).parent / "templates" / template_name
        raw_template = template_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        logging.error(f"Template file not found: {template_path}")
        raise

    start_tag = config.skip_content["startTag"]
    end_tag = config.skip_content["endTag"]
    if start_tag and end_tag and start_tag in raw_template:
        pattern = re.compile(
            f"{re.escape(start_tag)}.*?{re.escape(end_tag)}", re.DOTALL
        )
        content = re.sub(pattern, "", raw_template).strip()
    else:
        content = raw_template

    for placeholder, value in context.items():
        content = content.replace(f"{{{{{placeholder}}}}}", str(value))
    return content


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


def run_release_and_post(
    config: Config, gh: GitHubClient, reddit: RedditClient
) -> None:
    """The main application function to check, patch, release, and post."""
    logging.info("--- Starting Release & Post Cycle ---")

    # 1. Get the latest version from the source repository (the source of truth)
    source_release = gh.get_latest_release(config.github.source_repo)
    if not source_release:
        logging.error(
            "Could not fetch latest release from source repo: %s",
            config.github.source_repo,
        )
        return
    source_version_str = _parse_version_from_release(source_release)
    if not source_version_str:
        logging.error(
            "Could not parse valid version from source release '%s'.",
            source_release.get("name"),
        )
        return
    source_version = semver.Version.parse(source_version_str)

    # 2. Get the version of the last successful post from Reddit
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

    # 3. CORE DECISION: Only proceed if the source version is newer than what's on Reddit
    logging.info(f"Source: v{source_version} | Reddit: v{latest_posted_version}")
    if source_version <= latest_posted_version:
        logging.info("Reddit post is up to date. No new release needed.")
        return

    logging.info(f"Newer version v{source_version} found. Proceeding with release.")

    # 4. Download and patch the asset
    patched_content_bytes = _download_and_patch_asset(gh, source_release, config)
    if not patched_content_bytes:
        return

    # 5. Create or get the GitHub release for the new version
    tag_name = f"v{source_version}"
    release_title = (
        config.messages["releaseTitle"]
        .replace("{{asset_name}}", config.github.asset_file_name)
        .replace("{{version}}", str(source_version))
    )
    release_body = config.messages["releaseDescription"].replace(
        "{{asset_name}}", config.github.asset_file_name
    )

    release_data = gh.get_release_by_tag(tag_name)
    if release_data:
        logging.info(f"Release {tag_name} already exists. Using it.")
    else:
        logging.info(f"Creating new GitHub release: {release_title}")
        release_data = gh.create_release(tag_name, release_title, release_body)

    # 6. Delete existing asset if it exists, then upload the new one.
    existing_asset = next(
        (
            asset
            for asset in release_data.get("assets", [])
            if asset["name"] == config.github.asset_file_name
        ),
        None,
    )
    if existing_asset:
        logging.info(
            f"Asset '{config.github.asset_file_name}' already exists. Deleting it first."
        )
        gh.delete_asset(existing_asset["id"])

    logging.info("Uploading patched asset...")
    gh.upload_asset(
        release_data["upload_url"],
        config.github.asset_file_name,
        patched_content_bytes,
    )
    refetched_release = gh.get_release_by_tag(tag_name)
    if not refetched_release or not refetched_release.get("assets"):
        logging.error("CRITICAL: Failed to refetch release or find asset after upload.")
        return

    # 7. Post the new version to Reddit
    logging.info("Preparing to post to Reddit...")
    direct_download_url = refetched_release["assets"][0]["browser_download_url"]
    old_posts = reddit.get_bot_submissions(limit=20)

    post_context = {
        "asset_name": config.github.asset_file_name,
        "version": source_version,
        "direct_download_url": direct_download_url,
        "creator_username": config.reddit.creator,
        "bot_repo": config.github.bot_repo,
        "bot_name": config.reddit.bot_name,
        "initial_status": config.messages["statusLine"].replace(
            "{{status}}", config.feedback.labels["unknown"]
        ),
    }
    post_title = (
        config.messages["postTitle"]
        .replace("{{asset_name}}", post_context["asset_name"])
        .replace("{{version}}", str(post_context["version"]))
    )
    post_body = _render_template(config.templates["post"], post_context, config)

    logging.info(f"Submitting new post to r/{config.reddit.subreddit}...")
    new_submission = reddit.submit_post(title=post_title, selftext=post_body)
    _save_active_post_id(new_submission.id)

    # 8. Update old posts and releases
    _update_old_reddit_posts(old_posts, new_submission, config)
    logging.info("Marking old GitHub releases as outdated...")
    gh.mark_old_releases_outdated()

    logging.info("--- Release & Post Cycle Complete ---")


def _download_and_patch_asset(
    gh: GitHubClient, source_release: dict[str, Any], config: Config
) -> bytes | None:
    """Download the specified asset from the source release and patch it."""
    asset_to_download = next(
        (
            asset
            for asset in source_release.get("assets", [])
            if asset["name"] == config.github.asset_file_name
        ),
        None,
    )
    if not asset_to_download:
        logging.error(
            "Asset '%s' not found in source release.", config.github.asset_file_name
        )
        return None

    logging.info("Downloading original asset...")
    original_content_bytes = gh.download_asset(asset_to_download["url"])
    original_content = original_content_bytes.decode("utf-8")

    logging.info("Patching asset content...")
    patched_content = patch_monetization_vars(original_content)
    return patched_content.encode("utf-8")


def _update_old_reddit_posts(
    old_posts: list[Submission], new_submission: Submission, config: Config
) -> None:
    """Find and update old Reddit posts to point to the new one."""
    if not old_posts:
        return

    logging.info(f"Updating {len(old_posts)} old Reddit post(s)...")
    latest_post_details = {
        "latest_post_title": new_submission.title,
        "latest_post_url": new_submission.shortlink,
        "latest_version": str(new_submission.title).split(" v")[-1],
        "asset_name": config.github.asset_file_name,
    }
    outdated_mode = config.outdated_post_handling["mode"]
    template_name = config.templates.get(outdated_mode)

    if not template_name:
        logging.error(f"Template for outdated mode '{outdated_mode}' not in config.")
        return

    outdated_content = _render_template(template_name, latest_post_details, config)

    for post in old_posts:
        if (
            post.id != new_submission.id
            and "⚠️ Outdated Post" not in post.selftext
            and "This Post is Outdated" not in post.selftext
        ):
            new_body = (
                f"{outdated_content}\n\n---\n\n{post.selftext}"
                if outdated_mode == "inject"
                else outdated_content
            )
            try:
                post.edit(body=new_body)
                logging.info(f"-> Updated old post {post.id}")
            except Exception as e:
                logging.warning(f"Failed to edit post {post.id}: {e}")


def run_comment_check(config: Config, gh: GitHubClient, reddit: RedditClient) -> None:
    """Checks for comments on the active post and updates status."""
    logging.info("--- Starting Comment Check Cycle ---")
    active_post_id = _get_active_post_id()

    # This condition now handles missing file, empty file, and whitespace-only file
    if not active_post_id:
        active_post_id = _recover_active_post_id(reddit)

    if not active_post_id:
        # If still no ID after recovery attempt, then we must exit.
        logging.warning(
            "No active post ID found and could not recover. Skipping comment check."
        )
        return

    logging.info(f"Performing check on active post: {active_post_id}")
    try:
        submission = reddit.reddit.submission(id=active_post_id)
        submission.comments.replace_more(limit=0)
        comments = submission.comments.list()

        working_kw = re.compile("|".join(config.feedback.working_keywords), re.I)
        not_working_kw = re.compile(
            "|".join(config.feedback.not_working_keywords), re.I
        )
        positive_score = sum(1 for c in comments if working_kw.search(c.body))
        negative_score = sum(1 for c in comments if not_working_kw.search(c.body))
        net_score = positive_score - negative_score
        logging.info(
            f"Comment analysis: Positive={positive_score}, Negative={negative_score}"
        )

        threshold = config.feedback.min_feedback_count
        if net_score >= threshold:
            new_status_text = config.feedback.labels["working"]
        elif net_score <= -threshold:
            new_status_text = config.feedback.labels["broken"]
        else:
            new_status_text = config.feedback.labels["unknown"]

        new_status_line = config.messages["statusLine"].replace(
            "{{status}}", new_status_text
        )

        status_regex = re.compile(config.feedback.status_line_regex, re.MULTILINE)
        if not status_regex.search(submission.selftext):
            logging.warning(
                "Could not find status line in the post. It may have been edited."
            )
        elif new_status_line not in submission.selftext:
            updated_body = status_regex.sub(new_status_line, submission.selftext)
            submission.edit(body=updated_body)
            logging.info(f"Post status updated to: '{new_status_text}'")
        else:
            logging.info("Post status is already correct.")

    except Exception as e:
        logging.error(f"An error occurred during comment check: {e}", exc_info=True)

    logging.info("--- Comment Check Cycle Complete ---")
