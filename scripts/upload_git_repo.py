#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# Uploads a local-only Git repository to GitHub.
#
# This script creates a new public repository on GitHub with the same name
# as the current directory, sets it as the 'origin' remote, and pushes
# the current branch.
# -----------------------------------------------------------------------------
import os
import sys
import subprocess
import requests
from git_api_helpers import GITHUB_USERNAME, get_github_token

def upload_repo():
    """The main logic for validating and uploading the repository."""
    # --- 1. Verify Local Git Repository State ---
    print("--> Verifying local Git repository...")
    try:
        # Check if inside a git repository
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=True, capture_output=True
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: This script must be run from the root of a Git repository.", file=sys.stderr)
        sys.exit(1)

    # Check if remote 'origin' already exists
    remotes = subprocess.check_output(["git", "remote"]).decode().strip().split('\n')
    if "origin" in remotes:
        print("Error: A remote named 'origin' already exists for this repository.", file=sys.stderr)
        print("This script is only for uploading local-only repositories.", file=sys.stderr)
        sys.exit(1)

    repo_name = os.path.basename(os.getcwd())
    print(f"--> Local repository '{repo_name}' is valid for upload.")

    # --- 2. Authenticate and Create GitHub Repository ---
    access_token = get_github_token()
    if not access_token:
        sys.exit(1)

    print(f"--> Creating GitHub repository '{GITHUB_USERNAME}/{repo_name}'...")
    api_url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    data = {"name": repo_name, "private": False}
    response = requests.post(api_url, headers=headers, json=data)

    if response.status_code == 422 and "already exists" in response.text:
        print(f"Error: A repository named '{repo_name}' already exists on GitHub.", file=sys.stderr)
        print("Please choose a different local directory name or delete the remote repository.", file=sys.stderr)
        sys.exit(1)
    elif response.status_code != 201:
        print(f"Failed to create GitHub repository. Status: {response.status_code}", file=sys.stderr)
        print("Response:", response.json(), file=sys.stderr)
        sys.exit(1)

    print("--> Successfully created GitHub repository.")

    # --- 3. Link Remote and Push ---
    remote_url = f"git@github.com:{GITHUB_USERNAME}/{repo_name}.git"
    try:
        print(f"--> Setting remote 'origin' to '{remote_url}'...")
        subprocess.run(["git", "remote", "add", "origin", remote_url], check=True)

        print("--> Pushing to GitHub...")
        # Get current branch name to push
        current_branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode().strip()
        subprocess.run(["git", "push", "-u", "origin", current_branch], check=True)

    except subprocess.CalledProcessError as e:
        print(f"Error during git remote or push operation: {e}", file=sys.stderr)
        print("The remote repository was created on GitHub, but you will need to manually set the remote and push.", file=sys.stderr)
        sys.exit(1)

    print("\n✅ Successfully uploaded repository to GitHub!")

def main():
    upload_repo()

if __name__ == "__main__":
    main()

