#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# Deletes a Git repository from both the local system and GitHub.
# -----------------------------------------------------------------------------
import sys
import shutil
from pathlib import Path

try:
    from git_tools import git_operations, github_api, validation
    from git_tools.exceptions import GitToolsError
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from git_tools import git_operations, github_api, validation
    from git_tools.exceptions import GitToolsError


def main() -> None:
    """Orchestrates the repository deletion process."""
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <local_repo_directory_name>", file=sys.stderr)
        sys.exit(1)

    repo_dir_name = sys.argv[1]
    local_repo_path = Path.cwd() / repo_dir_name

    if not local_repo_path.is_dir():
        print(f"Error: The directory '{local_repo_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    try:
        # Step 1: Get remote URL and parse it
        remote_url = git_operations.get_remote_url(local_repo_path)
        if not remote_url:
            raise GitToolsError("Could not find a remote URL for 'origin'. Is this a GitHub repo?")

        parsed_url = validation.get_repo_from_remote_url(remote_url)
        if not parsed_url:
            raise GitToolsError(f"Could not parse GitHub info from URL: {remote_url}")
        owner, repo_name = parsed_url

        # Step 2: Get user confirmation
        try:
            prompt = (
                f"Are you sure you want to permanently delete '{owner}/{repo_name}' "
                f"from GitHub and the local directory '{local_repo_path}'? [y/N]: "
            )
            confirm = input(prompt)
        except (EOFError, KeyboardInterrupt):  # Handle non-interactive or Ctrl+C
            confirm = 'n'
            print("\nDeletion aborted by user.")

        if confirm.strip().lower() != 'y':
            print("Deletion aborted.")
            return

        # Step 3: Delete remote repository first
        github_api.delete_github_repo(owner, repo_name)

        # Step 4: If remote deletion succeeds, delete local directory
        print(f"Deleting local directory: {local_repo_path}...")
        shutil.rmtree(local_repo_path)
        print(f"Successfully deleted local directory.")

        print(f"\n✅ Successfully deleted '{repo_name}'.")

    except (GitToolsError, OSError) as e:
        print(f"\nError: An operation failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
