import os
import sys
import json
import re
import praw
from datetime import datetime, timezone, timedelta

def load_config():
    """Loads the main configuration file."""
    with open("config.json", "r") as f:
        return json.load(f)

def load_state():
    """Loads the bot's current monitoring state."""
    with open("bot_state.json", "r") as f:
        return json.load(f)

def save_state(data):
    """Saves the bot's monitoring state."""
    with open("bot_state.json", "w") as f:
        json.dump(data, f, indent=2)

def main():
    """
    Checks for comments on the active Reddit post, analyzes feedback, and
    updates the post status with an adaptive timer.
    """
    config = load_config()
    state = load_state()
    state_was_meaningfully_updated = False

    if not state.get("activePostId"):
        print("No active post ID in state file. Exiting pulse.")
        sys.exit(0)

    now = datetime.now(timezone.utc)
    last_check = datetime.fromisoformat(state["lastCheckTimestamp"].replace("Z", "+00:00"))
    
    if now < (last_check + timedelta(seconds=state["currentIntervalSeconds"])):
        # Corrected line with fixed parenthesis placement.
        print(f"Not time yet. Next check in {int(((last_check + timedelta(seconds=state['currentIntervalSeconds'])) - now).total_seconds())}s.")
        with open(os.environ.get('GITHUB_OUTPUT', '/dev/null'), 'a') as f:
            print("state_changed=false", file=f)
        sys.exit(0)

    print(f"Time for a real check on post: {state['activePostId']}")
    try:
        reddit = praw.Reddit(
            client_id=os.environ["REDDIT_CLIENT_ID"],
            client_secret=os.environ["REDDIT_CLIENT_SECRET"],
            user_agent=os.environ["REDDIT_USER_AGENT"],
            username=os.environ["REDDIT_USERNAME"],
            password=os.environ["REDDIT_PASSWORD"],
        )
        submission = reddit.submission(id=state["activePostId"])
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

        if len(comments) > state["lastCommentCount"]:
            state["currentIntervalSeconds"] = config["timing"]["firstCheck"]
            state_was_meaningfully_updated = True
        else:
            if state["currentIntervalSeconds"] < config["timing"]["maxWait"]:
                state["currentIntervalSeconds"] = min(config["timing"]["maxWait"], state["currentIntervalSeconds"] + config["timing"]["increaseBy"])
                state_was_meaningfully_updated = True

        if state["lastCommentCount"] != len(comments):
            state["lastCommentCount"] = len(comments)
            state_was_meaningfully_updated = True

    except Exception as e:
        print(f"::error::An exception occurred during check: {e}", file=sys.stderr)
    finally:
        state["lastCheckTimestamp"] = now.isoformat().replace("+00:00", "Z")
        if state_was_meaningfully_updated:
            print("Meaningful state change detected. Saving state file.")
            save_state(state)
        else:
            print("No meaningful state change detected. Skipping file write.")

        with open(os.environ.get('GITHUB_OUTPUT', '/dev/null'), 'a') as f:
            print(f"state_changed={str(state_was_meaningfully_updated).lower()}", file=f)
        print(f"Pulse check complete. Next interval: {state['currentIntervalSeconds']}s")

if __name__ == "__main__":
    main()
