# BitBot Project Context

## Project Overview

BitBot is an automated release management and announcement bot designed to monitor a source GitHub repository for new releases, patch asset files, create corresponding releases on its own repository, and announce them on Reddit. The project is built to be highly modular, configurable, and maintainable.

### Core Features

- **Automated Release Patching**: Monitors a source repository and automatically downloads, patches, and re-releases assets.
- **Structured Release Parsing**: Uses a robust, key-value format in release notes for reliable app detection.
- **Dual Reddit Posting Modes**: Direct Link Mode (individual download links) and Landing Page Mode (static HTML landing page).
- **Customizable HTML Templates**: The landing page can be fully customized using a placeholder and loop system.
- **Community Feedback Monitoring**: Actively checks comments on Reddit posts for keywords to provide real-time status updates.
- **Pure Python Toolchain**: Backend logic written in Python for simplicity and consistency.
- **Fast CI/CD**: Uses `uv` for rapid dependency installation in GitHub Actions.
- **GitHub Codespaces Friendly**: TOML-based credential management for persistent storage.
- **Multi-Level Dry-Run Support**: Five levels of dry-run mode for testing different scenarios.

## Project Structure

```
BitBot/
├── .github/workflows/     # GitHub Actions workflows
├── docs/                  # Project documentation
├── src/                   # Python source code
├── templates/             # Markdown and HTML templates
├── tests/                 # Test files
├── config.toml            # Main configuration file
├── credentials.example.toml # Example credentials file
├── Makefile               # Build and run commands
├── pyproject.toml         # Python project configuration
├── README.md              # Project documentation
└── requirements.txt       # Python dependencies
```

## Technology Stack

- **Language**: Python 3.13
- **Dependency Management**: `uv` for fast dependency installation
- **Package Management**: `pyproject.toml` with optional dev dependencies
- **Testing**: `pytest` with `hypothesis` for property-based testing
- **Code Quality**: `ruff` for linting, `mypy` for type checking, `xenon` for complexity analysis
- **Documentation**: Markdown files in `docs/` directory
- **External APIs**: GitHub API via `gh` CLI, Reddit API via `praw`
- **Templating**: Custom HTML templating engine with loops and conditionals
- **Logging**: Custom logging with `rich` for styled console output

## Configuration

The project uses TOML-based configuration files:

1. **Main Configuration**: `config.toml` contains all bot settings
2. **Credentials**: `credentials.toml` (gitignored) stores API keys and secrets
3. **Templates**: Files in `templates/` directory for Reddit posts and landing pages

Key configuration sections include:
- Authentication settings
- GitHub repository configuration
- Reddit posting settings
- Safety features
- Feedback analysis
- Deployment settings

## Core Components

### 1. Release Management (`src/release_manager.py`)
- Monitors source GitHub repository for new releases
- Parses structured release descriptions
- Downloads and patches asset files
- Creates new releases in the bot repository

### 2. Reddit Posting (`src/post_to_reddit.py`)
- Generates Reddit post content from templates
- Supports both direct link and landing page modes
- Posts to Reddit with appropriate formatting
- Manages post updates and status monitoring

### 3. Landing Page Generation (`src/page_generator.py`)
- Creates static HTML landing pages
- Uses customizable templates with placeholder system
- Supports deployment to GitHub Pages and Cloudflare Pages

### 4. Comment Monitoring (`src/check_comments.py`)
- Analyzes Reddit comments for feedback keywords
- Updates post status based on community feedback
- Implements adaptive polling intervals

### 5. File Patching (`src/patch_file.py`)
- Decrypts, modifies, and re-encrypts asset files
- Sets boolean values to true for monetization

### 6. Digest Aggregation (`src/digest_aggregator.py`)
- Collects releases over time for weekly digest posts
- Formats changelog for digest posts

### 7. Deployment Services (`src/deployment.py`)
- Supports multiple deployment targets (GitHub Pages, Cloudflare Pages)
- Handles deployment configuration and execution

## Dry-Run Levels

BitBot supports five different dry-run levels for testing:

1. **Level 0 (FULL_DRY_RUN)**: No external interactions at all
2. **Level 1 (READ_ONLY)**: Allows external read operations only
3. **Level 2 (SAFE_WRITES)**: Allows safe write operations
4. **Level 3 (PUBLIC_PREVIEW)**: Allows public preview operations
5. **Level 4 (PRODUCTION)**: Full production mode

These can be controlled through:
- `DRY_RUN_LEVEL` environment variable (0-4)
- `DRY_RUN` environment variable (named modes)
- Configuration in `config.toml`

## Development Workflow

### Setup
```bash
make setup        # Install dependencies using uv
```

### Testing
```bash
make test         # Run pytest
make pytest-dry-run # Run tests in dry-run mode
```

### Code Quality
```bash
make check        # Run linters and type checking
make fix          # Auto-fix code formatting issues
```

### Running
```bash
make dry-run      # Run in dry-run mode for testing
make run          # Run in production mode
```

## Credential Management

BitBot supports multiple credential management approaches:

1. **Environment Variables**: Default method using standard environment variables
2. **GitHub Codespaces Persistent Storage**: TOML-based automatic save/load
3. **Configuration-Based**: Auto-load from `credentials.toml` file
4. **Local Configuration File**: Manual configuration in `credentials.toml`

## Data Flow

1. **Release Detection**: Monitor source repository for new releases
2. **Release Processing**: Download, patch, and re-release assets
3. **Data Generation**: Create `releases.json` with release information
4. **Landing Page**: Generate static HTML page with app information
5. **Reddit Posting**: Create and post announcement to Reddit
6. **Comment Monitoring**: Monitor feedback and update post status
7. **Digest Aggregation**: Collect releases for weekly digest posts

## State Management

The bot maintains several state files:
- `bot_state.json`: Tracks post IDs, versions, and monitoring intervals
- `release_state.json`: Tracks processed source release IDs
- `dist/releases.json`: Contains release data for the current cycle
- `dist/data/digest_history.json`: Tracks releases for digest aggregation

## Deployment

The bot is designed to run in GitHub Actions workflows but can also be run locally. It supports deployment to:
- GitHub Pages
- Cloudflare Pages (planned)

## Testing Strategy

- Unit tests with `pytest`
- Property-based testing with `hypothesis`
- Dry-run modes for integration testing
- Mock services for external API testing

## Documentation

Comprehensive documentation is available in the `docs/` directory:
1. Configuration reference
2. Templates and customization guide
3. Workflow explanations
4. Script breakdowns