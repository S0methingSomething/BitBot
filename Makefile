# Makefile for BitBot project

.PHONY: help check fix clean

help:
	@echo "Available commands:"
	@echo "  make check   - Run ruff linter and mypy type checker"
	@echo "  make fix     - Automatically fix issues with ruff"
	@echo "  make clean   - Remove cache directories"

check:
	@echo "Running linter and type checker..."
	uv run ruff check .
	uv run mypy .

fix:
	@echo "Automatically fixing issues with ruff..."
	uv run ruff check . --fix

clean:
	@echo "Removing cache directories..."
	rm -rf .mypy_cache .ruff_cache .pytest_cache
