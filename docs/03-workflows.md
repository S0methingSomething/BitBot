# GitHub Actions Workflows

BitBot uses GitHub Actions to automate the release process. All workflows are in `.github/workflows/`.

---

## Main Workflow (`main.yml`)

**Name:** `[Multi-App Release] Check, Patch, and Manage Reddit`

**Triggers:**
- Schedule: Runs at 1 AM and 4 PM UTC daily
- Manual: Can be triggered via workflow_dispatch

**Jobs:**

### 1. gather_releases
- Checks source repository for new releases
- Adds new releases to queue
- Uploads `dist/` and `bot_state.json` as artifacts

### 2. create_releases
- Downloads artifacts from previous job
- Creates GitHub releases for queued items
- Uploads updated artifacts

### 3. generate_page
- Generates landing page HTML
- Deploys to GitHub Pages
- Outputs page URL

### 4. post_to_reddit
- Updates existing Reddit post (rolling_update mode)
- Uses landing page URL from previous job
- Skipped if `dry_run` input is true
- Uploads final `bot_state.json`

**Environment Variables Required:**
- `GITHUB_TOKEN` (automatic)
- `REDDIT_CLIENT_ID`
- `REDDIT_CLIENT_SECRET`
- `REDDIT_USERNAME`
- `REDDIT_PASSWORD`

---

## Maintenance Workflow (`maintain_releases.yml`)

**Name:** `[Maintenance] Update Old Release Titles`

**Triggers:**
- Runs after main workflow completes successfully

**What it does:**
- Marks old releases as outdated
- Updates release titles with `[OUTDATED]` prefix

---

## Preview Workflow (`preview_page.yml`)

**Name:** `[Preview] Generate and Deploy Landing Page`

**Triggers:**
- Manual only (workflow_dispatch)

**What it does:**
- Gathers current releases
- Generates landing page
- Deploys to GitHub Pages for preview

**Use case:** Preview landing page changes without running full workflow.

---

## Workflow Configuration

### Secrets Required

Set these in your repository settings under **Settings → Secrets and variables → Actions**:

- `REDDIT_CLIENT_ID`: Reddit app client ID
- `REDDIT_CLIENT_SECRET`: Reddit app client secret
- `REDDIT_USERNAME`: Reddit bot account username
- `REDDIT_PASSWORD`: Reddit bot account password

**Note:** `GITHUB_TOKEN` is automatically provided by GitHub Actions.

### Permissions Required

The repository needs these permissions:
- **Contents:** Read and write (for creating releases)
- **Pages:** Write (for deploying landing page)
- **ID token:** Write (for GitHub Pages deployment)

Set these in **Settings → Actions → General → Workflow permissions**.

---

## Dry Run Mode

The main workflow supports a dry run mode:

1. Go to **Actions** tab
2. Select **[Multi-App Release] Check, Patch, and Manage Reddit**
3. Click **Run workflow**
4. Check **Run without posting to Reddit**
5. Click **Run workflow**

This will run everything except the Reddit posting step.

---

## Monitoring Workflows

### View Workflow Runs

1. Go to **Actions** tab
2. Click on a workflow run to see details
3. Click on individual jobs to see logs

### Artifacts

Workflows upload artifacts that can be downloaded:
- `release-data`: Release queue and data files
- `final-state`: Final bot state after posting

### Troubleshooting

**Common issues:**

1. **Authentication errors:** Check that secrets are set correctly
2. **Rate limits:** GitHub/Reddit API rate limits may cause failures
3. **Missing artifacts:** Ensure previous jobs completed successfully
4. **State persistence:** `bot_state.json` must be uploaded/downloaded between jobs

---

## Customizing Workflows

### Changing Schedule

Edit the cron expression in `main.yml`:

```yaml
schedule:
  - cron: '0 1,16 * * *'  # 1 AM and 4 PM UTC
```

### Adding Steps

Add new steps to existing jobs or create new jobs. Make sure to:
1. Upload/download artifacts as needed
2. Set required environment variables
3. Use `uv run python -m src.commands.<command>` for CLI commands

### Disabling Workflows

To disable a workflow:
1. Go to **Actions** tab
2. Click on the workflow
3. Click **⋯** (three dots)
4. Select **Disable workflow**
