#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# Clones one of your own repositories from GitHub.
# -----------------------------------------------------------------------------
import sys
from pathlib import Path

try:
    from git_tools import git_operations
    from git_tools.config import GITHUB_USERNAME
    from git_tools.exceptions import GitToolsError
    from git_tools.logging_config import setup_logging
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from git_tools import git_operations
    from git_tools.config import GITHUB_USERNAME
    from git_tools.exceptions import GitToolsError
    from git_tools.logging_config import setup_logging

def main() -> None:
    """Parses arguments and orchestrates the clone operation."""
    setup_logging()
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <repo-name>", file=sys.stderr)
        sys.exit(1)

    repo_name = sys.argv[1]
    clone_url = f"git@github.com:{GITHUB_USERNAME}/{repo_name}.git"
    
    if Path(repo_name).exists():
        print(f"Error: A file or directory named '{repo_name}' already exists.", file=sys.stderr)
        sys.exit(1)

    try:
        print(f"Cloning '{clone_url}'...")
        # We don't use the quiet flag here so the user can see git's output
        git_operations.run_git_command(["clone", clone_url])
        print(f"\n✅ Successfully cloned '{repo_name}'.")
    except GitToolsError as e:
        print(f"\nError: Clone operation failed.\n{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
