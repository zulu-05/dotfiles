# `git_tools` Library Architecture

This document provides a deep dive into the internal architecture of the Python command-line tools.

## Core Philosophy

The primary design goal is the **separation of concerns** between the user-facing executables and the underlying logic.

-   **Executables (in `bin/`)**: These are thin wrappers responsible only for parsing command-line arguments and presenting user-friendly output. They contain no complex logic.
-   **Library (in `bin/git_tools/`)**: This is a robust, well-structured Python library that encapsulates all the complex functionality, including API calls, subprocess management, and error handling.

This two-layer architecture makes the system highly maintainable, testable, and easy to extend.

---

## Module Breakdown

The `git_tools` library is organized into several modules, each with a distinct responsibility:

| Module              | Description                                                                         |
| ------------------- | ----------------------------------------------------------------------------------- |
| `github_api.py`     | Handles all REST API communication with GitHub.                                     |
| `git_operations.py` | Manages all local `git` commands via a secure subprocess wrapper.                   |
| `validation.py`     | Provides functions for validating user input (e.g., repo names, URLs).              |
| `exceptions.py`     | Defines the custom `GitToolsError` hierarchy for standardized error handling.       |
| `config.py`         | Manages the lazy-loaded, cached retrieval of secrets (username, token) from `pass`. |
| `logging_config.py` | Provides a centralized setup for application logging.                               |
| `ui.py`             | Contains the presentation logic for the interactive `list_git_repos.py`.            |

---

## Key Design Patterns

### Centralized Error Handling

All functions within the `git_tools` library raise a `GitToolsError` (or one of its subclasses) upon failure. The top-level executable scripts do not handle these errors individually. Instead, they wrap their main logic in a single `try...except` block.

**Example (`create_git_repo.py`):**

```python
def main() -> None:
    try:
        # All calls to the library happen here.
        git_operations.initialize_local_repo(...)
        github_api.create_github_repo(...)
        git_operations.push_to_origin(...)

    except GitToolsError as e:
        # If any library function fails, it is caught here.
        # This provides a single, consistent point for reporting errors to the user.
        print(f"\nError: An operation failed: {e}", file=sys.stderr)
        sys.exit(1)
```

This pattern keeps the executables clean and ensures that all errors, regardless of their origin, are presented to the user in a uniform way.

### Transactional Safety 

For operations that involve multiple critical steps (like renaming a repository), the system attempts to be transactional. It tries to complete all steps, but if a later step fails, it will attempt to roll back the earlier steps.

**Example (`rename_git_repo.py`):**

1. **Attempt Remote Rename:** The script first calls `github_api.rename_github_repo()` to rename the repository on GitHub.
   
2. **Attempt Local Operations:** If the remote rename succeeds, it then tries to rename the local directory and update the git remote URL.
   
3. **Rollback on Failure:** If any of the local operations fail, the `except` block is triggered. This block makes another call to `github_api.rename_github_repo()` to change the name on GitHub _back_ to its original state, preventing a mismatch between the local and remote repositories.

### Mock-Based Testing Strategy

The test suite, located in `bin/tests/`, is designed to be fast and reliable. It achieves this by **mocking** all external interactions.

- **Subprocess Calls:** Instead of running real `git` commands, tests use `pytest-mock` to patch `subprocess.run`. This allows us to verify that our functions are __trying__ to call `git` with the correct arguments, and to simulate both success and failure scenarios without touching the filesystem.
  
- **API Requests:** Instead of making real network calls to GitHub, tests patch `requests.request`. This allows us to simulate various API responses (e.g., success, "not found", "unauthorized") and confirm that our `github_api` module handles each case correctly.

- **Configuration Functions:** To isolate tests from the `pass` password manager, tests patch the functions in `config.py` (e.g., `config.get_github_token`). This allows us to inject fake secrets and test functions that rely on them without needing a real, configured `pass` environment.
