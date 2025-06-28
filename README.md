# BitBot

A robust, automated bot for managing and distributing patches for BitLife via GitHub and Reddit. This project is built with a focus on modern, professional Python development practices, including automated testing, linting, security scanning, and fully automated releases.

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

This project uses **uv** for fast environment creation and dependency management, and **pre-commit** for code quality.

1.  **Clone the repository:**
    ```bash
    git clone <repo-url>
    cd bitbot
    ```
2.  **Ensure you have `pipx` installed, then install UV:**
    ```bash
    pip install pipx
    pipx install uv
    ```
3.  **Create the virtual environment and install dependencies:**
    ```bash
    uv pip install -e .
    ```
4.  **Set up pre-commit hooks (Developer Guardrail):**
    ```bash
    uv run pre-commit install
    ```

## Activating the Environment

To run the bot or development tools, activate the virtual environment:
```bash
source .venv/bin/activate```
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

Note: The `bot_actions.yml` workflow uses the default `GITHUB_TOKEN` which is automatically granted permissions for most actions.

### State Management Setup

The bot stores its state in the body of a GitHub Issue. To set this up safely and correctly, run the `init-state` command.

1.  Ensure your `GITHUB_TOKEN` or `GH_PAT` is available as an environment variable.
2.  Run the initialization command:
    ```bash
    uv run bitbot init-state
    ```
3.  This will create a new issue in the `botRepo` defined in `config.yaml`. Note the issue number and update `state_issue_number` in your `config.yaml` file.

## Usage

Once the environment is activated, you can run the bot's commands directly:
```bash
# Display help for all commands
bitbot --help

# Example: Run the full release and post cycle
bitbot release

# Example: Run the comment checker manually
bitbot check-comments

# Example: Initialize the state-tracking issue
bitbot init-state
```

## Development

With the environment activated, you can run the quality-control tools:

-   **Testing:** `pytest`
-   **Linting:** `ruff check .`
-   **Formatting:** `black .`
-   **Type Checking:** `mypy src`
