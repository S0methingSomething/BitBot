# BitBot Architectural Blueprint (v6 - Final & Complete)

This document provides the definitive architectural specification for the BitBot project. All development must adhere strictly to this blueprint.

## 1. Core Principles

*   **Centralized Core:** All cross-cutting concerns (configuration, logging, permissions, state) are managed by a single, unified `ApplicationCore`.
*   **Zero Trust & Context-Based Permissions:** No service can perform I/O or access resources without explicit, context-aware permission from the Core's Execution Broker.
*   **Declarative & Intentional Logic:** Services declare their needs and intent using a family of context-aware decorators. Business logic must be clean and separate from infrastructure concerns.
*   **Single Responsibility:** Each component has one, and only one, reason to change.
*   **Untyped Library Containment:** Interactions with untyped libraries must be contained within an **Adapter** that translates their objects into our trusted Pydantic domain models.
*   **Developer Accountability:** All commits must include the formal "Pre-Commit Self-Review" checklist.
*   **Maximum Observability:** The system must produce detailed, structured logs that tell a complete, story-like narrative of every operation, including the data payloads involved.

## 2. The `ApplicationCore` Architecture

The application is built around a central `ApplicationCore` that provides all essential infrastructure services.

### 2.1. The `ApplicationCore` (`core.py`)

This is the heart of the application, initialized once at startup. It is responsible for creating and managing all other components, including the Broker, the Feature Registry, and the family of decorators.

### 2.2. The Context-Based Execution Broker

The Broker is the engine of our Zero Trust and Observability principles. It is the only component that performs I/O.

*   **Responsibilities:**
    1.  **Permissioning:** Maintains a rulebook that grants or denies actions based on the requesting service and the **context** of the request (e.g., the specific file path).
    2.  **Execution:** Executes the requested action (e.g., file read, network call).
    3.  **Detailed Logging:** Before and after execution, it logs the **WHO** (requester), **WHAT** (action), **WHY** (business intent), **CONTEXT** (arguments), and the **PAYLOAD** (the actual data being written or sent).

### 2.3. The Feature Registry (`features.toml`)

A simple, declarative registry of the bot's capabilities, loaded by the `ApplicationCore`. This allows services to be decoupled from each other and provides a master on/off switch for major functionalities.

### 2.4. The Decorator Model (The Primary Interface)

Services interact with the Core and Broker almost exclusively through a consistent, declarative "family of decorators".

*   **Permission & Feature Decorators (The `@requires_...` family):**
    *   These decorators act as gateways, ensuring a function only runs if its preconditions are met. They are context-aware and require a `why` argument where appropriate to state business intent.
    *   **`@core.requires_feature("feature_name")`**: Ensures the function only runs if the named feature is enabled in `features.toml`.
    *   **`@core.requires_file_read(path_arg="...", why="...")`**: Checks permission for reading a specific file.
    *   **`@core.requires_file_write(path_arg="...", content_arg="...", why="...")`**: Checks permission for writing to a specific file.
    *   **`@core.requires_network_call(why="...")`**: Checks permission for making an external API call.

*   **Infrastructure Decorators:**
    *   These decorators handle common, repetitive tasks, keeping the business logic in services clean.
    *   **`@core.log_entry_exit(log_args=["..."])`**: Handles detailed, structured logging for method entry, exit, duration, and status.
    *   **`@core.skip_in_dry_run(log_args=["..."])`**: Prevents a method from executing its logic when the bot is in "dry run" mode.
    *   **`@core.handle_errors_with(...)`**: Provides a clean way to wrap methods in a `try...except` block for graceful error handling.

### 2.5. Core Services

Services contain the application's business logic. They are orchestrated by the `ApplicationCore` and use decorators to interact with the Broker.

*   **`WorkspaceService`:** Manages file system interactions.
*   **`ApiClientService`:** Manages external API communication (contains `GitHubClient`, `RedditClient`).
*   **`OrchestrationService`:** The central "brain" containing high-level business logic.

## 3. Posting Strategy & Safety Mechanisms

To mitigate the risk of being flagged as spam by Reddit, the bot supports two distinct posting strategies, controlled by a feature flag in `config.toml`.

### 3.1. Configuration

```toml
[reddit]
post_style = "landing_page" # "direct_links" or "landing_page"
max_outbound_links_warning = 5
```

### 3.2. `landing_page` Workflow (Default & Recommended)

The bot posts a single link to a consolidated GitHub Release.

1.  The `OrchestrationService` aggregates all new app releases for the cycle.
2.  It generates a detailed markdown body using a `github_release_template.md`.
3.  It requests the `ApiClientService` to create a single, consolidated GitHub release.
4.  It then generates a simple Reddit post body using `reddit_landing_page_template.md`, which contains only a single link to the new GitHub release.
5.  It requests the `ApiClientService` to submit this simple post to Reddit.

### 3.3. `direct_links` Workflow (Legacy & High-Risk)

The bot posts all download links directly to Reddit and uses a "Post Linter" to warn if the link count exceeds the configured threshold.

1.  The `OrchestrationService` generates a complex Reddit post body.
2.  **Post Linter:** Before submitting, the service performs a "lint check" on the generated markdown.
3.  It requests the `ApiClientService` to submit the post to Reddit.

## 4. The Quality Mandate

All development will adhere to the strict automated quality framework (`black`, `ruff`, `mypy`, `xenon`) and the mandatory "Pre-Commit Self-Review" checklist.

## 5. Target Project Structure

The project structure will include a `templates/` directory for the new templates.

```
/workspaces/BitBot/
├── ARCHITECTURE.md
├── ROADMAP.md
├── config.toml
├── pyproject.toml
├── Makefile
├── src/
│   └── bitbot/
│       ├── __init__.py
│       ├── main.py
│       ├── core.py
│       ├── domain/
│       │   └── models.py
│       └── services/
│           ├── __init__.py
│           ├── workspace.py
│           ├── api_clients.py
│           ├── orchestrator.py
│           └── patcher.py
├── templates/
│   ├── github_release_template.md
│   ├── inject_template.md
│   ├── post_landing_page_template.md
│   └── post_direct_links_template.md
└── tests/
    └── ...
```

*Note: The architecture diagram should be updated to include the `PatcherService`.*

## 6. Phased Implementation Plan

The project will be built in three phases, as outlined in `ROADMAP.md`.
