import os
import sys
import re
from datetime import datetime, timezone, timedelta
from helpers import load_config, load_bot_state, save_bot_state, init_reddit

def main():
    """
    Checks for comments on the active Reddit post, analyzes feedback, and
    updates the post status with an adaptive timer.
    """
    config = load_config()
    state = load_bot_state()
    state_was_meaningfully_updated = False

    active_post_id = state.get("activePostId")
    if not active_post_id:
        print("No active post ID in state file. Exiting pulse.")
        sys.exit(0)

    now = datetime.now(timezone.utc)
    last_check_str = state.get("lastCheckTimestamp", "2000-01-01T00:00:00Z")
    last_check = datetime.fromisoformat(last_check_str.replace("Z", "+00:00"))
    
    current_interval = state.get("currentIntervalSeconds", config["timing"]["firstCheck"])
    if now < (last_check + timedelta(seconds=current_interval)):
        print(f"Not time yet. Next check in {int(((last_check + timedelta(seconds=current_interval)) - now).total_seconds())}s.")
        with open(os.environ.get('GITHUB_OUTPUT', '/dev/null'), 'a') as f:
            print("state_changed=false", file=f)
        sys.exit(0)

    print(f"Time for a real check on post: {active_post_id}")
    try:
        reddit = init_reddit(config)
        submission = reddit.submission(id=active_post_id)
        submission.comments.replace_more(limit=0)
        comments = submission.comments.list()
        
        working_kw = re.compile("|".join(config["feedback"]["workingKeywords"]), re.I)
        not_working_kw = re.compile("|".join(config["feedback"]["notWorkingKeywords"]), re.I)
        positive_score = sum(1 for c in comments if working_kw.search(c.body))
        negative_score = sum(1 for c in comments if not_working_kw.search(c.body))
        net_score = positive_score - negative_score
        print(f"Comment analysis: Positive={positive_score}, Negative={negative_score}, Net Score={net_score}")
        
        threshold = config["feedback"]["minFeedbackCount"]
        if net_score <= -threshold:
            new_status_text = config["feedback"]["labels"]["broken"]
        elif net_score >= threshold:
            new_status_text = config["feedback"]["labels"]["working"]
        else:
            new_status_text = config["feedback"]["labels"]["unknown"]
            
        new_status_line = config["feedback"]["statusLineFormat"].replace("{{status}}", new_status_text)
        
        status_regex = re.compile(config["feedback"]["statusLineRegex"], re.MULTILINE)
        if not status_regex.search(submission.selftext):
            print("::warning::Could not find status line in post. It may have been edited or is an outdated post.")
        elif new_status_line not in submission.selftext:
            updated_body = status_regex.sub(new_status_line, submission.selftext)
            submission.edit(body=updated_body)
            print(f"Status updated to: {new_status_text}")
        else:
            print("Status is already correct.")

        last_comment_count = state.get("lastCommentCount", 0)
        if len(comments) > last_comment_count:
            state["currentIntervalSeconds"] = config["timing"]["firstCheck"]
            state_was_meaningfully_updated = True
        else:
            if current_interval < config["timing"]["maxWait"]:
                state["currentIntervalSeconds"] = min(config["timing"]["maxWait"], current_interval + config["timing"]["increaseBy"])
                state_was_meaningfully_updated = True

        if last_comment_count != len(comments):
            state["lastCommentCount"] = len(comments)
            state_was_meaningfully_updated = True

    except Exception as e:
        print(f"::error::An exception occurred during check: {e}", file=sys.stderr)
    finally:
        state["lastCheckTimestamp"] = now.isoformat().replace("+00:00", "Z")
        if state_was_meaningfully_updated:
            print("Meaningful state change detected. Saving state file.")
            save_bot_state(state)
        else:
            print("No meaningful state change detected. Skipping file write.")

        with open(os.environ.get('GITHUB_OUTPUT', '/dev/null'), 'a') as f:
            print(f"state_changed={str(state_was_meaningfully_updated).lower()}", file=f)
        print(f"Pulse check complete. Next interval: {state.get('currentIntervalSeconds', config['timing']['firstCheck'])}s")

if __name__ == "__main__":
    main()