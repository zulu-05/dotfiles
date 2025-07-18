#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# Uploads a local-only Git repository to GitHub.
# -----------------------------------------------------------------------------
import sys
from pathlib import Path

try:
    from git_tools import git_operations, github_api
    from git_tools.config import GITHUB_USERNAME
    from git_tools.exceptions import GitToolsError
    from git_tools.logging_config import setup_logging
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from git_tools import git_operations, github_api
    from git_tools.config import GITHUB_USERNAME
    from git_tools.exceptions import GitToolsError
    from git_tools.logging_config import setup_logging

def main() -> None:
    """Orchestrates the repository upload process."""
    setup_logging()
    repo_path = Path.cwd()
    repo_name = repo_path.name

    try:
        # Step 1: Validate local repository state
        if not git_operations.is_git_repository(repo_path):
            raise GitToolsError("This script must be run from the root of a Git repository.")
        
        if git_operations.get_remote_url(repo_path):
            raise GitToolsError("A remote named 'origin' already exists. This script is only for uploading new repos.")

        # Step 2: Create the remote repository
        github_api.create_github_repo(repo_name)

        # Step 3: Link local and remote, then push
        current_branch = git_operations.get_current_branch(repo_path)
        git_operations.set_remote_origin(repo_path, GITHUB_USERNAME, repo_name)
        git_operations.push_to_origin(repo_path, current_branch)

        print(f"\n✅ Successfully uploaded repository '{repo_name}' to GitHub!")

    except GitToolsError as e:
        print(f"\nError: Upload operation failed.\n{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
