# Contributing to BitBot

First off, thank you for considering contributing to BitBot! Whether you're fixing a bug, adding a new feature, or improving documentation, your help is appreciated.

This document provides guidelines for contributing to this project. Please read it carefully to ensure that your contributions are merged smoothly.

## Getting Started

1.  **Fork the repository** on GitHub.
2.  **Clone your fork** locally: `git clone https://github.com/your-username/BitBot.git`
3.  **Set up the development environment**:
    ```bash
    cd BitBot
    uv venv
    source .venv/bin/activate
    uv pip install -r requirements.txt -r requirements-dev.txt
    pre-commit install
    ```

## Running Checks and Tests

Before submitting a pull request, please ensure that your changes pass all the checks and tests.

1.  **Run the pre-commit hooks** on all files:
    ```bash
    pre-commit run --all-files
    ```
    This will run `ruff`, `black`, and `mypy` to format, lint, and type-check the code.

2.  **Run the tests**:
    ```bash
    uv run pytest
    ```

## Coding Style

*   **Follow the PEP 8 style guide.**
*   **Use type hints** for all function signatures.
*   **Use the logger** for all output. Do not use `print` statements.
*   **Keep functions small and focused.** If a function is getting too long or complex, refactor it into smaller functions.
*   **Write docstrings** for all modules, classes, and functions.

## Commit Messages

*   **Use the imperative mood** in the subject line (e.g., "Add new feature" not "Added new feature").
*   **Keep the subject line short** (under 50 characters).
*   **Use the body to explain what and why** vs. how.
*   **Reference any issues** that the commit addresses.

By following these guidelines, you'll help us maintain a high-quality codebase and make the project easier for everyone to contribute to.
