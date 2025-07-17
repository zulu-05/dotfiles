#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# Clones one of your own repositories from GitHub.
#
# This script provides a simple wrapper around 'git clone' to quickly
# download one of your own repositories using a consistent SSH URL format.
# -----------------------------------------------------------------------------
import os
import sys
import subprocess
from git_api_helpers import GITHUB_USERNAME

def download_repo(repo_name):
    """
    Checks for conflicts and clones a specified repository from GitHub
    using an SSH URL.
    """
    # --- 1. Check for local conflicts ---
    print(f"--> Preparing to clone '{repo_name}'...")
    if os.path.exists(repo_name):
        print(f"Error: A directory or file named '{repo_name}' already exists in this location.", file=sys.stderr)
        sys.exit(1)

    # --- 2. Construct URL and Execute Clone ---
    clone_url = f"git@github.com:{GITHUB_USERNAME}/{repo_name}.git"
    print(f"--> Executing: git clone {clone_url}")

    try:
        # We don't capture output here, so the user sees git's progress directly.
        subprocess.run(
            ["git", "clone", clone_url],
            check=True
        )
    except FileNotFoundError:
        print("Error: The 'git' command was not found. Is Git installed and in your PATH?", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError:
        # Git already prints detailed errors to stderr (e.g., repo not found, no access).
        # We just add a concluding message.
        print("\nError: 'git clone' failed. Please check the error message above.", file=sys.stderr)
        print(f"Verify that the repository '{GITHUB_USERNAME}/{repo_name}' exists and you have access.", file=sys.stderr)
        sys.exit(1)

    print(f"\n✅ Successfully cloned '{repo_name}'.")

def main():
    """Parses command-line arguments and initiates the download."""
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <repo-name>", file=sys.stderr)
        sys.exit(1)

    repo_to_download = sys.argv[1]
    download_repo(repo_to_download)

if __name__ == "__main__":
    main()
