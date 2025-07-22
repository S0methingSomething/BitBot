# BitBot Architectural Blueprint (v2 - Detailed)

This document provides a detailed architectural specification for the BitBot refactoring project. It serves as the definitive blueprint for all development work, defining not just the components but their specific responsibilities and interactions.

## 1. Core Principles

*   **Zero Trust Architecture:** No component trusts another by default. All actions that affect the outside world (network, file system) are brokered and permissioned.
*   **Single Responsibility Principle:** Each component (class, module) has one, and only one, reason to change. A `GitHubClient` only changes if the GitHub API changes.
*   **Explicit & Observable:** The bot's behavior is not hidden in complex logic. It is orchestrated through a central, observable broker, making its actions transparent and easy to debug.
*   **Configuration-Driven:** The bot's behavior is controlled by `config.toml`, not by its code.
*   **Developer Accountability:** All code changes must be accompanied by a formal, structured self-review to ensure quality beyond what automated tools can check.

## 2. The Component Model

The application is composed of several distinct types of components, each with a clearly defined role.

### 2.1. The Execution Broker (The "Central Nervous System")

This is the most critical component. It is the only part of the application with the authority to perform "dangerous" operations. All other components must submit requests to it.

*   **Location:** `src/bitbot/broker.py`
*   **Responsibilities:**
    1.  **Permissioning:** It holds a non-negotiable, hard-coded `Rulebook` that maps which services can access which resources.
        *   *Example Rule:* `ReleaseService` is allowed to request network calls via the `GitHubClient` and `RedditClient`.
        *   *Example Rule:* `CommunityService` is allowed to request file writes *only* to the path defined for the bot's state file.
    2.  **Execution:** It directly executes all I/O operations using the underlying libraries (`httpx`, `asyncpraw`, `pathlib`).
    3.  **Logging & Observability:** It generates a detailed, structured log of every request, permission check, execution, and result. This log is the primary tool for debugging.
*   **Key Methods (Conceptual):**
    *   `async request_network_call(requester, client_method, *args)`: Handles all API calls.
    *   `async request_file_read(requester, file_path)`: Handles all file reading.
    *   `async request_file_write(requester, file_path, content)`: Handles all file writing.

### 2.2. Clients (The "Tools")

Clients are stateless components that know how to communicate with a specific external API. They do not contain business logic. They are "dumb" tools that only know how to format requests and parse responses for one service.

*   **Location:** `src/bitbot/clients/`
*   **`GitHubClient` (`github.py`):**
    *   **Responsibilities:** Knows how to talk to the GitHub API via `httpx`.
    *   **Key Methods:** `async get_releases(repo)`, `async create_release(...)`, `async download_asset(...)`.
*   **`RedditClient` (`reddit.py`):**
    *   **Responsibilities:** Knows how to talk to the Reddit API via `asyncpraw`.
    *   **Key Methods:** `async submit_post(...)`, `async edit_post(...)`, `async get_comments(...)`.

### 2.3. Services (The "Brains")

Services contain the core business logic of the application. They orchestrate the Clients by making requests to the Execution Broker. They are the "workers" that make decisions.

*   **Location:** `src/bitbot/services/`
*   **`ReleaseService` (`release.py`):**
    *   **Responsibilities:** Implements the entire release workflow logic.
    *   **Logic Flow:**
        1.  Ask the Broker to call the `GitHubClient` to get new releases.
        2.  Parse the release descriptions to find a valid `bitbot` block.
        3.  If a new, valid release is found, ask the Broker to call the `GitHubClient` to download the asset.
        4.  Ask the Broker to call the `PatcherService` to patch the file.
        5.  Ask the Broker to call the `GitHubClient` to create a new release with the patched asset.
        6.  Ask the Broker to call the `RedditClient` to post about the new release.
*   **`PatcherService` (`patcher.py`):**
    *   **Responsibilities:** A pure, logic-only service that knows how to modify the `MonetizationVars` file content. It takes file content as input and returns modified file content as output. It performs no I/O itself.

### 2.4. Configuration (`settings.py` & `config.toml`)

This defines the user-controllable state of the bot.

*   **`config.toml`:** The human-readable control panel.
    ```toml
    # Example Structure
    [github]
    source_repo = "S0methingSomething/BitEdit"
    bot_repo = "S0methingSomething/BitBot"

    [reddit]
    subreddit = "BitTest1"
    post_title_template = "[BitBot] MonetizationVars for {{app_name}} v{{version}}"

    [[apps]]
    id = "bitlife"
    display_name = "BitLife"

    [[apps]]
    id = "bitlife_go"
    display_name = "BitLife Go"
    ```
*   **`settings.py`:** Contains the Pydantic models that validate the structure of `config.toml` at startup. If `config.toml` is invalid, the bot will refuse to start.

## 3. The Quality Mandate: Tools and Process

To ensure the highest quality, development will adhere to two levels of quality control: automated tooling and a formal self-review process.

### 3.1. The Automated Quality Framework

All code will be checked by the following tools on every commit:

| Tool      | Purpose                 |
| --------- | ----------------------- |
| `black`   | Code Formatting         |
| `ruff`    | Linting                 |
| `mypy`    | Static Type Checking    |
| `xenon`   | Complexity Analysis     |
| `pytest`  | Testing Framework       |
| `hypothesis`| Property-Based Testing  |

### 3.2. The Pre-Commit Self-Review Mandate

Automated tools are not enough. They cannot verify logical correctness or readability. Therefore, every commit must include a formal self-review checklist in its description. This makes the developer's internal quality check an explicit and auditable part of the project's history.

**The Checklist:**
1.  **Architectural Compliance:**
    *   Does this change adhere strictly to `ARCHITECTURE.md`?
    *   Does it go through the Execution Broker for all I/O?
    *   Is it in the correct module (`clients`, `services`)?
2.  **Correctness of Logic:**
    *   What is the intended purpose of the code?
    *   Has the logic been manually traced for a typical case?
3.  **Readability and Maintainability:**
    *   Are variable and function names clear and unambiguous?
    *   Is there any "magic" that should be a named constant or config value?
4.  **Testing Rigor:**
    *   Does the test suite cover the "happy path," the "sad path" (errors), and all relevant edge cases (`None`, empty lists, etc.)?

## 4. Detailed Workflow Example: `manage-releases`

This trace shows how the components interact to perform the main release task.

1.  **User/CI:** Executes the command `bitbot release manage`.
2.  **`main.py` (CLI):**
    *   Initializes the `Settings` object by loading `config.toml`.
    *   Initializes the `ExecutionBroker`.
    *   Initializes all clients (`GitHubClient`, `RedditClient`).
    *   Initializes the `ReleaseService`, passing the `ExecutionBroker` to it.
    *   Calls `await release_service.run()`.
3.  **`ReleaseService`:**
    *   Calls `await self.broker.request_network_call(requester=self, target=self.github_client.get_releases, ...)`.
4.  **`ExecutionBroker`:**
    *   Receives the request.
    *   **Permission Check:** Consults its `Rulebook`. Is `ReleaseService` allowed to call `GitHubClient.get_releases`? Yes.
    *   **Logging:** Logs "PERMISSION GRANTED".
    *   **Execution:** Calls `await self.github_client.get_releases(...)` itself.
    *   **Logging:** Logs the result (e.g., "SUCCESS, found 2 releases").
    *   Returns the list of releases to the `ReleaseService`.
5.  **`ReleaseService`:**
    *   Receives the releases and processes them. It finds a new valid release for the "bitlife" app.
    *   Calls `await self.broker.request_network_call(requester=self, target=self.github_client.download_asset, ...)`
6.  **`ExecutionBroker`:**
    *   ... (approves, logs, executes, logs, returns the local file path) ...
7.  **`ReleaseService`:**
    *   ... continues this request-approve-execute cycle for patching the file, creating the new release, and finally posting to Reddit. If any step fails, the Broker's log will show the exact point of failure.

## 5. Target Project Structure

```
/workspaces/BitBot/
├── ARCHITECTURE.md
├── config.toml
├── pyproject.toml
├── src/
│   └── bitbot/
│       ├── __init__.py
│       ├── main.py          # CLI Entrypoint
│       ├── broker.py        # The Execution Broker
│       ├── settings.py      # Pydantic Settings Models
│       ├── state.py         # Pydantic State Models
│       ├── clients/
│       │   ├── __init__.py
│       │   ├── github.py
│       │   └── reddit.py
│       └── services/
│           ├── __init__.py
│           ├── release.py
│           ├── community.py
│           └── patcher.py
└── tests/
    ├── __init__.py
    ├── test_broker.py
    ├── test_settings.py
    └── ...
```

## 6. Phased Implementation Plan

The project will be built in three phases. This architecture will be constructed piece by piece, starting with the Broker and a "Vertical Slice" in Phase 1 to validate the design, before the full feature set is implemented in Phase 2.
