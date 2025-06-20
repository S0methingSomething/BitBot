import os
import json
import sys
import re
import requests
import praw
from datetime import datetime, timezone, timedelta

# --- Load Configuration ---
with open("config.json", "r") as f:
    config = json.load(f)
STATE_FILE = "bot_state.json"
GITHUB_REPO = config["botRepo"]
STATUS_WORKING = config["status"]["workingText"]
STATUS_NOT_WORKING = config["status"]["notWorkingText"]
STATUS_NEUTRAL = config["status"]["neutralText"]
WORKING_KEYWORDS_PATTERN = re.compile("|".join(config["status"]["workingKeywords"]), re.I)
NOT_WORKING_KEYWORDS_PATTERN = re.compile("|".join(config["status"]["notWorkingKeywords"]), re.I)
THRESHOLD = config["status"]["threshold"]
INITIAL_INTERVAL_S = config["intervals"]["initialSeconds"]
MAX_INTERVAL_S = config["intervals"]["maxSeconds"]
INCREMENT_INTERVAL_S = config["intervals"]["incrementSeconds"]

def load_state():
    with open(STATE_FILE, "r") as f:
        return json.load(f)

def save_state(data):
    with open(STATE_FILE, "w") as f:
        json.dump(data, f, indent=2)

# --- Main Logic ---
state = load_state()
if not state["postId"] or state["postId"] == "null":
    print("No active post ID in state file. Exiting pulse.")
    sys.exit(0)

now = datetime.now(timezone.utc)
last_check = datetime.fromisoformat(state["lastCheckTimestamp"].replace("Z", "+00:00"))

if now < (last_check + timedelta(seconds=state["currentIntervalSeconds"])):
    print("Not time yet. Exiting pulse.")
    sys.exit(0)

print("Time for a real check.")
try:
    reddit = praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        user_agent=os.environ["REDDIT_USER_AGENT"],
        username=os.environ["REDDIT_USERNAME"],
        password=os.environ["REDDIT_PASSWORD"],
    )
    submission = reddit.submission(id=state["postId"])
    submission.comments.replace_more(limit=0)
    comments = submission.comments.list()
    
    positive_score = 0
    negative_score = 0
    for c in comments:
        if NOT_WORKING_KEYWORDS_PATTERN.search(c.body):
            negative_score += 1
        elif WORKING_KEYWORDS_PATTERN.search(c.body):
            positive_score += 1

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
