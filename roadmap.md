# BitBot Refactoring Roadmap

This document outlines the step-by-step plan to refactor the BitBot project into a modern, robust, and maintainable Python application.

---

### **Phase 1: Foundation & Project Setup**

*Goal: Establish the new structure and install our quality-control tools.*

1.  **Create `pyproject.toml`:** This file will be created to define the project, its dependencies (`praw`, `requests`), and all development tools (`ruff`, `mypy`, `pytest`, `hypothesis`, `types-praw`, `types-requests`). The Python version will be set to `3.13`.
2.  **Implement the `src` Layout:**
    -   Create the `src/bitbot/` directory.
    -   Create the `tests/` directory.
    -   Move all existing `.py` files from the old `src/` into `src/bitbot/` to begin the refactoring process.
3.  **Initial Code Cleanup:** Run `ruff format .` and `ruff check --fix .` across the entire project. This ensures we start from a consistent, clean baseline.

---

### **Phase 2: Service-Oriented Refactoring**

*Goal: Decouple all logic into independent, testable services using Dependency Injection (DI).*

1.  **Create Data Models:** Inside `src/bitbot/models/`, define simple data classes to represent core objects like `Release`, `App`, and `BotState`.
2.  **Build the Service Container:** In `src/bitbot/core/container.py`, create the `ServiceContainer`. This class will be responsible for instantiating and providing all services, managing their dependencies automatically.
3.  **Implement Services:** Create the service classes inside `src/bitbot/services/`. The logic from the old scripts will be moved into these classes: `GitHubService`, `RedditService`, `FilePatcherService`, `ReleaseManagementService`, etc. Each service will be a focused, independent component.

---

### **Phase 3: Testing & Type Safety**

*Goal: Build a powerful automated safety net to guarantee correctness.*

1.  **Enforce Strict Typing:** Configure `mypy` to enforce strict type checking on the entire `src/bitbot/` package.
2.  **Test Critical Code with `Hypothesis`:** Write a property-based test for the `FilePatcherService` in `tests/`. This will rigorously test the file modification logic with a wide range of generated inputs, ensuring its absolute correctness.
3.  **Unit Test Application Logic:** Write `pytest` unit tests for at least one high-level service (e.g., `ReleaseManagementService`), using mocking to test its logic without making real network calls.

---

### **Phase 4: Integration & Automation**

*Goal: Connect the new architecture to the outside world and automate all quality checks in CI/CD.*

1.  **Create `bin` Entry Points:** The old scripts will be replaced by thin executable scripts in the `bin/` directory. These scripts will do nothing more than import the container, request a service, and run it.
2.  **Update GitHub Actions:** Modify all workflows in `.github/workflows/` to use the new structure and run our full suite of checks (`ruff`, `mypy`, `pytest`) on every single change. This will block any code that doesn't meet our quality standards.
