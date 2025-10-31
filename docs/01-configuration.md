# Configuration (`config.toml`)

This file is the central control panel for the bot. Below is a detailed explanation of every section and key.

---

### `[github]`

This section configures the GitHub repositories the bot interacts with.

-   `sourceRepo`: The repository the bot monitors for new releases (e.g., `S0methingSomething/BitEdit`).
-   `botRepo`: The repository where the bot will create its own releases with the patched assets (e.g., `S0methingSomething/BitBot`).
-   `assetFileName`: The name of the asset file the bot should download from the source release and patch.
-   `pages_url`: The URL to your GitHub Pages site where the landing page will be hosted.

---

### `[reddit]`

This section controls how the bot posts and manages content on Reddit.

-   `subreddit`: The name of the subreddit to post to (e.g., `"BitTest1"`).
-   `botName`: The name of your bot, used in post templates.
-   `creator`: Your Reddit username, used in post templates.
-   `postMode`: Determines how download links are presented.
    -   `"direct_link"`: The post body will contain a separate download link for each updated app.
    -   `"landing_page"`: (Default) The post body will contain a single link to a generated GitHub Pages site that lists all the downloads.
-   `post_manually`: Set to `true` to generate post files instead of posting to Reddit (for manual review).

---

### `[reddit.templates]`

Defines the paths to template files used by the bot.

-   `post`: Path to the Markdown template for new Reddit posts (e.g., `"templates/post_template.md"`).
-   `outdated_post`: Path to the Markdown template for outdated post banners.
-   `inject_banner`: Path to the Markdown template for the banner injected into old posts (e.g., `"templates/inject_template.md"`).
-   `custom_landing`: (Optional) Path to your custom HTML template for the landing page. If omitted or file doesn't exist, uses the default template.

---

### `[reddit.formats]`

Defines dynamic format strings for post content.

#### `[reddit.formats.titles]`

Title formats for different scenarios:
-   `added_only`: Title when only new apps are added.
-   `updated_only_single`: Title when a single app is updated.
-   `updated_only_multi`: Title when multiple apps are updated.
-   `mixed_single_update`: Title when apps are both added and one is updated.
-   `mixed_multi_update`: Title when apps are both added and multiple are updated.
-   `generic`: Fallback title for complex updates.

Placeholders: `{{added_list}}`, `{{updated_list}}`, `{{date}}`

#### `[reddit.formats.changelog]`

Changelog line formats for different actions and modes:
-   `added_landing`: Format for added apps in landing page mode.
-   `updated_landing`: Format for updated apps in landing page mode.
-   `removed_landing`: Format for removed apps in landing page mode.
-   `added_direct`: Format for added apps in direct link mode.
-   `updated_direct`: Format for updated apps in direct link mode.
-   `removed_direct`: Format for removed apps in direct link mode.

Placeholders: `{{display_name}}`, `{{asset_name}}`, `{{version}}`, `{{new_version}}`, `{{old_version}}`, `{{download_url}}`

#### `[reddit.formats.table]`

Table format for available apps list:
-   `header`: Table header row.
-   `divider`: Table divider row.
-   `line`: Format for each app row.

Placeholders: `{{display_name}}`, `{{asset_name}}`, `{{version}}`

---

### `[safety]`

Safety features to prevent account flagging.

-   `max_outbound_links_warn`: Warning threshold for number of outbound links in a post (default: 5).

---

### `[outdatedPostHandling]`

Defines how the bot should handle its own previous posts after a new one is made.

-   `mode`: The method for marking posts as outdated. Currently supports `"inject"` (injects a banner at the top of old posts).

---

### `[messages]`

Text formats for GitHub releases.

-   `releaseTitle`: Title format for bot releases (e.g., `"{{displayName}} MonetizationVars v{{version}}"`).
-   `releaseDescription`: Description format for bot releases.

Placeholders: `{{displayName}}`, `{{version}}`, `{{asset_name}}`

---

### `[skipContent]`

Defines tags for tutorial/comment blocks to be removed before posting.

-   `startTag`: Opening tag for content to skip (e.g., `"<!-- TUTORIAL-START -->"`).
-   `endTag`: Closing tag for content to skip (e.g., `"<!-- TUTORIAL-END -->"`).

---

### `[feedback]`

Rules for analyzing Reddit comments and updating the post status.

-   `statusLineFormat`: Format for the status line in posts (e.g., `"**Status:** {{status}} (based on comments)."`).
-   `statusLineRegex`: Regex pattern to find the status line for updating.
-   `workingKeywords`: List of keywords indicating the app is working.
-   `notWorkingKeywords`: List of keywords indicating the app is not working.
-   `minFeedbackCount`: Minimum net feedback count to change status.

#### `[feedback.labels]`

Status labels:
-   `working`: Label when app is confirmed working.
-   `broken`: Label when app is potentially broken.
-   `unknown`: Label when there's not enough feedback.

---

### `[timing]`

Controls the adaptive polling interval for the comment checker (in seconds).

-   `firstCheck`: Initial check interval after a new post (default: 300 seconds / 5 minutes).
-   `maxWait`: Maximum wait time between checks (default: 3600 seconds / 1 hour).
-   `increaseBy`: Amount to increase interval when no new comments (default: 300 seconds).

---

### `[parsing]`

Defines the keys to look for when parsing release descriptions.

-   `app_key`: Key for app identifier (default: `"app"`).
-   `version_key`: Key for version number (default: `"version"`).
-   `asset_name_key`: Key for asset filename (default: `"asset_name"`).

---

### `[[apps]]`

This is a list of tables, where each table represents an application the bot manages.

-   `id`: A short, unique, lowercase identifier for the app (e.g., `"bitlife"`). This is used for creating release tags.
-   `displayName`: The user-friendly name of the app (e.g., `"BitLife"`). This is used in post titles and templates.
