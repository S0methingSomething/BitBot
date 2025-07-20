# BitBot Refactoring Design & Implementation Plan

This document outlines the phased plan to refactor the BitBot application to the target state described in `ARCHITECTURE.md`. The primary goals are to fix the current testing failures, improve resilience, and establish a professional, maintainable codebase.

## Guiding Principles for Implementation

- **Strict Quality Gates:** Every change will be validated against our full toolchain: `ruff` (strict), `mypy`, `black`, `bandit`, `hypothesis`, `pytest-cov` (>90%), `mutmut`, and `xenon`.
- **`uv` Exclusively:** All dependency management will be handled by `uv`.
- **Iterative Progress:** The refactoring is broken into logical phases. The goal is to have a stable, testable application at the end of each phase.

---

## Phase 1: Foundational Stability & Testability

**Goal:** Fix the immediate testing crisis and establish a clean, testable core. This phase is about creating a stable foundation.

### Detailed Task Breakdown

#### 1. Finalize Directory Structure & File Placement
- **Task:** Ensure all files are in their correct locations as per the new architecture.
- **Completed:**
    - `src/bitbot/data/`, `src/bitbot/interfaces/`, `src/bitbot/services/` created.
    - `templates/` and `data/` created at the project root.
    - `.md` files moved to `templates/`.
    - `bot_state.json` moved to `data/`.
    - `config.json` converted to `config.toml` and moved to the root.
    - `.gitignore` updated to exclude the `data/` directory and `config.toml`.

#### 2. Implement Pydantic Data Models
- **Task:** Define all core data structures as Pydantic models for automatic validation.
- **File:** `src/bitbot/data/models.py`
- **Implementation Details:**
    - **`Settings`:** Will use `pydantic-settings` to load all required API keys and secrets directly from environment variables. This will be the single source of truth for secrets.
    - **`AppConfig`:** Will define the structure for an individual application.
    - **`Config`:** Will define the entire structure of `config.toml`. The `apps` field will be a list of `AppConfig` objects. This model will validate the entire configuration file on load.
    - **`BotState`:** Will define the structure of `bot_state.json`.
    - **`RedditPost` & `GitHubRelease`:** Will serve as data transfer objects (DTOs) to decouple our business logic from the raw API responses.

#### 3. Define Synchronous Service Protocols
- **Task:** Create the initial, synchronous contracts for our services. This simplifies the initial refactor and allows us to focus on structure before adding the complexity of `async`.
- **Location:** `src/bitbot/interfaces/`
- **Implementation Details:**
    - All methods will be standard `def`, not `async def`.

#### 4. Implement the Test Framework
- **Task:** Build the testing infrastructure that will allow us to write clean, reliable, and data-driven tests.
- **Implementation Details:**
    - **`tests/config.toml`:**
        - Will contain all mock data needed for testing.
        - This allows us to change test scenarios without changing test code.
    - **`tests/base.py`:**
        - The `BaseTestCase` will be created.
        - Its `setUp` method will read `tests/config.toml` and create mock instances of all our service protocols.
        - These mocks will be pre-configured with the data from the TOML file.
    - **`tests/mocks.py`:**
        - This file will contain simple, in-memory mock implementations of our protocols.

#### 5. Fix All Existing Tests
- **Task:** Rewrite every test file to use the new framework.
- **Implementation Details:**
    - Each test class will inherit from `BaseTestCase`.
    - All `patch()` decorators for file I/O and API clients will be **removed**.
    - The tests will be rewritten to call the business logic functions, passing in the mock managers provided by the base class.
    - Assertions will be made against the mock managers.

**Exit Criteria for Phase 1:**
- The project has a clean, well-organized directory structure.
- All existing unit tests pass reliably.
- `make format` and `make lint` commands pass without error.
- The core architectural patterns (DI, Protocols) are in place.
- The test suite is data-driven and no longer relies on `patch`.
