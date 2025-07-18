#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# Renames a Git repository on both the local system and GitHub.
# Implements rollback for remote rename if local operations fail.
# -----------------------------------------------------------------------------
import sys
from pathlib import Path

try:
    from git_tools import git_operations, github_api, validation
    from git_tools.config import GITHUB_USERNAME
    from git_tools.exceptions import GitToolsError
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from git_tools import git_operations, github_api, validation
    from git_tools.config import GITHUB_USERNAME
    from git_tools.exceptions import GitToolsError


def main() -> None:
    """Orchestrates the transactional repository rename process."""
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <old_name> <new_name>", file=sys.stderr)
        sys.exit(1)

    old_name = sys.argv[1]
    new_name = sys.argv[2]
    old_path = Path.cwd() / old_name
    new_path = Path.cwd() / new_name

    if not old_path.is_dir():
        print(f"Error: Directory '{old_name}' not found.", file=sys.stderr)
        sys.exit(1)

    # Step 1: Validate the new name before any operations
    if not validation.validate_repo_name(new_name):
        sys.exit(1)

    owner = GITHUB_USERNAME # Assuming the user is renaming their own repo
    remote_renamed = False

    try:
        # Step 2: Rename repository on GitHub first
        github_api.rename_github_repo(owner, old_name, new_name)
        remote_renamed = True

        # Step 3: Perform local operations
        git_operations.rename_local_repo(old_path, new_path)
        git_operations.set_remote_origin(new_path, owner, new_name)

        print(f"\n✅ Successfully renamed '{old_name}' to '{new_name}'.")

    except GitToolsError as e:
        print(f"\nError: An operation failed: {e}", file=sys.stderr)

        # ROLLBACK LOGIC
        if remote_renamed:
            print(f"Attempting to roll back GitHub rename...")
            try:
                github_api.rename_github_repo(owner, new_name, old_name)
                print("Rollback successful. GitHub repo is back to its original name.")
            except GitToolsError as rollback_e:
                print(
                    "\nCRITICAL ERROR: FAILED TO ROLL BACK GITHUB RENAME.\n"
                    f"The GitHub repository is named '{new_name}', but the local "
                    f"directory is still '{old_name}'. Manual intervention is required.\n"
                    f"Rollback error: {rollback_e}",
                    file=sys.stderr
                )
        sys.exit(1)


if __name__ == "__main__":
    main()
