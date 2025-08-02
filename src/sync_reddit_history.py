import os
import sys
from helpers import (
    load_config,
    init_reddit,
    get_bot_posts,
    parse_versions_from_post,
    load_bot_state,
    save_bot_state,
)

def main():
    """
    Synchronizes the bot's online state with the latest post on Reddit.
    This script reads the latest Reddit post, parses the versions from it,
    and updates the `online.last_posted_versions` in `bot_state.json`.
    """
    config = load_config()
    
    print("Initializing Reddit client...")
    reddit = init_reddit(config)
    
    print("Fetching latest bot posts...")
    bot_posts = get_bot_posts(reddit, config)
    
    if not bot_posts:
        print("::warning::No posts found on Reddit. Cannot sync state.")
        sys.exit(0)
        
    latest_post = bot_posts[0]
    print(f"Found latest post: {latest_post.title} ({latest_post.id})")
    
    versions_on_reddit = parse_versions_from_post(latest_post, config)
    
    if not versions_on_reddit:
        print(f"::error::Could not parse any versions from the latest post. State will not be updated.")
        sys.exit(1)
        
    print(f"Updating local state with versions from Reddit: {versions_on_reddit}")
    
    bot_state = load_bot_state()
    bot_state['online']['last_posted_versions'] = versions_on_reddit
    bot_state['online']['activePostId'] = latest_post.id
    
    save_bot_state(bot_state)
    
    print("Successfully synchronized Reddit state to bot_state.json.")

if __name__ == "__main__":
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    import paths
    main()