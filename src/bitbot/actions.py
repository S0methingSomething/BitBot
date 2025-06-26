import json
import logging
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict

import semver

from .clients import GitHubClient, RedditClient
from .config import BotState, Config
from .core import patch_monetization_vars

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def _render_template(template_name: str, context: Dict[str, Any], config: Config) -> str:
    """Loads and renders a template from the templates directory."""
    try:
        template_path = Path(__file__).parent / "templates" / template_name
        raw_template = template_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        logging.error(f"Template file not found: {template_path}")
        raise

    # Remove tutorial block
    start_tag = config.skipContent["startTag"]
    end_tag = config.skipContent["endTag"]
    if start_tag and end_tag and start_tag in raw_template:
        pattern = re.compile(f"{re.escape(start_tag)}.*?{re.escape(end_tag)}", re.DOTALL)
        content = re.sub(pattern, "", raw_template).strip()
    else:
        content = raw_template

    # Replace placeholders
    for placeholder, value in context.items():
        content = content.replace(f"{{{{{placeholder}}}}}", str(value))
    return content


def _parse_version_from_release(release_data: Dict[str, Any]) -> str | None:
    """Parses version from release tag or body, preferring tag."""
    if not release_data: return None
    tag = release_data.get("tag_name", "").lstrip("v")
    if semver.Version.is_valid(tag):
        return tag

    body = release_data.get("body", "")
    match = re.search(r"v(\d+\.\d+\.\d+)", body)
    if match:
        return match.group(1)
    return None


def run_release_and_post(config: Config, gh: GitHubClient, reddit: RedditClient) -> None:
    """The main application function to check, patch, release, and post."""
    logging.info("--- Starting Release & Post Cycle ---")

    # 1. Get latest source and bot releases
    try:
        source_release = gh.get_latest_release(config.github.sourceRepo)
        if not source_release:
             logging.error(f"Could not fetch latest release from source repo: {config.github.sourceRepo}")
             return
        source_version_str = _parse_version_from_release(source_release)
        if not source_version_str:
            logging.error(f"Could not parse a valid version from source repo release '{source_release.get('name')}'.")
            return
        source_version = semver.Version.parse(source_version_str)

        bot_release = gh.get_latest_release(config.github.botRepo)
        bot_version_str = _parse_version_from_release(bot_release) if bot_release else "0.0.0"
        bot_version = semver.Version.parse(bot_version_str)
    except Exception as e:
        logging.error(f"Failed to fetch initial release data: {e}", exc_info=True)
        return

    logging.info(f"Source repo version: {source_version} | Bot repo version: {bot_version}")

    # 2. Compare versions
    if source_version <= bot_version:
        logging.info("Bot is up to date. No new release needed.")
        return

    logging.info(f"New version found: {source_version}. Proceeding with release.")

    # 3. Download and patch the asset
    asset_to_download = next(
        (asset for asset in source_release.get("assets", []) if asset["name"] == config.github.assetFileName), None
    )
    if not asset_to_download:
        logging.error(f"Asset '{config.github.assetFileName}' not found in source release.")
        return

    logging.info("Downloading original asset...")
    original_content_bytes = gh.download_asset(asset_to_download["url"])
    original_content = original_content_bytes.decode("utf-8")

    logging.info("Patching asset content...")
    patched_content = patch_monetization_vars(original_content)
    patched_content_bytes = patched_content.encode("utf-8")

    # 4. Create new GitHub release in bot repo
    tag_name = f"v{source_version}"
    release_title = config.messages["releaseTitle"].replace("{{asset_name}}", config.github.assetFileName).replace("{{version}}", str(source_version))
    release_body = config.messages["releaseDescription"].replace("{{asset_name}}", config.github.assetFileName)

    logging.info(f"Creating new GitHub release: {release_title}")
    new_release_data = gh.create_release(tag_name, release_title, release_body)
    upload_url = new_release_data["upload_url"]

    logging.info("Uploading patched asset...")
    gh.upload_asset(upload_url, config.github.assetFileName, patched_content_bytes)
    # Refetch release data to get the asset URL
    new_release_data = gh.get_latest_release(config.github.botRepo)


    # 5. Post to Reddit
    logging.info("Preparing to post to Reddit...")
    direct_download_url = new_release_data["assets"][0]["browser_download_url"]

    # Get old Reddit posts before creating new one
    old_posts = reddit.get_bot_submissions(limit=20)
    
    # Create the new post
    post_context = {
        "asset_name": config.github.assetFileName,
        "version": source_version,
        "direct_download_url": direct_download_url,
        "creator_username": config.reddit.creator,
        "bot_repo": config.github.botRepo,
        "bot_name": config.reddit.botName,
        "initial_status": config.messages["statusLine"].replace("{{status}}", config.feedback.labels["unknown"]),
    }
    post_title_template = config.messages["postTitle"]
    post_title = post_title_template.replace("{{asset_name}}", post_context["asset_name"]).replace("{{version}}", str(post_context["version"]))
    post_body = _render_template(config.templates["post"], post_context, config)
    
    logging.info(f"Submitting new post to r/{config.reddit.subreddit}...")
    new_submission = reddit.submit_post(title=post_title, selftext=post_body)
    
    # Update state to monitor new post
    new_state = BotState(
        activePostId=new_submission.id,
        lastCheckTimestamp=datetime.now(timezone.utc).isoformat(),
        currentIntervalSeconds=config.timing.firstCheck,
        lastCommentCount=0,
    )
    gh.save_state(new_state)
    logging.info(f"State updated to monitor new post: {new_submission.id}")

    # Now update old posts
    if old_posts:
        logging.info(f"Updating {len(old_posts)} old Reddit post(s)...")
        latest_post_details = {
            "latest_post_title": new_submission.title,
            "latest_post_url": new_submission.shortlink,
            "latest_version": source_version,
            "asset_name": config.github.assetFileName
        }
        outdated_mode = config.outdatedPostHandling['mode']
        template_name = config.templates.get(outdated_mode)
        if not template_name:
            logging.error(f"Outdated post template for mode '{outdated_mode}' not found in config.templates")
            return
            
        outdated_content = _render_template(template_name, latest_post_details, config)

        for post in old_posts:
            if "⚠️ Outdated Post" not in post.selftext and "This Post is Outdated" not in post.selftext:
                if outdated_mode == 'inject':
                    new_body = f"{outdated_content}\n\n---\n\n{post.selftext}"
                else: # overwrite
                    new_body = outdated_content
                
                try:
                    post.edit(body=new_body)
                    logging.info(f"-> Updated old post {post.id}")
                except Exception as e:
                    logging.warning(f"Failed to edit post {post.id}: {e}")

    # 6. Mark old GitHub releases as [OUTDATED]
    logging.info("Marking old GitHub releases as outdated...")
    gh.mark_old_releases_outdated()
    
    logging.info("--- Release & Post Cycle Complete ---")


def run_comment_check(config: Config, gh: GitHubClient, reddit: RedditClient) -> None:
    """Checks for comments on the active post and updates status."""
    logging.info("--- Starting Comment Check Cycle ---")
    state = gh.load_state()

    if not state or not state.activePostId:
        logging.warning("No active post ID found in state. Skipping comment check.")
        return

    now = datetime.now(timezone.utc)
    last_check_time = datetime.fromisoformat(state.lastCheckTimestamp)
    next_check_time = last_check_time + timedelta(seconds=state.currentIntervalSeconds)

    if now < next_check_time:
        wait_seconds = (next_check_time - now).total_seconds()
        logging.info(f"Not time for a full check yet. Next check in {int(wait_seconds)}s.")
        return

    logging.info(f"Performing check on active post: {state.activePostId}")
    try:
        submission = reddit.reddit.submission(id=state.activePostId)
        submission.comments.replace_more(limit=0)
        comments = submission.comments.list()

        working_kw = re.compile("|".join(config.feedback.workingKeywords), re.I)
        not_working_kw = re.compile("|".join(config.feedback.notWorkingKeywords), re.I)
        positive_score = sum(1 for c in comments if working_kw.search(c.body))
        negative_score = sum(1 for c in comments if not_working_kw.search(c.body))
        net_score = positive_score - negative_score
        logging.info(f"Comment analysis: Positive={positive_score}, Negative={negative_score}")
        
        threshold = config.feedback.minFeedbackCount
        if net_score >= threshold:
            new_status_text = config.feedback.labels["working"]
        elif net_score <= -threshold:
            new_status_text = config.feedback.labels["broken"]
        else:
            new_status_text = config.feedback.labels["unknown"]

        new_status_line = config.messages["statusLine"].replace("{{status}}", new_status_text)
        
        status_regex = re.compile(config.feedback.statusLineRegex, re.MULTILINE)
        if not status_regex.search(submission.selftext):
            logging.warning("Could not find status line in the post. It may have been edited.")
        elif new_status_line not in submission.selftext:
            updated_body = status_regex.sub(new_status_line, submission.selftext)
            submission.edit(body=updated_body)
            logging.info(f"Post status updated to: '{new_status_text}'")
        else:
            logging.info("Post status is already correct.")
            
        # Update state object
        state.lastCheckTimestamp = now.isoformat()
        if len(comments) > state.lastCommentCount: # New comments arrived
            state.currentIntervalSeconds = config.timing.firstCheck
        else: # No new comments, increase wait time
            state.currentIntervalSeconds = min(
                config.timing.maxWait,
                state.currentIntervalSeconds + config.timing.increaseBy
            )
        state.lastCommentCount = len(comments)
        
        gh.save_state(state)
        logging.info(f"State saved. Next check interval: {state.currentIntervalSeconds}s")

    except Exception as e:
        logging.error(f"An error occurred during comment check: {e}", exc_info=True)

    logging.info("--- Comment Check Cycle Complete ---")
