"""Monitor Reddit comments and update post status based on feedback."""

import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

import deal
from beartype import beartype

from core.config import load_config
from core.credentials import Credentials
from core.errors import BitBotError, RedditAPIError
from core.result import Err, Ok, Result
from core.state import load_bot_state, save_bot_state
from reddit.client import init_reddit


@beartype  # type: ignore[misc]
def main() -> Result[None, BitBotError]:  # noqa: C901, PLR0912, PLR0915
    """Check comments on the active Reddit post and analyze feedback."""
    config_result = load_config()
    if config_result.is_err():
        return config_result
    config = config_result.unwrap()
    
    state_result = load_bot_state()
    if state_result.is_err():
        return state_result
    state = state_result.unwrap()
    
    state_was_meaningfully_updated = False

    active_post_id = state.get("activePostId")
    if not active_post_id:
        _write_github_output(False)
        return Ok(None)

    now = datetime.now(timezone.utc)
    last_check_str = state.get("lastCheckTimestamp", "2000-01-01T00:00:00Z")
    last_check = datetime.fromisoformat(last_check_str.replace("Z", "+00:00"))

    current_interval = state.get("currentIntervalSeconds", config["timing"]["firstCheck"])
    if now < (last_check + timedelta(seconds=current_interval)):
        _write_github_output(False)
        return Ok(None)

    reddit_result = init_reddit(config)
    if reddit_result.is_err():
        return reddit_result
    reddit = reddit_result.unwrap()
    
    try:
        submission = reddit.submission(id=active_post_id)
        submission.comments.replace_more(limit=0)
        comments = submission.comments.list()

        working_kw = re.compile("|".join(config["feedback"]["workingKeywords"]), re.IGNORECASE)
        not_working_kw = re.compile(
            "|".join(config["feedback"]["notWorkingKeywords"]), re.IGNORECASE
        )
        positive_score = sum(1 for c in comments if working_kw.search(c.body))
        negative_score = sum(1 for c in comments if not_working_kw.search(c.body))
        net_score = positive_score - negative_score

        threshold = config["feedback"]["minFeedbackCount"]
        if net_score <= -threshold:
            new_status_text = config["feedback"]["labels"]["broken"]
        elif net_score >= threshold:
            new_status_text = config["feedback"]["labels"]["working"]
        else:
            new_status_text = config["feedback"]["labels"]["unknown"]

        new_status_line = config["feedback"]["statusLineFormat"].replace(
            "{{status}}", new_status_text
        )

        status_regex = re.compile(config["feedback"]["statusLineRegex"], re.MULTILINE)
        if status_regex.search(submission.selftext) and new_status_line not in submission.selftext:
            updated_body = status_regex.sub(new_status_line, submission.selftext)
            submission.edit(body=updated_body)

        last_comment_count = state.get("lastCommentCount", 0)
        if len(comments) > last_comment_count:
            state["currentIntervalSeconds"] = config["timing"]["firstCheck"]
            state_was_meaningfully_updated = True
        elif current_interval < config["timing"]["maxWait"]:
            state["currentIntervalSeconds"] = min(
                config["timing"]["maxWait"], current_interval + config["timing"]["increaseBy"]
            )
            state_was_meaningfully_updated = True

        if last_comment_count != len(comments):
            state["lastCommentCount"] = len(comments)
            state_was_meaningfully_updated = True

    except Exception as e:  # noqa: BLE001
        return Err(RedditAPIError(f"Failed to check comments: {e}"))
    finally:
        state["lastCheckTimestamp"] = now.isoformat().replace("+00:00", "Z")
        if state_was_meaningfully_updated:
            save_result = save_bot_state(state)
            if save_result.is_err():
                return save_result
        _write_github_output(state_was_meaningfully_updated)

    return Ok(None)


@beartype  # type: ignore[misc]
def _write_github_output(state_changed: bool) -> None:
    """Write state_changed to GitHub Actions output."""
    output_file = Credentials.get_github_output()
    if output_file:
        with Path(output_file).open("a") as f:
            f.write(f"state_changed={str(state_changed).lower()}\n")


if __name__ == "__main__":
    result = main()
    if result.is_err():
        print(f"Error: {result.error.message}")  # noqa: T201
        raise SystemExit(1)
