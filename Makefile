.PHONY: setup check fix test test-all

VENV_DIR := .venv
UV := uv
SRC_DIR := src

setup:
	@echo ">>> Installing uv if not present..."
	@command -v uv >/dev/null 2>&1 || { echo "Installing uv..."; curl -LsSf https://astral.sh/uv/install.sh | sh; }
	@echo ">>> Setting up Python 3.13 environment..."
	$(UV) venv --python 3.13 $(VENV_DIR)
	@echo ">>> Installing dependencies..."
	$(UV) pip install -e .[dev]

check:
	@echo ">>> Running ruff checks..."
	$(UV) run ruff check $(SRC_DIR)
	@echo ">>> Running mypy type checks..."
	$(UV) run mypy $(SRC_DIR)
	@echo ">>> Running xenon complexity checks..."
	$(UV) run xenon --max-absolute B --max-modules A --max-average A $(SRC_DIR)

test:
	@echo ">>> Running pytest..."
	$(UV) run pytest

test-all:
	@echo ">>> Running pytest..."
	$(UV) run pytest

fix:
	@echo ">>> Running ruff to auto-fix files..."
	$(UV) run ruff check --fix $(SRC_DIR)
