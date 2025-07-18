#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# A script to list and inspect your GitHub repositories.
# -----------------------------------------------------------------------------
import sys
from pathlib import Path

try:
    from git_tools import github_api, ui
    from git_tools.exceptions import GitToolsError
    from git_tools.logging_config import setup_logging
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from git_tools import github_api, ui
    from git_tools.exceptions import GitToolsError
    from git_tools.logging_config import setup_logging

def main() -> None:
    """Fetches repos and launches the interactive UI."""
    setup_logging()
    try:
        repos = github_api.get_all_user_repos()
        if not repos:
            print("No repositories found.")
            return
        ui.run_repo_inspector_menu(repos)
    except GitToolsError as e:
        print(f"\nError: Could not retrieve repository list.\n{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
