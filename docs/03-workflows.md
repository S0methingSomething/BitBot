# Guide: GitHub Actions Workflows

This project uses several GitHub Actions workflows to automate the entire release and maintenance process. They are located in the `.github/workflows/` directory.

---

### `main.yml` - The Core Workflow

**Trigger:** Runs on a schedule (twice a day) or can be triggered manually (`workflow_dispatch`).

This is the primary workflow that orchestrates the entire release process.

**Jobs:**

1.  **`manage_releases`**
    -   Runs `src/release_manager.py`.
    -   Checks the source repository for new releases.
    -   If new releases are found, it patches the asset file using `src/patch_file.py` and creates new releases in the bot's repository.
    -   Saves the data for all new releases to a `releases.json` file.
    -   Uploads the `dist/` directory (containing `releases.json`) as an artifact named `release-data`.

2.  **`generate_page`**
    -   Runs only if the `manage_releases` job found new releases.
    -   Downloads the `release-data` artifact.
    -   Runs `src/page_generator.py` to create the `index.html` landing page.
    -   Uploads the generated `dist/index.html` as an artifact named `github-pages`.

3.  **`post_to_reddit`**
    -   Runs only if the `manage_releases` job found new releases.
    -   Runs `src/post_to_reddit.py`.
    -   The script reads the `releases.json` file to generate a changelog.
    -   It posts the new release announcement to the configured subreddit.
    -   It updates all older posts by the bot to mark them as outdated.

---

### `deploy_pages.yml` - GitHub Pages Deployment

**Trigger:** Runs automatically after `main.yml` completes successfully.

-   This workflow is responsible for deploying the landing page to GitHub Pages.
-   It downloads the `github-pages` artifact created by the `generate_page` job.
-   It uses the standard `actions/deploy-pages` action to publish the contents to your GitHub Pages site.

---

### `check_comments.yml` - Community Feedback Monitor

**Trigger:** Runs on a schedule (every 15 minutes).

-   This workflow runs `src/check_comments.py`.
-   It fetches the comments on the currently active Reddit post (defined in `bot_state.json`).
-   It analyzes the comments for positive and negative keywords.
-   Based on the feedback, it updates a status line in the Reddit post body.
-   It uses an adaptive timer to check more frequently when new comments appear.

---

### `maintain_releases.yml` - Release Maintenance

**Trigger:** Runs automatically after `main.yml` completes successfully.

-   This workflow runs `src/maintain_releases.py`.
-   It fetches all releases from the bot's own GitHub repository.
-   It prepends `[OUTDATED]` to the title of all but the most recent release, keeping the releases page clean.
