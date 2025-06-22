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
    Main execution function. Checks for comments on the active Reddit post,
    analyzes feedback, and updates the post status with an adaptive timer.
    """
    config = load_config()
    state = load_state()

    if not state.get("activePostId"):
        print("No active post ID in state file. Exiting pulse.")
        sys.exit(0)

    # Implement adaptive timing to avoid excessive API calls
    now = datetime.now(timezone.utc)
    last_check = datetime.fromisoformat(state["lastCheckTimestamp"].replace("Z", "+00:00"))
    if now < (last_check + timedelta(seconds=state["currentIntervalSeconds"])):
        print(f"Not time yet. Next check in {int((last_check + timedelta(seconds=state['currentIntervalSeconds'])) - now).total_seconds())}s.")
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
        
        # Analyze comments based on keywords from config
        working_kw = re.compile("|".join(config["feedback"]["workingKeywords"]), re.I)
        not_working_kw = re.compile("|".join(config["feedback"]["notWorkingKeywords"]), re.I)
        positive_score = sum(1 for c in comments if working_kw.search(c.body))
        negative_score = sum(1 for c in comments if not_working_kw.search(c.body))
        net_score = positive_score - negative_score
        
        print(f"Comment analysis: Positive={positive_score}, Negative={negative_score}, Net Score={net_score}")
        
        # Determine new status based on score and threshold
        threshold = config["feedback"]["minFeedbackCount"]
        if net_score <= -threshold:
            new_status_text = config["feedback"]["labels"]["broken"]
        elif net_score >= threshold:
            new_status_text = config["feedback"]["labels"]["working"]
        else:
            new_status_text = config["feedback"]["labels"]["unknown"]
            
        new_status_line = config["feedback"]["statusLineFormat"].replace("{{status}}", new_status_text)
        
        # Update the post body if the status has changed
        status_regex = re.compile(config["feedback"]["statusLineRegex"], re.MULTILINE)
        if not status_regex.search(submission.selftext):
            print("::warning::Could not find status line in post. It may have been edited or is an outdated post.")
        elif new_status_line not in submission.selftext:
            updated_body = status_regex.sub(new_status_line, submission.selftext)
            submission.edit(body=updated_body)
            print(f"Status updated to: {new_status_text}")
        else:
            print("Status is already correct.")

        # Adjust the next check interval based on comment activity
        if len(comments) > state["lastCommentCount"]:
            state["currentIntervalSeconds"] = config["timing"]["firstCheck"]
        else:
            state["currentIntervalSeconds"] = min(config["timing"]["maxWait"], state["currentIntervalSeconds"] + config["timing"]["increaseBy"])
        state["lastCommentCount"] = len(comments)

    except Exception as e:
        print(f"::error::An exception occurred during check: {e}", file=sys.stderr)
    finally:
        # Always save the state, even on failure, to update the timestamp
        state["lastCheckTimestamp"] = now.isoformat().replace("+00:00", "Z")
        save_state(state)
        print(f"State saved. Next interval: {state['currentIntervalSeconds']}s")

if __name__ == "__main__":
    main()            positive_score += 1

    net_score = positive_score - negative_score
    print(f"Comment analysis: Positive={positive_score}, Negative={negative_score}, Net Score={net_score}")
    
    if net_score <= -THRESHOLD:
        new_status = STATUS_NOT_WORKING
    elif net_score >= THRESHOLD:
        new_status = STATUS_WORKING
    else:
        new_status = STATUS_NEUTRAL
        
    status_line = f"**Current Status (based on comments):** {new_status}"
    
    if status_line not in submission.selftext:
        submission.edit(body=re.sub(r"(\*\*Current Status.*\*\*).*$", status_line, submission.selftext, flags=re.DOTALL))
        print(f"Status updated to: {new_status}")
    else:
        print("Status is already correct.")

    if len(comments) > state["lastCommentCount"]:
        state["currentIntervalSeconds"] = INITIAL_INTERVAL_S
    else:
        state["currentIntervalSeconds"] = min(MAX_INTERVAL_S, state["currentIntervalSeconds"] + INCREMENT_INTERVAL_S)
    state["lastCommentCount"] = len(comments)

except Exception as e:
    print(f"::error::An exception occurred during check: {e}")
finally:
    state["lastCheckTimestamp"] = now.isoformat().replace("+00:00", "Z")
    save_state(state)
    print(f"State saved. Next interval: {state['currentIntervalSeconds']}s")
