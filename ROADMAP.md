# BitBot Development Roadmap

This document tracks the planned work for the BitBot project. It is organized by development phase and serves as the official checklist for the refactoring effort and future feature development.

## Phase 1: The Foundation

**Goal:** Build a stable, modern project structure with an integrated quality framework and a working `async` prototype that validates our `ApplicationCore` architecture.

*   [x] **Task 1: Establish Automated Quality Framework**
    *   [x] Create and configure `pyproject.toml` with strict, pragmatic rules.
    *   [x] Add and configure `uv`, `black`, `ruff`, `mypy`, `xenon`.
    *   [x] Create `Makefile` for convenience commands.
    *   [x] Add and configure `pre-commit`.
*   [x] **Task 2: Define Core Dependencies & Project Structure**
    *   [x] Add `async`-native libraries: `httpx`, `asyncpraw`.
    *   [x] Add testing libraries: `pytest`, `pytest-asyncio`, `hypothesis`.
    *   [x] Add core libraries: `pydantic-settings`, `tomlkit`.
    *   [x] Create `src/bitbot` package structure and all sub-packages.
*   [x] **Task 3: Build the "Vertical Slice" Prototype**
    *   [x] Implement the `ApplicationCore` skeleton in `src/bitbot/core.py`.
    *   [x] Implement the **context-based** Execution Broker with detailed logging (`who`, `what`, `why`, `context`, `payload`).
    *   [x] Implement the **family of context-aware decorators** (`@core.requires_file_read`, etc.) with mandatory `why` fields.
    *   [x] Implement Pydantic `Settings` models with `pydantic-settings`.
    *   [x] Implement the `bitbot check-config` CLI command.
*   [x] **Task 4: Validate the Testing Methodology**
    *   [x] Write `hypothesis` and `pytest` tests for the `ApplicationCore`'s settings loader and the Broker's context-based rules to prove the testing protocol works.

---

## Phase 2: Feature Implementation

**Goal:** Implement the bot's core business logic on top of the new, stable foundation, adhering to the `ApplicationCore` architecture.

*   [x] **Task 1: Implement Core Services & Domain Models**
    *   [x] Implement `FeatureRegistry` and `features.toml`.
    *   [x] Build `WorkspaceService` using the new decorator model.
    *   [x] Build `ApiClientService` skeleton.
    *   [x] Build `OrchestrationService` skeleton.
    *   [x] Create Pydantic domain models for Reddit objects (for the Adapter Pattern).
*   [x] **Task 2: Implement API Clients**
    *   [x] Build `GitHubClient`, with all methods using the `@core.requires_network_call` decorator.
    *   [x] Build `RedditClient`, implementing the **Adapter Pattern** and using decorators.
*   [x] **Task 3: Implement Orchestration Logic**
    *   [x] Implement the main release workflow in `OrchestrationService`, using `@core.requires_feature` to guard optional logic.
    *   [x] Implement the branching logic for the `post_style` feature flag.
    *   [x] Implement the "Post Linter" safety check.
*   [x] **Task 4: Implement Python-Native Patcher**
    *   [x] Rewrite the `process_vars.js` logic in a pure Python service.
*   [x] **Task 5: Write Comprehensive Tests**
    *   [x] Add full, TDD-style test coverage for all new services and clients.

---

## Phase 3: Integration and Finalization

**Goal:** Connect the features to the outside world, finalize the CLI, and document the project.

*   [x] **Task 1: Build Out the CLI**
    *   [x] Implement all user-facing commands in `main.py`, connecting them to the `OrchestrationService`.
*   [x] **Task 2: Update CI/CD Workflows**
    *   [x] Modify `.github/workflows/` to use the new `bitbot` CLI commands.
    *   [x] Ensure CI fails if any quality check fails.
*   [x] **Task 3: Write Documentation**
    *   [x] Create a user-focused `README.md`.
    *   [x] Update `ARCHITECTURE.md` with any final implementation details.

---

## Future Enhancements (Post-Refactor)

This is a backlog of Quality of Life (QoL) features and other ideas to be prioritized after the core refactoring is complete.

*   [ ] **Feature: App Management CLI**
    *   Implement `bitbot new-app` to automatically add a new application to the config and update templates.
*   [ ] **Feature: Dry Run Mode**
    *   Add a `--dry-run` flag to all state-changing commands to preview actions without executing them.
*   [ ] **Feature: Automated Diagnostics**
    *   Implement `bitbot diagnose` to check credentials, validate templates, and sync state.
*   [ ] **Feature: Advanced Feedback Analysis**
    *   Add state to the feedback system to track comment history and provide more nuanced status updates.
*   [... More ideas to be added here ...]