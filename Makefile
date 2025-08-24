.PHONY: setup check fix test test-all dry-run run pytest-dry-run

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
	uv run ruff check src
	@echo ">>> Running mypy type checks..."
	uv run mypy src
	@echo ">>> Running xenon complexity checks..."
	uv run xenon --max-absolute B --max-modules A --max-average A src --exclude src/utils/config_loader.py,src/credentials.py

test:
	@echo ">>> Running pytest..."
	$(UV) run pytest

test-all:
	@echo ">>> Running pytest..."
	$(UV) run pytest

fix:
	@echo ">>> Running ruff to auto-fix files..."
	$(UV) run ruff check --fix $(SRC_DIR)

# Production run target for actual execution
run:
	@echo ">>> Running BitBot in production mode..."
	@echo ">>> Checking credentials..."
	@if [ ! -f "credentials.toml" ]; then \
		echo "Error: credentials.toml not found!"; \
		echo "   Create it by copying credentials.example.toml:"; \
		echo "   cp credentials.example.toml credentials.toml"; \
		echo "   Then edit credentials.toml with your actual credentials."; \
		exit 1; \
	fi
	@echo ">>> Running release manager..."
	$(UV) run python src/reddit_release_manager.py
	@echo ">>> Running page generator..."
	$(UV) run python src/page_generator.py
	@echo ">>> Running Reddit post script..."
	$(UV) run python src/post_to_reddit.py
	@echo ">>> Running comment checker..."
	$(UV) run python src/check_comments.py
	@echo ">>> Production execution complete."

# Dry-run target for local testing without external service interactions
dry-run:
	@echo ">>> Running BitBot in dry-run mode..."
	@echo ">>> Creating mock releases.json for page generator..."
	@mkdir -p dist
	@echo '{"bitlife": {"display_name": "BitLife", "latest_release": {"version": "4.2.0", "download_url": "https://example.com/bitlife-v4.2.0", "published_at": "2025-08-20T10:00:00Z"}}}' > dist/releases.json
	@echo ">>> Running release manager..."
	$(UV) run env DRY_RUN=true python src/reddit_release_manager.py
	@echo ">>> Running page generator..."
	$(UV) run env DRY_RUN=true python src/page_generator.py
	@echo ">>> Running Reddit post script..."
	$(UV) run env DRY_RUN=true python src/post_to_reddit.py
	@echo ">>> Running comment checker..."
	$(UV) run env DRY_RUN=true python src/check_comments.py
	@echo ">>> Dry-run execution complete."

# Pytest-based dry-run target for running tests in a dry-run environment
pytest-dry-run:
	@echo ">>> Running pytest in dry-run mode..."
	$(UV) run env DRY_RUN=true pytest
