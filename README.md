# BitBot

A robust, automated bot for managing and distributing patches for BitLife via GitHub and Reddit.

This project is built with a focus on modern, professional Python development practices, including automated testing, linting, security scanning, and fully automated releases.

## Features

- Monitors a source GitHub repository for new releases.
- Patches a specific asset file (`MonetizationVars`) by transforming its content.
- Creates new, versioned releases in its own repository with the patched asset.
- Posts new releases to a configured subreddit, marking old posts as outdated.
- Adaptively checks for new comments on Reddit to update a post's status.
- Manages its state in a dedicated GitHub Issue, removing the need for stateful commits.
- Implements resilient API clients with automatic retries for handling network failures.
- Enforces code quality and security standards through a rigorous CI/CD pipeline.

## Setup & Installation

This project is managed by **Poetry** for dependency resolution and **uv** for fast environment creation and installation.

1.  **Clone the repository:**
    `git clone <repo-url>`
2.  **Navigate into the project directory:**
    `cd bitbot`
3.  **Ensure you have `pipx` installed, then install Poetry and UV:**
    `pip install pipx`
    `pipx install poetry`
    `pipx install uv`
4.  **Create the virtual environment and install dependencies:**
    `uv pip install -e .[dev]`

## Activating the Environment

After setup, activate the virtual environment to use the installed tools and run the bot:

```bash
source .venv/bin/activate
```

You should see `(.venv)` at the beginning of your shell prompt.

## Configuration

The bot is configured via `config.yaml`. See the comments within the file for details on each setting.

### Secrets Configuration

For the automation to work, you must configure the following secrets in your GitHub repository (`Settings > Secrets and variables > Actions`):

-   `GH_PAT`: A Personal Access Token with `repo` and `issue` scopes, required for the automated semantic release process.
-   `REDDIT_CLIENT_ID`
-   `REDDIT_CLIENT_SECRET`
-   `REDDIT_USERNAME`
-   `REDDIT_PASSWORD`
-   `REDDIT_USER_AGENT`

Note: The `bot_actions.yml` workflow uses the default `GITHUB_TOKEN` which is automatically granted permissions.

### State Management Setup

The bot stores its state (e.g., the active Reddit post ID) in the body of a GitHub Issue to avoid stateful commits.

1.  Create a new issue in your bot's repository.
2.  In the issue body, create a JSON code block with the initial state:
    \`\`\`
    ```json
    {
      "activePostId": null,
      "lastCheckTimestamp": "2024-01-01T00:00:00Z",
      "currentIntervalSeconds": 300,
      "lastCommentCount": 0
    }
    ```
    \`\`\`
3.  Note the issue number and update `state_issue_number` in `config.yaml`.

## Usage

Once the environment is activated, you can run the bot's commands directly:

```bash
# Display help for all commands
bitbot --help

# Example: Run the full release and post cycle
bitbot release

# Example: Run the comment checker manually
bitbot check-comments
```

## Development

With the environment activated, you can run the quality-control tools:

-   **Testing:** `pytest`
-   **Linting:** `ruff check .`
-   **Formatting:** `black .`
-   **Type Checking:** `mypy src`
