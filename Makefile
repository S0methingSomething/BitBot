.PHONY: setup check fix

VENV_DIR := .venv
PYTHON := $(VENV_DIR)/bin/python
SRC_DIR := src

setup:
	@echo ">>> Setting up virtual environment in $(VENV_DIR)..."
	python3 -m venv $(VENV_DIR)
	@echo ">>> Installing dependencies with uv..."
	$(PYTHON) -m pip install -q uv
	$(VENV_DIR)/bin/uv pip install -e .[dev]

check:
	@echo ">>> Running ruff checks..."
	$(PYTHON) -m ruff check $(SRC_DIR)
	@echo ">>> Running mypy type checks..."
	$(PYTHON) -m mypy $(SRC_DIR)
	@echo ">>> Running xenon complexity checks..."
	$(PYTHON) -m xenon --max-absolute B --max-modules A --max-average A $(SRC_DIR)

fix:
	@echo ">>> Running ruff to auto-fix files..."
	$(PYTHON) -m ruff check --fix $(SRC_DIR)
