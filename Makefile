.PHONY: help install format lint typecheck complexity test check ci

help:
	@echo "Available commands:"
	@echo "  install      - Install all dependencies and set up the environment"
	@echo "  format       - Format the code (ruff format)"
	@echo "  lint         - Run the linter (ruff)"
	@echo "  typecheck    - Run the static type checker (mypy)"
	@echo "  complexity   - Run the complexity checker (xenon)"
	@echo "  test         - Run the test suite (pytest)"
	@echo "  check        - Run all checks (format, lint, typecheck, complexity, test)"
	@echo "  ci           - Alias for 'check'"

install:
	@echo "--- Installing dependencies and pre-commit hooks ---"
	uv pip install -e .'[dev]'
	uv run pre-commit install

format:
	@echo "--- Formatting code ---"
	uv run ruff format src/ tests/

lint:
	@echo "--- Running linter ---"
	uv run ruff check src/ tests/

typecheck:
	@echo "--- Running type checker ---"
	uv run mypy src/bitbot/

complexity:
	@echo "--- Running complexity checker ---"
	uv run xenon --max-absolute B --max-modules A --max-average A src/

test:
	@echo "--- Running tests ---"
	uv run pytest

check: format lint typecheck complexity test

ci: check
