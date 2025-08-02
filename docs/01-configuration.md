# Configuration (`config.toml`)

This file is the central control panel for the bot. Below is a detailed explanation of every section and key.

---

### `[github]`

This section configures the GitHub repositories the bot interacts with.

-   `sourceRepo`: The repository the bot monitors for new releases (e.g., `S0methingSomething/BitEdit`).
-   `botRepo`: The repository where the bot will create its own releases with the patched assets (e.g., `S0methingSomething/BitBot`).
-   `assetFileName`: The name of the asset file the bot should download from the source release and patch.

---

### `[reddit]`

This section controls how the bot posts and manages content on Reddit.

-   `subreddit`: The name of the subreddit to post to (e.g., `"BitTest1"`).
-   `templateFile`: The path to the Markdown template for new Reddit posts.
-   `outdatedTemplateFile`: The path to the Markdown template used for the banner in outdated posts.
-   `postTitle`: The title format for new Reddit posts.
-   `botName`: The name of your bot, used in post templates.
-   `creator`: Your Reddit username, used in post templates.
-   `postMode`: Determines how download links are presented.
    -   `"direct_link"`: (Default) The post body will contain a separate download link for each updated app.
    -   `"landing_page"`: The post body will contain a single link to a generated GitHub Pages site that lists all the downloads.
-   `custom_landing_template`: (Optional) The path to your custom HTML template for the landing page. If this is commented out or the file doesn't exist, the bot will use its built-in default template.

---

### `[outdatedPostHandling]`

This section defines how the bot should handle its own previous posts after a new one is made.

-   `mode`: The method for marking posts as outdated. Currently, only `"inject"` is fully supported.
-   `injectTemplateFile`: The path to the Markdown template for the banner that gets injected at the top of old posts.

---

### `[parsing]`

This section defines the format the bot expects to see in the source repository's release notes.

-   `app_key`, `version_key`, `asset_name_key`: These keys define the exact text the bot looks for when parsing release descriptions (e.g., `app: BitLife`).

---

### `[[apps]]`

This is a list of tables, where each table represents an application the bot manages.

-   `id`: A short, unique, lowercase identifier for the app (e.g., `"bitlife"`). This is used for creating release tags.
-   `displayName`: The user-friendly name of the app (e.g., `"BitLife"`). This is used in post titles and templates.
