# BitBot Quick Start Guide

## Prerequisites

1. **GitHub Personal Access Token** with `repo` permissions
2. **Reddit App Credentials** (client ID, client secret, username, password)
3. **Python 3.11+** and `uv` installed

## Setup (5 minutes)

### 1. Configure `config.toml`

Edit `config.toml` with your settings:

```toml
[github]
sourceRepo = "owner/source-repo"  # Repo to monitor for releases
botRepo = "your-username/BitBot"  # Your bot's repo
assetFileName = "MonetizationVars" # File to patch

[reddit]
subreddit = "your-subreddit"
botName = "YourBot"
creator = "your-reddit-username"
postIdentifier = "[YourBot]"

[apps]
[[apps]]
id = "bitlife"
displayName = "BitLife"

[[apps]]
id = "bitlife-go"
displayName = "BitLife Go"
```

### 2. Set Environment Variables

```bash
# GitHub
export GITHUB_TOKEN="ghp_your_token_here"

# Reddit
export REDDIT_CLIENT_ID="your_client_id"
export REDDIT_CLIENT_SECRET="your_secret"
export REDDIT_USERNAME="your_bot_username"
export REDDIT_PASSWORD="your_bot_password"
```

### 3. Install Dependencies

```bash
uv sync
```

## Usage

BitBot has 8 commands that run in sequence:

### 1. **Gather** - Check for new releases
```bash
uv run python -m src.commands.gather
```
- Fetches releases from source repo
- Parses release descriptions
- Adds to pending queue

### 2. **Release** - Create patched releases
```bash
uv run python -m src.commands.release
```
- Downloads assets from pending queue
- Patches files
- Creates releases on your bot repo

### 3. **Post** - Announce on Reddit
```bash
uv run python -m src.commands.post
```
- Generates post title and body
- Posts to Reddit (or updates existing post in rolling mode)
- Saves post ID to state

### 4. **Page** - Generate landing page (optional)
```bash
uv run python -m src.commands.page
```
- Creates HTML landing page
- Outputs to `dist/index.html`
- Deploy to GitHub Pages

### 5. **Maintain** - Mark old releases
```bash
uv run python -m src.commands.maintain
```
- Finds old releases on bot repo
- Marks them as [OUTDATED] in title

### 6. **Check** - Monitor feedback (optional)
```bash
uv run python -m src.commands.check
```
- Reads Reddit comments
- Updates post status based on keywords

### 7. **Sync** - Sync state (optional)
```bash
uv run python -m src.commands.sync
```
- Syncs bot state with Reddit post

### 8. **Patch** - Manual file patching
```bash
uv run python -m src.commands.patch input.file output.file
```
- Patches a single file manually

## Typical Workflow

### First Time Setup:
```bash
# 1. Check for new releases
uv run python -m src.commands.gather

# 2. Create releases on your repo
uv run python -m src.commands.release

# 3. Post to Reddit
uv run python -m src.commands.post

# 4. (Optional) Generate landing page
uv run python -m src.commands.page
```

### Regular Updates (Automated):
Set up GitHub Actions to run these commands on a schedule:
- `gather` → `release` → `post` every 6-12 hours
- `maintain` once per day
- `check` every hour (if monitoring feedback)

## Rolling Update Mode

In `config.toml`:
```toml
[reddit]
postMode = "rolling_update"

[reddit.rolling]
daysBeforeNewPost = 7  # Edit same post for 7 days
updateExisting = true
```

This prevents spam by editing ONE post instead of creating multiple posts.

## Troubleshooting

### "No pending releases"
- Run `gather` first to fetch releases
- Check `bot_state.json` for pending queue

### "GitHub API error"
- Verify `GITHUB_TOKEN` is set
- Check token has `repo` permissions

### "Reddit API error"
- Verify all Reddit env vars are set
- Check credentials are correct

### "File not found"
- Ensure `config.toml` exists
- Check paths in config are correct

## Files to Know

- `config.toml` - Main configuration
- `bot_state.json` - Bot state (auto-created)
- `templates/post_template.md` - Reddit post template
- `.taskmaster/logs/bitbot.log` - Error logs

## Need Help?

Check the full docs:
- `docs/01-configuration.md` - All config options
- `docs/02-templates.md` - Customize templates
- `docs/03-workflows.md` - GitHub Actions setup
- `docs/04-scripts.md` - Detailed command reference

## Quick Test

Test without credentials:
```bash
# Check if commands work
uv run python -m src.commands.gather --help
uv run python -m src.commands.release --help
uv run python -m src.commands.post --help
```

All commands should show help text without errors.
