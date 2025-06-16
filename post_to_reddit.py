import os
import sys
import praw

def post_update_to_reddit(version, release_url, subreddit_name, bot_repo_name):
    """Posts a new release announcement and saves the post ID."""
    print("Authenticating with Reddit...")
    try:
        reddit = praw.Reddit(
            client_id=os.environ["REDDIT_CLIENT_ID"],
            client_secret=os.environ["REDDIT_CLIENT_SECRET"],
            user_agent=os.environ["REDDIT_USER_AGENT"],
            username=os.environ["REDDIT_USERNAME"],
            password=os.environ["REDDIT_PASSWORD"],
        )
        print(f"Authenticated as Reddit user: {reddit.user.me()}")
    except Exception as e:
        print(f"Error: Failed to authenticate with Reddit: {e}")
        sys.exit(1)

    title = f"MonetizationVars for BitLife v{version}"
    self_text = f"""
This is an automated post by [BitBot](https://github.com/{bot_repo_name}).

---

### **Download Link**

You can download the decrypted JSON file from the official release page:

**[MonetizationVars_decrypted.json (at GitHub)]({release_url})**

---

This bot was created by u/C1oudyLol.

**Current Status (based on community feedback):** Working
    """

    print(f"Submitting to r/{subreddit_name}...")
    try:
        submission = reddit.subreddit(subreddit_name).submit(title, selftext=self_text.strip())
        print(f"Post successful: {submission.shortlink}")

        # CRUCIAL STEP: Save the new post ID for the monitoring workflow
        with open("latest_post_id.txt", "w") as f:
            f.write(submission.id)
        print(f"Saved new post ID ({submission.id}) to latest_post_id.txt")

    except Exception as e:
        print(f"Error: Failed to submit post: {e}")
        sys.exit(1)

if __name__ == "__main__":
    version, release_url, subreddit, bot_repo = sys.argv[1:5]
    post_update_to_reddit(version, release_url, subreddit, bot_repo)
