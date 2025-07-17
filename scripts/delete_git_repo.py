#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# Deletes a Git repository from both the local system and GitHub.
# -----------------------------------------------------------------------------
import os
import sys
import subprocess
import requests
import shutil
from git_api_helpers import get_github_token, get_repo_from_remote_url

def delete_git_repo(repo_dir_name):
    """Deletes the GitHub remote and the local repository directory."""
    local_repo_path = os.path.join(os.getcwd(), repo_dir_name)

    if not os.path.isdir(local_repo_path):
        print(f"Error: The directory '{local_repo_path}' does not exist.", file=sys.stderr)
        return

    try:
        remote_url = subprocess.check_output(
            ["git", "config", "--get", "remote.origin.url"],
            cwd=local_repo_path,
            stderr=subprocess.STDOUT
        ).decode().strip()
    except subprocess.CalledProcessError:
        print("Error: Unable to retrieve remote URL. Is this a valid Git repository?", file=sys.stderr)
        return

    owner, repo_name = get_repo_from_remote_url(remote_url)
    if not owner or not repo_name:
        print(f"Error: Unable to parse GitHub info from URL '{remote_url}'.", file=sys.stderr)
        return

    github_token = get_github_token()
    if not github_token:
        return

    try:
        confirm = input(f"Are you sure you want to delete '{owner}/{repo_name}' from GitHub and the local directory '{local_repo_path}'? [y/N]: ")
    except EOFError:  # Handle non-interactive execution
        confirm = 'n'
        
    if confirm.strip().lower() != 'y':
        print("Deletion aborted.")
        return

    print(f"Deleting GitHub repository: {owner}/{repo_name}...")
    api_url = f"https://api.github.com/repos/{owner}/{repo_name}"
    headers = {"Authorization": f"token {github_token}"}
    response = requests.delete(api_url, headers=headers)

    if response.status_code == 204:
        print(f"Successfully deleted GitHub repository: {owner}/{repo_name}")
    else:
        print(f"Error deleting GitHub repository. Status: {response.status_code}", file=sys.stderr)
        print(f"Response: {response.json()}", file=sys.stderr)
        print("Aborting before deleting local directory.", file=sys.stderr)
        return

    try:
        print(f"Deleting local directory: {local_repo_path}...")
        shutil.rmtree(local_repo_path)
        print(f"Successfully deleted local directory: {local_repo_path}")
    except OSError as e:
        print(f"Error deleting local directory: {e}", file=sys.stderr)

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <local_repo_directory_name>")
        sys.exit(1)
    
    repo_name_arg = sys.argv[1]
    delete_git_repo(repo_name_arg)

if __name__ == "__main__":
    main()
