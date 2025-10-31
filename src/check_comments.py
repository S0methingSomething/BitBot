"""Monitor Reddit comments and update post status based on feedback."""

import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from beartype import beartype

from core.config import load_config
from core.credentials import Credentials
from core.state import load_bot_state, save_bot_state
from reddit.client import init_reddit


@beartype  # type: ignore[misc]
def main() -> None:  # noqa: C901, PLR0912, PLR0915
    """Check comments on the active Reddit post and analyze feedback.

    Updates the post status using an adaptive timer to check comments at
    increasing intervals.
    """
    config = load_config()
    state = load_bot_state()
    state_was_meaningfully_updated = False

    active_post_id = state.get("activePostId")
    if not active_post_id:
        sys.exit(0)

    now = datetime.now(timezone.utc)
    last_check_str = state.get("lastCheckTimestamp", "2000-01-01T00:00:00Z")
    last_check = datetime.fromisoformat(last_check_str.replace("Z", "+00:00"))

    current_interval = state.get("currentIntervalSeconds", config["timing"]["firstCheck"])
    if now < (last_check + timedelta(seconds=current_interval)):
        with Path(Credentials.get_github_output() or "/dev/null").open("a") as f:
            print("state_changed=false", file=f)
        sys.exit(0)

    try:
        reddit = init_reddit(config)
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
        if not status_regex.search(submission.selftext):
            pass
        elif new_status_line not in submission.selftext:
            updated_body = status_regex.sub(new_status_line, submission.selftext)
            submission.edit(body=updated_body)
        else:
            pass

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

    except Exception:  # noqa: BLE001, S110
        pass
    finally:
        state["lastCheckTimestamp"] = now.isoformat().replace("+00:00", "Z")
        if state_was_meaningfully_updated:
            save_bot_state(state)
        else:
            pass

        with Path(Credentials.get_github_output() or "/dev/null").open("a") as f:
            print(f"state_changed={str(state_was_meaningfully_updated).lower()}", file=f)


if __name__ == "__main__":
    main()
