# Contributing to BitBot

This document outlines the contribution guidelines for the BitBot project. By participating in this project, you agree to abide by these guidelines.

## Development Environment

This project uses `uv` for virtual environment and package management, and a `Makefile` to simplify the development process. All dependencies are managed in `pyproject.toml`. Python 3.13 is the required version.

To set up your development environment, simply run:

```bash
make setup
```

This will create a virtual environment, install all the necessary dependencies, and get you ready to start coding.

## Development Commands

The `Makefile` provides several commands to help with development:

-   `make setup`: Set up the development environment.
-   `make lint`: Run linters and type checkers.
-   `make format`: Format the code.
-   `make test`: Run tests.
-   `make clean`: Remove temporary files.


## Toolchain

This project enforces a strict set of tools to ensure code quality, consistency, and correctness. All contributions must pass checks from these tools. The configuration for these tools is located in `pyproject.toml`.

-   **Linter:** [Ruff](https://github.com/astral-sh/ruff) (configured for strict checking with multiple rule sets)
-   **Formatter:** [Black](https://github.com/psf/black)
-   **Type Checker:** [Mypy](http://mypy-lang.org/) (configured for strict checking)
-   **Security Scanner:** [Bandit](https://github.com/PyCQA/bandit)
-   **Test Runner:** [Pytest](https://pytest.org/)
-   **Test Coverage:** [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/) (with a minimum coverage of 90%)
-   **Property-based Testing:** [Hypothesis](https://hypothesis.works/)
-   **Mutation Testing:** [Mutmut](https://mutmut.readthedocs.io/en/latest/)
-   **Docstring Style:** Google-style, enforced by `pydocstyle` via `ruff`.
-   **Pre-commit Hooks:** This project uses `pre-commit` to automate checks before each commit.

## Coding Style

-   All code must be formatted with `black`.
-   All code must pass `ruff` and `mypy` checks with the project's strict configuration.
-   All functions and methods must have type hints.
-   All public modules, classes, functions, and methods must have docstrings following the Google style guide.

## Testing

-   All new features must be accompanied by tests.
-   All bug fixes must include a regression test.
-   The test suite must pass with 100% coverage.

## CI/CD

The project uses GitHub Actions for continuous integration. The CI pipeline runs all the checks mentioned above on every push and pull request. The workflows are defined in the `.github/workflows` directory. There are three main workflows:
- `main.yml`: Manages the release process, including checking for new releases, patching files, and posting to Reddit.
- `check_comments.yml`: Periodically checks for new comments on Reddit posts and updates the post status.
- `maintain_releases.yml`: Marks old GitHub releases as outdated.

