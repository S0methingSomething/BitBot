# Configuration (`config.toml`)

This file is the central control panel for BitBot. Below is a detailed explanation of every section and key.

---

## `[github]`

Configures the GitHub repositories the bot interacts with.

- `sourceRepo`: The repository to monitor for new releases (e.g., `"S0methingSomething/BitEdit"`)
- `botRepo`: Your repository where patched releases will be created (e.g., `"S0methingSomething/BitBot"`)
- `assetFileName`: The asset file name to download and patch (e.g., `"MonetizationVars"`)

---

## `[reddit]`

Controls how the bot posts and manages content on Reddit.

- `subreddit`: The subreddit to post to (e.g., `"BitTest1"`)
- `botName`: Your bot's name, used in templates (e.g., `"BitBot"`)
- `creator`: Your Reddit username (e.g., `"C1oudyLol"`)
- `userAgent`: Reddit API user agent (e.g., `"BitBot/1.0 by C1oudyLol"`)
- `postMode`: How posts are managed
  - `"rolling_update"`: Updates a single post with new releases (recommended)
- `downloadMode`: How download links are presented
  - `"landing_page"`: Only links to landing page (recommended, lower ban risk)
  - `"direct"`: Includes individual download links in changelog
- `post_manually`: Set to `true` to generate post files instead of posting (for manual review)

---

## `[reddit.templates]`

Paths to template files used by the bot.

- `post`: Markdown template for Reddit posts (e.g., `"templates/post_template.md"`)
- `outdated_post`: Template for outdated post banners
- `inject_banner`: Template for banners injected into old posts
- `custom_landing`: (Optional) Custom HTML template for landing page

---

## `[reddit.formats]`

Dynamic format strings for post content.

### `[reddit.formats.changelog]`

Changelog line formats:
- `added_landing`: Format for added apps (landing page mode)
- `updated_landing`: Format for updated apps (landing page mode)
- `removed_landing`: Format for removed apps (landing page mode)
- `added_direct`: Format for added apps (direct link mode)
- `updated_direct`: Format for updated apps (direct link mode)
- `removed_direct`: Format for removed apps (direct link mode)

**Placeholders:**
- `{{display_name}}`: App display name
- `{{asset_name}}`: Asset file name
- `{{version}}` / `{{new_version}}` / `{{old_version}}`: Version numbers
- `{{download_url}}`: Direct download URL (direct mode only)

### `[reddit.formats.table]`

Available apps table format:
- `header`: Table header row
- `divider`: Table divider row
- `line`: Table data row format

---

## `[outdatedPostHandling]`

Controls how old posts are marked as outdated.

- `mode`: How to update old posts
  - `"overwrite"`: Replace entire post body with outdated banner
  - `"inject"`: Inject banner at the top of existing content
- `titlePrefix`: Prefix added to outdated release titles (e.g., `"[OUTDATED]"`)

---

## `[feedback]`

Community feedback monitoring settings.

- `statusLineFormat`: Format for status line (e.g., `"**Status:** {{status}}"`)
- `labels`: Status labels
  - `working`: Label when app is working
  - `broken`: Label when app is broken
  - `unknown`: Label when status is unknown
- `keywords`: Keywords to detect in comments
  - `working`: Keywords indicating app works
  - `broken`: Keywords indicating app is broken

---

## `[safety]`

Safety limits to prevent Reddit bans.

- `max_outbound_links_warn`: Warning threshold for outbound links (default: 5)
- `max_outbound_links_error`: Error threshold for outbound links (default: 10)

**Note:** With `downloadMode = "landing_page"`, posts typically have only 3 links total (landing page + 2 related projects), well below safety limits.

---

## Environment Variables

Required environment variables (set in GitHub Secrets):

- `GITHUB_TOKEN`: GitHub personal access token
- `REDDIT_CLIENT_ID`: Reddit app client ID
- `REDDIT_CLIENT_SECRET`: Reddit app client secret
- `REDDIT_USERNAME`: Reddit bot account username
- `REDDIT_PASSWORD`: Reddit bot account password

**Note:** `REDDIT_USER_AGENT` is no longer needed as an environment variable - it's configured in `config.toml` as `userAgent`.

---

## Example Configuration

```toml
[github]
sourceRepo = "S0methingSomething/BitEdit"
botRepo = "S0methingSomething/BitBot"
assetFileName = "MonetizationVars"

[reddit]
subreddit = "BitTest1"
botName = "BitBot"
creator = "C1oudyLol"
userAgent = "BitBot/1.0 by C1oudyLol"
postMode = "rolling_update"
downloadMode = "landing_page"
post_manually = false
```
