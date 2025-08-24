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
-   **GitHub Codespaces Friendly:** TOML-based credential management for persistent storage in Codespaces.
-   **Multi-Level Dry-Run Support:** Five levels of dry-run mode for testing different interaction scenarios.

## Dry-Run Levels

BitBot supports five different dry-run levels for testing various scenarios:

### Level 0: `FULL_DRY_RUN`
- **No external interactions at all**
- Simulates all operations without making any API calls
- Perfect for local development and testing

### Level 1: `READ_ONLY`  
- **Allows external read operations only**
- Can fetch data from GitHub/Reddit but no writes
- Useful for testing data retrieval

### Level 2: `SAFE_WRITES`
- **Allows safe write operations**
- Can write files and make safe API calls (no public posts)
- Good for testing file operations and safe writes

### Level 3: `PUBLIC_PREVIEW`
- **Allows public preview operations**
- Creates drafts/previews instead of live posts
- Perfect for testing the full workflow without public exposure

### Level 4: `PRODUCTION`
- **Full production mode**
- All operations allowed, no dry-run restrictions
- Default behavior when no dry-run settings are specified

## Production Deployment

To run BitBot in production mode:

1. **Set up credentials**:
   ```bash
   cp credentials.example.toml credentials.toml
   # Edit credentials.toml with your actual credentials
   ```

2. **Configure auto-loading** in `config.toml`:
   ```toml
   [auth]
   auto_load = true    # Automatically load from credentials.toml
   auto_save = false   # Set to true if you want to save env vars
   ```

3. **Run in production mode**:
   ```bash
   make run
   ```

   Or manually:
   ```bash
   python src/main.py
   ```

## Usage Examples

```bash
# Level 0: Full dry-run (default for development)
export DRY_RUN_LEVEL=0
python src/main.py

# Level 1: Read-only mode
export DRY_RUN_LEVEL=1
python src/main.py

# Level 3: Public preview mode
export DRY_RUN_LEVEL=3
python src/main.py

# Named modes also work
export DRY_RUN=PUBLIC_PREVIEW
python src/main.py

# Production mode (no dry-run)
unset DRY_RUN_LEVEL
unset DRY_RUN
python src/main.py

# Or use make commands
make dry-run  # Dry-run mode
make run      # Production mode
```

## Credentials Management

BitBot supports multiple ways to manage credentials:

### Environment Variables (Default)
Set these in your environment:
```bash
export GITHUB_TOKEN="ghp_your_token"
export REDDIT_CLIENT_ID="your_client_id"
export REDDIT_CLIENT_SECRET="your_client_secret"
export REDDIT_USERNAME="your_username"
export REDDIT_PASSWORD="your_password"
export REDDIT_USER_AGENT="BitBot by /u/your_username"
```

### GitHub Codespaces Persistent Storage (TOML Format)
For GitHub Codespaces, you can save/load credentials automatically using TOML format:

1. **Save credentials to file:**
```bash
# Set your credentials in environment variables
export GITHUB_TOKEN="ghp_your_token"
export REDDIT_CLIENT_ID="your_client_id"
# ... etc

# Save them to credentials.toml
export BITBOT_SAVE_CREDS=1
python src/main.py
```

2. **Load credentials from file:**
```bash
# Auto-load saved credentials
export BITBOT_LOAD_CREDS=1
python src/main.py

# Or configure in config.toml:
# [auth]
# auto_load = true
```

### Configuration-Based Credential Management
Enable automatic credential loading in `config.toml`:
```toml
[auth]
auto_load = true  # Automatically load credentials from credentials.toml
auto_save = false # Set to true to automatically save credentials
```

### Local Configuration File (TOML Format)
Copy `credentials.example.toml` to `credentials.toml` and fill in your values:
```bash
cp credentials.example.toml credentials.toml
# Edit credentials.toml with your actual credentials
```

The credentials file uses TOML format:
```toml
[github]
token = "ghp_your_github_token_here"

[reddit]
client_id = "your_reddit_client_id"
client_secret = "your_reddit_client_secret"
username = "your_reddit_username"
password = "your_reddit_password"
user_agent = "BitBot by /u/your_username"
```

**Note:** `credentials.toml` is gitignored and will never be committed.

## Documentation

For detailed information on how to set up, configure, and customize the bot, please see the comprehensive documentation in the `docs/` directory.

-   **[01 - Configuration](./docs/01-configuration.md):** A complete reference for every setting in `config.toml`.
-   **[02 - Templates & Customization](./docs/02-templates.md):** Instructions on how to customize the Reddit posts and landing page.
-   **[03 - Workflows](./docs/03-workflows.md):** An explanation of the GitHub Actions that automate the bot.
-   **[04 - Scripts](./docs/04-scripts.md):** A detailed breakdown of each Python script and its role.

## Local Development & Dry-Run Modes

To facilitate local development and testing without interacting with external services (GitHub, Reddit), two dry-run modes are available:

1.  **Simulation Dry-Run**: Runs the actual bot scripts in a simulated environment without external interactions.
2.  **Pytest Dry-Run**: Runs the test suite in a dry-run environment to ensure all components work correctly.

### Simulation Dry-Run

To run the bot in simulation dry-run mode locally:

1.  Ensure you have Python 3.13 and `uv` installed.
2.  Set up your environment:
    ```bash
    make setup
    ```
3.  Run the simulation dry-run target:
    ```bash
    make dry-run
    ```

This will execute all the main components of the bot with simulated interactions, preventing any actual posts or releases.

### Pytest Dry-Run

To run the test suite in a dry-run environment:

1.  Ensure you have Python 3.13 and `uv` installed.
2.  Set up your environment:
    ```bash
    make setup
    ```
3.  Run the pytest dry-run target:
    ```bash
    make pytest-dry-run
    ```

This will run all the tests with the `DRY_RUN` environment variable set, ensuring that the tests can run without external dependencies.

### Code Quality Checks

To run the code quality checks:

```bash
make check
```

To automatically fix code quality issues:

```bash
make fix
```

## Project Structure

-   `.github/workflows/`: Contains the GitHub Actions workflows.
-   `docs/`: Contains all project documentation.
-   `src/`: Contains all Python source code.
-   `templates/`: Contains the Markdown and HTML templates.
-   `config.toml`: The main configuration file for the bot.
-   `requirements.txt`: A list of Python dependencies.
