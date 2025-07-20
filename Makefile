.PHONY: all setup format lint test

all: format lint test

setup:
	@echo "Setting up the development environment..."
	@python3 -m venv .venv
	@.venv/bin/pip install uv
	@.venv/bin/uv pip install -e ".[dev]"
	@echo "Environment setup complete."

format:
	@echo "Formatting the code..."
	@.venv/bin/black .
	@.venv/bin/ruff check . --fix
	@echo "Formatting complete."

lint:
	@echo "Linting the code..."
	@.venv/bin/ruff check .
	@.venv/bin/mypy .
	@PYTHONPATH=src python scripts/lint_architecture.py
	@echo "Linting complete."

test:
	@echo "Running tests..."
	@.venv/bin/pytest
	@.venv/bin/mutmut run
	@.venv/bin/xenon --max-absolute B --max-modules A --max-average A .
	@echo "Tests complete."

test-debug:
	@echo "Running tests in debug mode..."
	@.venv/bin/pytest --log-cli-level=DEBUG
	@echo "Tests complete."