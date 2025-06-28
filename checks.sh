#!/bin/bash
# A script to run all format, lint, and test checks.
# Exits immediately if any command fails.
set -e

# --- Helper functions for colored output ---
color_green() {
    echo -e "\033[32m$1\033[0m"
}
color_yellow() {
    echo -e "\033[33m$1\033[0m"
}

# --- Run Checks ---
echo
color_yellow "--- 1. Running all pre-commit hooks (black, ruff, mypy) ---"
pre-commit run --all-files

# echo
# color_yellow "--- 2. Running tests with pytest and checking coverage ---"
# pytest --cov=bitbot

echo
color_green "✅ All format and lint checks passed successfully! ✨"
