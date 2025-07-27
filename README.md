# BitBot

BitBot is a Reddit bot for managing and posting GitHub releases. It is designed to be a flexible and extensible platform for automating the release announcement process.

## Features

*   **Automated Release Management:** BitBot can monitor a GitHub repository for new releases, create corresponding releases in a bot-specific repository, and post announcements to Reddit.
*   **Flexible Posting Strategies:** BitBot supports two posting strategies: `landing_page` (posts a single link to a consolidated GitHub release) and `direct_links` (posts all download links directly to Reddit).
*   **Pluggable Services:** BitBot is built with a pluggable architecture, allowing for easy extension and customization.
*   **Configuration-Driven:** All aspects of BitBot's behavior are controlled by a simple TOML configuration file.

## Usage

1.  **Install dependencies:**
    ```bash
    make install
    ```

2.  **Configure the bot:**
    Create a `config.toml` file with your desired settings. See `config.example.toml` for an example.

3.  **Run the bot:**
    ```bash
    bitbot manage-releases
    ```

## Development

To run the tests:
```bash
make test
```
