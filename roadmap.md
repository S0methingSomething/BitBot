# BitBot Refactoring Roadmap

This document outlines the step-by-step plan to refactor the BitBot project into a modern, robust, and maintainable Python application.

---

### **Phase 1: Foundation & Project Setup (Complete)**

*Goal: Establish the new structure and install our quality-control tools.*

- [x] **Create `pyproject.toml`**
- [x] **Implement the `src` Layout**
- [x] **Initial Code Cleanup**

---

### **Phase 2: Service-Oriented Refactoring (Complete)**

*Goal: Decouple all logic into independent, testable services using Dependency Injection (DI).*

- [x] **Create Data Models**
- [x] **Build the Service Container**
- [x] **Implement Services**

---

### **Phase 3: Testing & Type Safety (Complete)**

*Goal: Build a powerful automated safety net to guarantee correctness.*

- [x] **Enforce Strict Typing**
- [x] **Test Critical Code with `Hypothesis`**
- [x] **Unit Test Application Logic**

---

### **Phase 4: Integration & Automation (In Progress)**

*Goal: Connect the new architecture to the outside world and automate all quality checks in CI/CD.*

- [x] **Create `scripts` Entry Points**
- [x] **Update GitHub Actions for Deployments**
- [ ] **Update GitHub Actions for CI Checks**

---

### **Phase 5: Reddit Feature Implementation (To Do)**

*Goal: Re-implement all Reddit-related features on top of the new architecture.*

- [ ] **Reddit Post Generation:** Create a `RedditPostService` that uses templates to generate post titles and bodies from a changelog.
- [ ] **Reddit Post Management:** Implement the logic to decide whether to create a new post or update an existing one based on the 7-day rule.
- [ ] **Reddit Comment Analysis:** Create a `CommentAnalysisService` to parse comments for user feedback.
- [ ] **State Synchronization:** Implement the logic to synchronize the local `bot_state.json` with the live Reddit post.
- [ ] **Repository Maintenance:** Create a `MaintenanceService` to mark old GitHub releases with an `[OUTDATED]` prefix.
