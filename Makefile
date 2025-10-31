.PHONY: check lint type test coverage format clean all

# Run all checks
all: lint type test

# Run all checks with coverage
check: lint type coverage

# Linting
lint:
	@echo "Running ruff..."
	uv run ruff check src/ tests/

# Type checking
type:
	@echo "Running mypy..."
	uv run mypy src/

# Run tests
test:
	@echo "Running pytest..."
	uv run pytest tests/ -v

# Run tests with coverage
coverage:
	@echo "Running pytest with coverage..."
	uv run pytest tests/ -v --cov=src --cov-report=term-missing

# Format code
format:
	@echo "Formatting with ruff..."
	uv run ruff check --fix src/ tests/
	uv run ruff format src/ tests/

# Clean cache files
clean:
	@echo "Cleaning cache files..."
	rm -rf .mypy_cache .pytest_cache .ruff_cache .coverage htmlcov
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
