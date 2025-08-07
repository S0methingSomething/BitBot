# BitBot Architecture

This document outlines the target software architecture for the BitBot project. The goal of this architecture is to create a system that is maintainable, testable, decoupled, and easy to understand.

## Core Principles

-   **Service-Oriented:** The application's logic is broken down into distinct, single-responsibility services (e.g., `GitHubService`, `RedditService`).
-   **Dependency Injection (DI):** Services do not create their own dependencies. Instead, dependencies are "injected" by a central Service Container. This decouples the services and makes them highly testable.
-   **Clear Separation of Concerns:** The codebase is organized into distinct layers (Core, Services, Models, Entry Points) with clear responsibilities.
-   **Packaged Application:** The project is structured as a proper, installable Python package using the `src` layout.

## Directory Structure

The target directory structure is as follows:

```
/
├── .github/
├── bin/                      <-- Simple, executable entry-point scripts
├── docs/
├── src/
│   └── bitbot/               <-- The core, installable Python package
│       ├── __init__.py
│       ├── __main__.py         <-- Allows `python -m bitbot`
│       ├── core/               <-- DI Container, base classes
│       ├── models/             <-- Simple data classes (e.g., Release, App)
│       ├── services/           <-- All business logic (GitHub, Reddit, etc.)
│       └── utils/              <-- Reusable helper functions
├── templates/
├── tests/                    <-- All automated tests
├── bot_state.json
├── config.toml
├── pyproject.toml            <-- The single source of truth for the project
└── README.md
```

### Directory Responsibilities

-   **`src/bitbot/`**: The main Python package. All application code resides here.
    -   **`core/`**: Contains the application's central nervous system, most importantly the `ServiceContainer` which manages DI.
    -   **`models/`**: Contains simple, passive data structures (often dataclasses) that represent the core entities of the application (e.g., a `Release` object, an `App` configuration). These classes do not contain business logic.
    -   **`services/`**: Contains the application's business logic. Each file/class in this directory is responsible for one specific capability (e.g., `github_service.py` handles all interactions with the GitHub API).
    -   **`utils/`**: Holds small, reusable helper functions that don't fit into a specific service (e.g., date formatters, string manipulators).
-   **`bin/`**: Contains thin, executable scripts that serve as the application's entry points. Their only job is to initialize the `ServiceContainer`, retrieve the necessary top-level service, and execute a single method.
-   **`tests/`**: Contains all automated tests. The structure of this directory will mirror the `src/bitbot/` directory.
-   **`pyproject.toml`**: The unified project definition file. It manages dependencies, project metadata, and the configuration for all development tools (`ruff`, `mypy`, `pytest`).
