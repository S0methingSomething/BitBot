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
	@echo "Linting complete."

test:
	@echo "Running tests..."
	@.venv/bin/pytest
	@echo "Tests complete."

test-debug:
	@echo "Running tests in debug mode..."
	@.venv/bin/pytest --log-cli-level=DEBUG
	@echo "Tests complete."
