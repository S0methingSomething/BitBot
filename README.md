# BitBot

BitBot is an automated release management and announcement bot. It monitors a source GitHub repository for new releases, patches asset files, creates corresponding releases on its own repository, and announces them on Reddit.

Built with modern Python practices: Result-based error handling, type safety with beartype, and comprehensive testing.

## Core Features

-   **Automated Release Patching:** Monitors a source repository and automatically downloads, patches, and re-releases assets.
-   **Structured Release Parsing:** Uses a robust, key-value format in release notes for reliable app detection.
-   **Dual Reddit Posting Modes:**
    -   **Direct Link Mode:** Posts individual download links for each updated app directly to Reddit.
    -   **Landing Page Mode:** Generates a clean, static HTML landing page (GitHub Pages + Cloudflare Pages) for all download links.
-   **Customizable HTML Templates:** Landing page can be fully customized using a powerful placeholder and loop system.
-   **Community Feedback Monitoring:** Actively checks comments on Reddit posts for keywords to provide real-time status (e.g., "Working", "Broken").
-   **Result-Based Error Handling:** No exceptions - all operations return `Ok[T] | Err[E]` for explicit error handling.
-   **Automatic Retries:** Network operations automatically retry with exponential backoff using tenacity.
-   **Type Safety:** Full beartype runtime validation and mypy static checking.
-   **Fast CI/CD:** Uses `uv` for rapid dependency installation in GitHub Actions.

## Quick Start

```bash
# Install dependencies
uv sync

# Run CLI
uv run python -m bitbot.cli --help

# Generate landing page
uv run python -m bitbot.cli page run

# Run tests
uv run pytest tests/ -v
```

## Documentation

For detailed information on how to set up, configure, and customize the bot, please see the comprehensive documentation in the `docs/` directory.

-   **[01 - Configuration](./docs/01-configuration.md):** A complete reference for every setting in `config.toml`.
-   **[02 - Templates & Customization](./docs/02-templates.md):** Instructions on how to customize the Reddit posts and landing page.
-   **[03 - Workflows](./docs/03-workflows.md):** An explanation of the GitHub Actions that automate the bot.
-   **[04 - Scripts](./docs/04-scripts.md):** A detailed breakdown of each Python script and its role.

## Project Structure

-   `.github/workflows/`: Contains the GitHub Actions workflows.
-   `docs/`: Contains all project documentation.
-   `src/bitbot/`: Contains all Python source code.
    -   `commands/`: CLI commands (post, check, release, sync, patch, page, gather, maintain)
    -   `core/`: Core utilities (result, retry, state, config, errors)
    -   `crypto/`: Encryption and patching logic
    -   `gh/`: GitHub API integration
    -   `reddit/`: Reddit API integration
-   `templates/`: Contains the Markdown and HTML templates.
-   `tests/`: Comprehensive test suite (64+ tests, 100% pass rate)
-   `config.toml`: The main configuration file for the bot.
-   `pyproject.toml`: Project dependencies and tool configuration.
