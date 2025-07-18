#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# Creates a local Git repository, a corresponding remote on GitHub,
# and pushes the initial commit.
#
# This script is a high-level wrapper around the git_tools library.
# -----------------------------------------------------------------------------
import sys
from pathlib import Path

# It's good practice to add the project root to the path if running scripts directly
# This makes imports more reliable.
try:
    from git_tools import git_operations, github_api
    from git_tools.config import GITHUB_USERNAME
    from git_tools.exceptions import GitToolsError
except ImportError:
    # This block allows the script to be run from the root directory
    # without having to install the package.
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from git_tools import git_operations, github_api
    from git_tools.config import GITHUB_USERNAME
    from git_tools.exceptions import GitToolsError


def main() -> None:
    """
    Main function to orchestrate the repository creation process.
    """
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <repo_name>", file=sys.stderr)
        sys.exit(1)

    repo_name = sys.argv[1]
    repo_path = Path.cwd() / repo_name

    try:
        # Step 1: Set up the local repository
        git_operations.initialize_local_repo(repo_path, repo_name)

        # Step 2: Create the remote repository on GitHub
        github_api.create_github_repo(repo_name)

        # Step 3: Create an initial commit if needed
        if git_operations.create_initial_commit(repo_path):
            # Step 4: Link the local and remote repos and push
            git_operations.set_remote_origin(repo_path, GITHUB_USERNAME, repo_name)
            git_operations.push_to_origin(repo_path)
        else:
            print("Skipping push because there are no new commits to send.")

        print(f"\n✅ Successfully processed repository '{repo_name}'.")

    except GitToolsError as e:
        print(f"\nError: An operation failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
