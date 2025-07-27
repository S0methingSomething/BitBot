# Makefile for BitBot

.PHONY: help install lint format check-types complexity test all

# Colors
GREEN := \033[0;32m
YELLOW := \033[0;33m
RESET := \033[0m

help:
	@echo "Available commands:"
	@echo "  ${YELLOW}install${RESET}        - Install dependencies using uv"
	@echo "  ${YELLOW}lint${RESET}           - Run ruff linter"
	@echo "  ${YELLOW}format${RESET}         - Run black formatter and ruff to fix issues"
	@echo "  ${YELLOW}check-types${RESET}    - Run mypy for static type checking"
	@echo "  ${YELLOW}complexity${RESET}      - Run xenon for complexity analysis"
	@echo "  ${YELLOW}test${RESET}           - Run pytest for all tests"
	@echo "  ${YELLOW}all${RESET}            - Run all checks (lint, format, types, complexity, test)"

install:
	@echo "${GREEN}Installing dependencies...${RESET}"
	uv pip install -e .[dev]

lint:
	@echo "${GREEN}Running linter...${RESET}"
	uv run ruff check src/

format:
	@echo "${GREEN}Formatting code...${RESET}"
	uv run black src/
	uv run ruff check src/ --fix

check-types:
	@echo "${GREEN}Checking types...${RESET}"
	uv run mypy src/

complexity:
	@echo "${GREEN}Analyzing complexity...${RESET}"
	uv run xenon --max-absolute B --max-modules A --max-average A src/ -i src/bitbot/main.py

test:
	@echo "${GREEN}Running tests...${RESET}"
	uv run pytest

all: lint format check-types complexity test
	@echo "${GREEN}All checks passed!${RESET}"
