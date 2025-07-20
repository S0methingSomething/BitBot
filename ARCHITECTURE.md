# BitBot Architecture

This document outlines the target architecture for the BitBot application. The design prioritizes modularity, testability, resilience, and maintainability, following professional software engineering principles.

## 1. Core Principles

- **Protocol-Oriented Design:** The system is built around interfaces (Protocols), not concrete implementations. Business logic depends only on these protocols, allowing for complete decoupling.
- **Dependency Injection (DI):** Components do not create their own dependencies. Instead, dependencies are "injected" from an external source (the Composition Root). This is the key to making the system testable.
- **Single Responsibility Principle (SRP):** Each module and class has one, and only one, reason to change. Logic for handling files is separate from logic for handling APIs, which is separate from business logic.
- **Async First:** All I/O-bound operations (file access, network requests) are designed to be asynchronous from the ground up to ensure performance and scalability.
- **Configuration as Code:** The bot's behavior is primarily driven by declarative configuration (`config.toml`), not hard-coded logic.
- **Resilience by Design:** The system anticipates failure (e.g., API outages, corrupted data) and handles it gracefully through retries, structured error handling, and atomic operations.

## 2. Component Breakdown

The application is divided into several distinct layers, each with a clear responsibility.

### a. The Composition Root (`src/bitbot/cli.py`)

- **Responsibility:** To initialize the application and compose the object graph.
- **Details:** This is the main entry point. Its *only* job is to:
    1.  Load environment-specific settings (e.g., from a `.env` file).
    2.  Use the `Service Factory` to create the concrete instances of all services.
    3.  Inject these services into the appropriate business logic functions.
    4.  Handle top-level exceptions and present user-friendly error messages.
- **It contains NO business logic.**

### b. Data Models (`src/bitbot/data/models.py`)

- **Responsibility:** To define the shape and validation rules for all data structures.
- **Details:** This module contains all Pydantic `BaseModel` classes (`Config`, `BotState`, `Settings`, `RedditPost`, etc.).
    - **Pydantic:** Used for automatic type coercion, validation, and clear error messages on malformed data (e.g., an invalid `config.toml`).
    - **Versioning:** Models like `BotState` and `Config` will have a `version` field to allow for safe data migration in the future.

### c. Interfaces (`src/bitbot/interfaces/`)

- **Responsibility:** To define the contracts that connect the application's layers.
- **Details:** This directory contains all the `typing.Protocol` definitions. These are the abstract blueprints for our services. Business logic modules will only ever import from here, never from the concrete services.
    - `ConfigManagerProtocol`, `StateManagerProtocol`, `RedditManagerProtocol`, etc.

### d. Services (`src/bitbot/services/`)

- **Responsibility:** To implement the logic for interacting with the outside world (files, APIs, etc.).
- **Details:** These are the concrete implementations of the protocols.
    - **`file_*.py` managers:** Handle all file I/O. They know how to read `.toml` and read/write `.json`. They use `aiofiles` for async operations and perform atomic writes for safety.
    - **`praw_manager.py`:** The *only* module in the entire application that is allowed to `import asyncpraw`. It encapsulates all logic for interacting with the Reddit API. It implements retry logic using `tenacity`.
    - **`github_manager.py`:** The *only* module that uses `aiohttp`. It handles GitHub API interaction and also has `tenacity`-based retry logic.
    - **`factory.py`:** Contains the `create_services` function. It reads the `Settings` model and instantiates the concrete services, wiring them together.

### e. Core Logic (`src/bitbot/history.py`, `src/bitbot/comments.py`, etc.)

- **Responsibility:** To orchestrate the application's business processes.
- **Details:** These modules contain the "brains" of the bot.
    - They are pure, stateless functions.
    - They are fully `async`.
    - They **only depend on protocols** from the `interfaces` directory, which are passed in as function arguments (DI).
    - They contain no `praw`, `aiohttp`, or file I/O code.

## 3. Data and Control Flow

A typical command (`bitbot sync`) flows through the system as follows:

1.  **`cli.py`:** The `main` function is called.
2.  **`cli.py`:** It instantiates the Pydantic `Settings` model, which loads environment variables.
3.  **`cli.py`:** It calls the `factory.create_services(settings)` function.
4.  **`factory.py`:** The factory creates instances of `FileStateManager`, `PrawManager`, etc.
5.  **`cli.py`:** The `main` function calls `history.sync_history()`, passing the service instances as arguments.
6.  **`history.py`:** The `sync_history` function uses the injected managers (e.g., `await github_manager.get_latest_release()`) to perform its logic, never knowing what the concrete implementation is.

This strict, unidirectional flow makes the system predictable and easy to debug.
