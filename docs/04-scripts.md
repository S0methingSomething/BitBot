# Guide: Python Scripts

This document provides a detailed breakdown of each Python script in the `src/` directory and its specific role in the bot's operation.

---

### `helpers.py`

This is a utility module that contains common, reusable functions that are imported by other scripts.
-   **`load_config()`**: Loads and parses the `config.toml` file.
-   **`load_bot_state()` / `save_bot_state()`**: Reads and writes the `bot_state.json` file, which tracks the active Reddit post.
-   **`init_reddit()`**: Handles the boilerplate for authenticating with the Reddit API using PRAW.
-   **`get_bot_posts()` / `update_older_posts()`**: Contains the logic for fetching the bot's post history and injecting the "outdated" banner into old posts.

---

### `release_manager.py`

This is the first and most critical script in the main release workflow.
-   **Responsibility:** To check for new releases in the source repository, create corresponding patched releases in the bot's repository, and prepare the data for all downstream steps.
-   **Process:**
    1.  Fetches the latest releases from the `sourceRepo` defined in the config.
    2.  Parses the release notes for structured, key-value blocks (`app:`, `version:`, etc.).
    3.  For each valid app block, it checks if a release with that tag already exists in the `botRepo`.
    4.  If not, it downloads the specified asset, patches it using `patch_file.py`, and creates a new GitHub release in the `botRepo`.
    5.  It saves the metadata for all newly created releases into `dist/releases.json`.

---

### `patch_file.py`

This script is a Python port of the original `process_vars.js` and is responsible for the core file manipulation.
-   **Responsibility:** To decrypt a file, modify its contents, and re-encrypt it.
-   **Process:**
    1.  Reads the encrypted input file.
    2.  Decrypts the contents using a Base64 decode followed by an XOR cipher.
    3.  Specifically looks for .NET boolean values and changes any `false` to `true`.
    4.  Re-encrypts the modified data and writes it to the output file.

---

### `page_generator.py`

This script builds the static HTML landing page.
-   **Responsibility:** To create the `index.html` file that will be deployed to GitHub Pages.
-   **Process:**
    1.  Reads the `dist/releases.json` file.
    2.  Determines whether to use the default template or a custom one based on the `config.toml` settings.
    3.  Reads the chosen HTML template and finds the `<!-- BEGIN-RELEASE-LOOP -->` block.
    4.  It loops through the release data, replacing placeholders in the loop block for each app.
    5.  It replaces the original loop block with the final, generated HTML and saves the result to `dist/index.html`.

---

### `post_to_reddit.py`

This script is responsible for all interactions with Reddit during a new release.
-   **Responsibility:** To create the new Reddit announcement post and update old ones.
-   **Process:**
    1.  Reads `dist/releases.json` to generate a changelog.
    2.  Reads the `post_template.md` file.
    3.  Replaces all placeholders (like `{{changelog}}` and `{{bot_name}}`) with the appropriate content.
    4.  Submits the new post to the configured subreddit.
    5.  Fetches all previous posts from the bot and uses the `update_older_posts` helper to mark them as outdated.
    6.  Updates `bot_state.json` with the ID of the new post.

---

### `check_comments.py`

This script runs on a frequent schedule to monitor community feedback.
-   **Responsibility:** To update the status line in the active Reddit post.
-   **Process:**
    1.  Reads `bot_state.json` to find the active post ID.
    2.  Fetches all comments on that post.
    3.  Searches for positive (`workingKeywords`) and negative (`notWorkingKeywords`) keywords from the config.
    4.  Calculates a net score and, if a threshold is met, edits the post body to update the status line (e.g., to "**Status:** Working").

---

### `maintain_releases.py`

This script performs routine cleanup on the bot's GitHub releases page.
-   **Responsibility:** To mark old releases as outdated.
-   **Process:**
    1.  Fetches all releases for the `botRepo`.
    2.  It prepends `[OUTDATED]` to the title of all releases except for the most recent one.

---

### `sync_reddit_history.py`

This is a maintenance script designed to correct the bot's state if it ever becomes out of sync with Reddit.
-   **Responsibility:** To ensure old posts are marked as outdated and the `bot_state.json` is pointing to the correct latest post.
-   **Note:** This script does *not* create new posts; it only syncs the state of existing ones.
