# BitBot

BitBot is a Reddit bot that helps you manage release posts for your projects.

## Getting Started

To get started with BitBot, you'll need to have Python 3.8+ and `make` installed.

### Setup

To set up the development environment, run the following command:

```bash
make setup
```

This will:

1.  Install `uv`, a high-performance Python package installer.
2.  Create a virtual environment.
3.  Install all project dependencies.
4.  Install the `pre-commit` hooks.

Once the setup is complete, activate the virtual environment:

```bash
source .venv/bin/activate
```

## Usage

The bot provides three commands to manage your Reddit release posts.

### Post a new release

Use the `post` command to create a new release post on Reddit.

```bash
bitbot post --version <version> --direct-download-url <url>
```

### Synchronize post history

Use the `sync` command to synchronize your Reddit post history with your GitHub releases. This ensures that older posts are updated correctly.

```bash
bitbot sync
```

### Check for comments

Use the `check` command to monitor the active post for new comments and update its status based on user feedback.

```bash
bitbot check
```

## Configuration

The bot is configured using the `config.toml` file. This file contains all the settings for the bot, including GitHub repositories, Reddit settings, and message formats.

The bot's state is stored in the `bot_state.toml` file. This file is created and managed automatically by the bot.

## Contributing

Contributions are welcome! Please see the [contributing guidelines](CONTRIBUTING.md) for more information.
