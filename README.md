# BitBot

BitBot is an automated release management and announcement bot. It is designed to monitor a source GitHub repository for new releases, patch asset files, create corresponding releases on its own repository, and announce them on Reddit.

This project is built to be highly modular, configurable, and maintainable.

## Core Features

-   **Automated Release Patching:** Monitors a source repository and automatically downloads, patches, and re-releases assets.
-   **Structured Release Parsing:** Uses a robust, key-value format in release notes for reliable app detection.
-   **Dual Reddit Posting Modes:**
    -   **Direct Link Mode:** Posts individual download links for each updated app directly to Reddit.
    -   **Landing Page Mode:** Generates a clean, static HTML landing page on GitHub Pages for all download links and posts a single link to it.
-   **Customizable HTML Templates:** The landing page can be fully customized using a powerful but simple placeholder and loop system.
-   **Community Feedback Monitoring:** Actively checks comments on Reddit posts for keywords to provide a real-time status (e.g., "Working", "Broken").
-   **Pure Python Toolchain:** The entire backend logic is written in Python for simplicity and consistency.
-   **Fast CI/CD:** Uses `uv` for rapid dependency installation in GitHub Actions.

## Documentation

For detailed information on how to set up, configure, and customize the bot, please see the comprehensive documentation in the `docs/` directory.

-   **[01 - Configuration](./docs/01-configuration.md):** A complete reference for every setting in `config.toml`.
-   **[02 - Templates & Customization](./docs/02-templates.md):** Instructions on how to customize the Reddit posts and landing page.
-   **[03 - Workflows](./docs/03-workflows.md):** An explanation of the GitHub Actions that automate the bot.
-   **[04 - Scripts](./docs/04-scripts.md):** A detailed breakdown of each Python script and its role.

## Project Structure

-   `.github/workflows/`: Contains the GitHub Actions workflows.
-   `docs/`: Contains all project documentation.
-   `src/`: Contains all Python source code.
-   `templates/`: Contains the Markdown and HTML templates.
-   `config.toml`: The main configuration file for the bot.
-   `requirements.txt`: A list of Python dependencies.
