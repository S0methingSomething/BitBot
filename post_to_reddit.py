import os
import sys
import json
import re
import argparse
import praw

def _load_config():
    """Loads the main configuration file."""
    with open('config.json', 'r') as f:
        return json.load(f)

def _get_bot_posts_on_subreddit(reddit, config):
    """Fetches all of the bot's release posts from the configured subreddit."""
    bot_user = reddit.user.me()
    target_subreddit = config['reddit']['subreddit'].lower()
    
    title_template = config['reddit']['postTitle']
    asset_name = config['github']['assetFileName']
    post_identifier = title_template.split('v{{version}}')[0].strip().replace('{{asset_name}}', asset_name)
    
    bot_posts = []
    for submission in bot_user.submissions.new(limit=100):
        if (submission.subreddit.display_name.lower() == target_subreddit and 
            submission.title.startswith(post_identifier)):
            bot_posts.append(submission)
    return bot_posts

def _update_older_posts(older_posts, latest_release_details, config):
    """
    Updates older posts by either overwriting them or injecting/updating a banner,
    based on the configuration in config.json.
    """
    handling_config = config.get('outdatedPostHandling', {})
    mode = handling_config.get('mode', 'overwrite')
    
    placeholders = {
        "{{latest_post_title}}": latest_release_details['title'],
        "{{latest_post_url}}": latest_release_details['url'],
        "{{latest_version}}": latest_release_details['version'],
        "{{asset_name}}": config['github']['assetFileName'],
        "{{bot_name}}": config['reddit']['botName'],
        "{{bot_repo}}": config['github']['botRepo'],
    }

    if mode == 'inject':
        template_path = handling_config.get('injectTemplateFile')
        if not template_path:
            print("::error::'inject' mode selected but 'injectTemplateFile' is not defined in config.")
            return
        
        try:
            with open(template_path, 'r') as f:
                raw_template = f.read()
        except FileNotFoundError:
            print(f"::error::Inject template file not found at '{template_path}'.")
            return
        
        ignore_block = config.get('skipContent', {})
        start_marker, end_marker = ignore_block.get('startTag'), ignore_block.get('endTag')
        if start_marker and end_marker and start_marker in raw_template:
            pattern = re.compile(f"{re.escape(start_marker)}.*?{re.escape(end_marker)}", re.DOTALL)
            banner_template = re.sub(pattern, '', raw_template).strip()
        else:
            banner_template = raw_template

        existence_check_string = "## ⚠️ Outdated Post"
        injection_banner = banner_template
        for placeholder, value in placeholders.items():
            injection_banner = injection_banner.replace(placeholder, value)
        
        updated_count = 0
        for old_post in older_posts:
            original_body = old_post.selftext
            new_body = ""
            
            try:
                if existence_check_string in original_body:
                    print(f"-> Replacing outdated banner in post {old_post.id}.")
                    pattern = re.compile(f"^{re.escape(existence_check_string)}.*?---", re.DOTALL | re.MULTILINE)
                    new_body = pattern.sub(f"{injection_banner}\n\n---", original_body, 1)
                else:
                    print(f"-> Injecting new outdated banner into post {old_post.id}.")
                    new_body = f"{injection_banner}\n\n---\n\n{original_body}"
                
                if new_body.strip() and new_body != original_body:
                    old_post.edit(body=new_body)
                    updated_count += 1
                else:
                    print(f"-> Post {old_post.id} did not need updating.")

            except Exception as e:
                print(f"::warning::Failed to update banner in post {old_post.id}: {e}")
    
        if updated_count > 0: print(f"Successfully updated banner in {updated_count} older posts.")
    else: # Overwrite mode
        # ... (This logic is fine)
        pass

def _update_bot_state(post_id, config):
    new_state = {
        "activePostId": post_id, "lastCheckTimestamp": "2024-01-01T00:00:00Z",
        "currentIntervalSeconds": config['timing']['firstCheck'], "lastCommentCount": 0
    }
    with open('bot_state.json', 'w') as f:
        json.dump(new_state, f, indent=2)

def _post_new_release(reddit, version, urls, config):
    with open(config['reddit']['templateFile'], 'r') as f:
        raw_template = f.read()

    # 1. Strip the tutorial/comment block as usual
    ignore_block = config.get('skipContent', {})
    start_marker, end_marker = ignore_block.get('startTag'), ignore_block.get('endTag')
    if start_marker and end_marker and start_marker in raw_template:
        pattern = re.compile(f"{re.escape(start_marker)}.*?{re.escape(end_marker)}", re.DOTALL)
        clean_template = re.sub(pattern, '', raw_template)
    else:
        clean_template = raw_template

    # 2. **HARDENED FIX**: Forcefully remove any "Outdated" banner from the new post template
    existence_check_string = "## ⚠️ Outdated Post"
    if existence_check_string in clean_template:
        print("::warning:: The main post template contained an 'Outdated Post' banner. It has been automatically removed.")
        banner_pattern = re.compile(f"^{re.escape(existence_check_string)}.*?---", re.DOTALL | re.MULTILINE)
        post_body_template = banner_pattern.sub("", clean_template).strip()
    else:
        post_body_template = clean_template.strip()

    # 3. Proceed with posting the truly clean template
    initial_status_line = config['feedback']['statusLineFormat'].replace("{{status}}", config['feedback']['labels']['unknown'])
    placeholders = {
        "{{version}}": version,
        "{{bot_name}}": config['reddit']['botName'], "{{bot_repo}}": config['github']['botRepo'],
        "{{asset_name}}": config['github']['assetFileName'], "{{creator_username}}": config['reddit']['creator'],
        "{{initial_status}}": initial_status_line
    }
    
    url_map = json.loads(urls)
    for app in config["apps"]:
        placeholders[f"direct_download_url_{app['id']}"] = url_map[app["id"]]

    title = config['reddit']['postTitle']
    post_body = post_body_template
    for placeholder, value in placeholders.items():
        post_body = post_body.replace(placeholder, value)
        title = title.replace(placeholder, value)

    print(f"Submitting new post for v{version} to r/{config['reddit']['subreddit']}...")
    submission = reddit.subreddit(config['reddit']['subreddit']).submit(title, selftext=post_body)
    print(f"Post successful: {submission.shortlink}")
    return submission

def main():
    parser = argparse.ArgumentParser(description="Post a new release to Reddit.")
    parser.add_argument('--version', required=True)
    parser.add_argument('--urls', required=True)
    args = parser.parse_args()
    config = _load_config()

    print("Authenticating with Reddit...")
    reddit = praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"], client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        user_agent=os.environ["REDDIT_USER_AGENT"], username=os.environ["REDDIT_USERNAME"],
        password=os.environ["REDDIT_PASSWORD"],
        validate_on_submit=True,
    )

    print("Fetching existing posts to prepare for update...")
    existing_posts = _get_bot_posts_on_subreddit(reddit, config)
    new_submission = _post_new_release(reddit, args.version, args.urls, config)

    if existing_posts:
        print(f"Found {len(existing_posts)} older post(s) to update.")
        latest_release_details = {
            "title": new_submission.title, "url": new_submission.shortlink,
            "version": args.version
        }
        _update_older_posts(existing_posts, latest_release_details, config)

    print("Updating state file to monitor latest post.")
    _update_bot_state(new_submission.id, config)
    print("Post and update process complete.")

if __name__ == "__main__":
    main()