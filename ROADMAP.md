# BitBot Refactoring Roadmap

This document outlines the agreed-upon plan to incrementally refactor the BitBot codebase to use a broker system with Pydantic models for improved robustness, observability, and ease of feature implementation.

The core principle is an **in-place refactor**: enhancing individual scripts with the new architecture internally, without changing the project's overall file structure or the way GitHub Actions workflows call the scripts.

---

## The Plan

### Step 1: Build the Broker and Pydantic Foundation

-   [ ] Create the core files for the new system in `src/bitbot/`:
    -   [ ] `models.py`: Define all Pydantic models for `config.toml` and `bot_state.json`. This serves as a strict "contract" for all data.
    -   [ ] `context.py`: Implement the `AppContext` broker class. This class will be responsible for loading the configuration (using the Pydantic models), setting up structured logging, and managing access to components.
    -   [ ] `decorators.py`: Create the `@brokered_action` decorator. This will be the primary tool for logging actions and enforcing the "why" justification.
    -   [ ] `logging_config.py`: Configure the structured logger (e.g., using `logging.dictConfig`).

### Step 2: Incrementally Refactor Each Script

For each script in the `src/` directory (starting with the simplest ones like `maintain_releases.py` and moving to more complex ones like `release_manager.py`), perform the following:

-   [ ] **Bootstrap the Broker:** At the `if __name__ == "__main__":` block of the script, initialize the `AppContext`.
-   [ ] **Convert Logic to a Class:** Move the script's core logic into a dedicated class (e.g., `MaintainReleases` in `maintain_releases.py`).
-   [ ] **Inject the Context:** Pass the `AppContext` instance to the new class's constructor.
-   [ ] **Wrap Methods with Decorators:** Apply the `@brokered_action` decorator to methods that perform file I/O, API calls, or run subprocesses. Ensure a `why: str` argument is added to these methods.
-   [ ] **Replace Direct Calls:** Update the internal logic of the class to use the brokered methods instead of direct calls (e.g., call `self.run_gh_command(...)` instead of `subprocess.run(...)`).
-   [ ] **Use Pydantic Models:** Replace all unsafe dictionary access (`config['github']['botRepo']`) with safe Pydantic model access (`config.github.botRepo`).

### Step 3: Clean Up and Verify

-   [ ] After all scripts have been refactored, remove the now-redundant functions from `helpers.py`.
-   [ ] Ensure the entire codebase passes `make check` with zero errors.
-   [ ] Manually trigger a workflow run to confirm the end-to-end process still works as expected.