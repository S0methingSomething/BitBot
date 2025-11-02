# CLI Commands

BitBot uses a modern CLI interface with individual commands for each operation. All commands are run using `uv run python -m src.commands.<command>`.

---

## Core Commands

### `gather`

Gathers new releases from the source repository.

```bash
uv run python -m src.commands.gather
```

**What it does:**
- Fetches latest releases from source repository
- Compares with previously processed releases
- Adds new releases to the queue
- Updates `dist/release_queue.json`

**Environment variables:**
- `GITHUB_TOKEN`: Required

---

### `release`

Creates GitHub releases from pending queue.

```bash
uv run python -m src.commands.release
```

**What it does:**
- Processes releases from `dist/release_queue.json`
- Downloads assets from source releases
- Patches assets (if applicable)
- Creates new releases in bot repository
- Updates `dist/releases.json`

**Environment variables:**
- `GITHUB_TOKEN`: Required

---

### `post`

Posts or updates Reddit announcement.

```bash
uv run python -m src.commands.post [--page-url URL]
```

**Options:**
- `--page-url`: Landing page URL (auto-detected if not provided)

**What it does:**
- Loads pending releases from queue
- Generates post title and body using templates
- In `rolling_update` mode: Updates existing post
- Otherwise: Creates new post
- Saves post ID to `bot_state.json`

**Environment variables:**
- `GITHUB_TOKEN`: Required
- `REDDIT_CLIENT_ID`: Required
- `REDDIT_CLIENT_SECRET`: Required
- `REDDIT_USERNAME`: Required
- `REDDIT_PASSWORD`: Required

---

### `page`

Generates the landing page.

```bash
uv run python -m src.commands.page [--output PATH]
```

**Options:**
- `--output`: Output path (default: `dist/index.html`)

**What it does:**
- Loads release data from `dist/releases.json`
- Renders HTML using template
- Outputs static landing page

---

### `maintain`

Marks old releases as outdated.

```bash
uv run python -m src.commands.maintain
```

**What it does:**
- Finds releases that are no longer the latest version
- Updates release titles with `[OUTDATED]` prefix
- Updates `dist/releases.json`

**Environment variables:**
- `GITHUB_TOKEN`: Required

---

## Utility Commands

### `patch`

Patches a single asset file.

```bash
uv run python -m src.commands.patch INPUT_FILE OUTPUT_FILE
```

**Arguments:**
- `INPUT_FILE`: Path to input file
- `OUTPUT_FILE`: Path to output file

**What it does:**
- Decrypts input file
- Applies modifications
- Re-encrypts output file

---

### `check`

Checks Reddit comments for feedback (not implemented).

```bash
uv run python -m src.commands.check
```

**Status:** Legacy feature, needs refactoring.

---

### `sync`

Syncs Reddit state (not implemented).

```bash
uv run python -m src.commands.sync
```

**Status:** Legacy feature, needs refactoring.

---

## Typical Workflow

The main workflow runs these commands in sequence:

1. **gather** - Find new releases
2. **release** - Create GitHub releases
3. **page** - Generate landing page
4. **post** - Update Reddit post

This is automated in `.github/workflows/main.yml` and runs twice daily.

---

## Development

### Running Commands Locally

```bash
# Install dependencies
uv sync

# Export required environment variables
export GITHUB_TOKEN=your_token
export REDDIT_CLIENT_ID=your_client_id
export REDDIT_CLIENT_SECRET=your_client_secret
export REDDIT_USERNAME=your_username
export REDDIT_PASSWORD=your_password

# Run commands
uv run python -m src.commands.gather
uv run python -m src.commands.release
uv run python -m src.commands.page
uv run python -m src.commands.post
```

### Testing Without Posting

Set `post_manually = true` in `config.toml` to generate post files without actually posting to Reddit.

---

## File Locations

- **Queue:** `dist/release_queue.json` - Pending releases
- **Releases:** `dist/releases.json` - All release data
- **State:** `bot_state.json` - Bot state (active post ID, etc.)
- **Landing Page:** `dist/index.html` - Generated landing page
- **Templates:** `templates/` - Post and page templates
