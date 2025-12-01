.PHONY: all quick check lint format type test models beartype coverage clean

# Full CI suite (all checks)
all:
	@uv run python .github/scripts/quality.py all

# Quick checks (pre-commit style)
quick:
	@uv run python .github/scripts/quality.py quick

# Individual checks
lint:
	@uv run python .github/scripts/quality.py lint

format:
	@uv run ruff check --fix src/ tests/
	@uv run ruff format src/ tests/

type:
	@uv run python .github/scripts/quality.py type

test:
	@uv run python .github/scripts/quality.py test

models:
	@uv run python .github/scripts/quality.py models

beartype:
	@uv run python .github/scripts/quality.py beartype

# Tests with coverage
coverage:
	@uv run pytest tests/ -v --cov=src --cov-report=term-missing

# Pre-commit
pre-commit:
	@uv run pre-commit run --all-files

# Clean cache files
clean:
	@rm -rf .mypy_cache .pytest_cache .ruff_cache .coverage htmlcov dist/
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@echo "✓ Cleaned"
