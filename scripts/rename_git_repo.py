#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# Renames a Git repository on both the local system and GitHub.
# -----------------------------------------------------------------------------
import os
import sys
import subprocess
import requests
from git_api_helpers import GITHUB_USERNAME, get_github_token

def rename_git_repo(old_name, new_name):
    """Renames the local directory, updates the remote URL, and renames on GitHub."""
    access_token = get_github_token()
    if not access_token:
        sys.exit(1)

    # Define paths
    parent_dir = os.getcwd()
    old_path = os.path.join(parent_dir, old_name)
    new_path = os.path.join(parent_dir, new_name)
    
    if not os.path.isdir(old_path):
        print(f"Error: Directory '{old_name}' not found in {parent_dir}.", file=sys.stderr)
        sys.exit(1)
        
    # --- Step 1: Rename repository on GitHub via API ---
    print(f"Renaming GitHub repository from '{old_name}' to '{new_name}'...")
    api_url = f'https://api.github.com/repos/{GITHUB_USERNAME}/{old_name}'
    headers = {
        'Authorization': f'token {access_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    data = {'name': new_name}
    response = requests.patch(api_url, headers=headers, json=data)

    if response.status_code != 200:
        print(f"Failed to rename GitHub repository. Status: {response.status_code}", file=sys.stderr)
        print(f"Response: {response.json()}", file=sys.stderr)
        sys.exit(1)
    
    print(f"Successfully renamed GitHub repository.")

    # --- Step 2: Rename local directory ---
    try:
        os.rename(old_path, new_path)
        print(f"Renamed local directory to '{new_name}'")
    except OSError as e:
        print(f"Error: Failed to rename local directory: {e}", file=sys.stderr)
        print("Please manually rename the local directory and update the remote URL.", file=sys.stderr)
        sys.exit(1)

    # --- Step 3: Update remote URL in local git config ---
    try:
        os.chdir(new_path)
        new_remote_url = f'git@github.com:{GITHUB_USERNAME}/{new_name}.git'
        subprocess.run(['git', 'remote', 'set-url', 'origin', new_remote_url], check=True)
        print(f"Updated remote URL to '{new_remote_url}'")
    except (OSError, subprocess.CalledProcessError) as e:
        print(f"Error: Failed to update git remote URL: {e}", file=sys.stderr)
        print("The GitHub repo was renamed, but the local repo needs manual correction.", file=sys.stderr)
        sys.exit(1)

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <old_name> <new_name>")
        sys.exit(1)
    
    old_name_arg = sys.argv[1]
    new_name_arg = sys.argv[2]
    rename_git_repo(old_name_arg, new_name_arg)

if __name__ == "__main__":
    main()
