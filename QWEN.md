# BitBot Project Context

## Project Overview

BitBot is an automated release management and announcement bot written in Python. Its primary purpose is to monitor a source GitHub repository for new releases, automatically download, patch, and re-release assets to its own repository, and then announce these updates on Reddit.

### Core Features

- **Automated Release Patching**: Monitors a source repository, downloads assets, patches them (e.g., setting boolean values to `true`), and creates corresponding releases on the bot's repository.
- **Structured Release Parsing**: Uses a key-value format in source release notes for reliable identification of apps and versions.
- **Dual Reddit Posting Modes**:
  - **Direct Link Mode**: Posts individual download links for each updated app directly to a Reddit post.
  - **Landing Page Mode**: Generates a static HTML landing page (hosted via GitHub Pages) listing all download links and posts a single link to this page.
- **Customizable HTML Templates**: The landing page and Reddit posts can be fully customized using templates with a placeholder and loop system.
- **Community Feedback Monitoring**: Monitors comments on Reddit posts for keywords (e.g., "working", "broken") to update the post's status dynamically.
- **Multi-Level Dry-Run Support**: Five levels of dry-run mode (`FULL_DRY_RUN`, `READ_ONLY`, `SAFE_WRITES`, `PUBLIC_PREVIEW`, `PRODUCTION`) for safe testing and development.
- **Pure Python Toolchain**: Backend logic implemented entirely in Python.
- **Fast CI/CD**: Uses `uv` for rapid dependency installation in GitHub Actions.
- **GitHub Codespaces Friendly**: TOML-based credential management for persistent storage in Codespaces.

## Project Structure

```
.
├── .github/workflows/     # GitHub Actions workflows
├── docs/                  # Project documentation
├── src/                   # Python source code
├── templates/             # Markdown and HTML templates
├── tests/                 # Python test suite
├── config.toml            # Main configuration file
├── credentials.example.toml # Example credentials file
├── Makefile               # Commands for setup, running, testing
├── pyproject.toml         # Python project and dependency configuration
├── README.md              # Project README
├── QWEN.md                # This file
```

## Key Technologies

- **Language**: Python 3.13+
- **Dependency Management & Virtual Environments**: `uv`
- **Dependencies**:
  - `praw`: Reddit API wrapper
  - `requests`: HTTP library
  - `toml`: TOML file parser
  - `packaging`: Utilities for versioning
  - `PyGithub`: GitHub API wrapper
  - `pydantic`: Data validation and settings management
  - `rich`: Rich text and beautiful formatting in the terminal
- **Development Dependencies**:
  - `ruff`: Linter and formatter
  - `mypy`: Static type checker
  - `xenon`: Code complexity analyzer
  - `pytest`: Testing framework
  - `hypothesis`: Property-based testing library
- **Configuration**: TOML files (`config.toml`, `credentials.toml`)
- **Deployment**: GitHub Actions, GitHub Pages

## Building, Running, and Testing

### Prerequisites

- Python 3.13
- `uv` (for fast dependency installation)

### Setup

```bash
make setup
```
This command installs `uv` if not present, creates a Python 3.13 virtual environment, and installs all project dependencies (including development dependencies) using `uv`.

### Running the Bot (Production)

1. **Configure credentials**:
   - Copy `credentials.example.toml` to `credentials.toml` and fill in your actual credentials.
   - Or set credentials as environment variables.
   - Or use GitHub Codespaces persistent storage.
2. **Ensure `config.toml` is correctly configured.**
3. **Run the bot**:
   ```bash
   make run
   ```
   Or manually:
   ```bash
   python src/main.py
   ```

### Dry-Run Modes

BitBot supports five dry-run levels for testing:
- **Level 0 (`FULL_DRY_RUN`)**: No external interactions.
- **Level 1 (`READ_ONLY`)**: Allows external read operations only.
- **Level 2 (`SAFE_WRITES`)**: Allows safe write operations.
- **Level 3 (`PUBLIC_PREVIEW`)**: Allows public preview operations (e.g., creating drafts).
- **Level 4 (`PRODUCTION`)**: Full production mode (default when no dry-run settings are specified).

Example usage:
```bash
# Level 0: Full dry-run (default for development)
export DRY_RUN_LEVEL=0
python src/main.py

# Level 3: Public preview mode
export DRY_RUN_LEVEL=3
python src/main.py

# Production mode (no dry-run)
unset DRY_RUN_LEVEL
unset DRY_RUN
python src/main.py

# Makefile targets
make dry-run  # Runs in dry-run mode (Level 0)
make run      # Runs in production mode
```

### Running Tests

```bash
# Run the test suite
make test

# Run tests in dry-run mode
make pytest-dry-run
```

### Code Quality Checks

```bash
# Run linters, type checker, and complexity checks
make check

# Automatically fix code quality issues (where possible)
make fix
```

## Development Conventions

- **Python Version**: Python 3.13 is the target.
- **Code Style**: Enforced by `ruff` with a configuration targeting high-quality, readable code.
  - Line length: 88 characters (Black standard).
  - Strict selection of linting rules (E, W, F, I, B, Q, T20, SIM, PT, RET, PTH, RUF, UP, N, S, A, C4, PIE, PL, PERF, SLF, ARG).
  - McCabe complexity threshold set to 10.
- **Type Checking**: Strict `mypy` configuration.
- **Testing**: `pytest` is used for testing. Tests should be comprehensive and cover different dry-run scenarios.
- **Code Complexity**: Monitored with `xenon`, aiming for low complexity (max absolute B, modules A, average A).
- **Dry-Run Support**: Core components are designed to operate under different dry-run levels to prevent unintended external interactions during development and testing.
- **Configuration**: Uses `pydantic` for robust configuration loading and validation from `config.toml`.
- **Logging**: Uses Python's `logging` module with `rich` for enhanced terminal output.
- **Documentation**: Comprehensive documentation is located in the `docs/` directory, covering configuration, templates, workflows, and scripts.
