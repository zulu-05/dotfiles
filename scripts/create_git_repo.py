#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# Creates a local Git repository, a corresponding remote on GitHub,
# and pushes the initial commit.
# -----------------------------------------------------------------------------
import os
import sys
import subprocess
import requests
from git_api_helpers import GITHUB_USERNAME, get_github_token

def create_local_repo(repo_name, directory_path):
    """
    Creates a local Git repository and makes an initial commit.
    Returns True on success, False on failure.
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path, exist_ok=True)
        print(f"Created directory: {directory_path}")
    else:
        print(f"Using existing directory: {directory_path}")

    if not os.path.exists(os.path.join(directory_path, ".git")):
        subprocess.run(["git", "init", "-b", "main"], cwd=directory_path, check=True)
        print(f"Initialized a new Git repository in {directory_path}")
    else:
        print(f"Git repository already exists in {directory_path}")

    readme_path = os.path.join(directory_path, "README.md")
    if not os.path.exists(readme_path):
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(f"# {repo_name}\n")
        print("Created README.md")

    subprocess.run(["git", "add", "."], cwd=directory_path, check=True)
    status = subprocess.run(["git", "status", "--porcelain"], cwd=directory_path, capture_output=True, text=True)
    
    if status.stdout.strip():
        subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=directory_path, check=True)
        print("Created initial commit")
        return True  # A commit was made
    else:
        print("No changes to commit, checking for existing commits...")
        # Check if there's already a commit in the repo
        try:
            subprocess.run(["git", "rev-parse", "--verify", "HEAD"], cwd=directory_path, check=True, capture_output=True)
            print("Repository already has commits.")
            return True # Commits exist, so we can proceed
        except subprocess.CalledProcessError:
            print("Error: No changes to commit and no existing commits. Cannot push.", file=sys.stderr)
            return False # No commits exist, cannot proceed

def create_github_repo(repo_name, access_token):
    """Creates a new GitHub repository using the GitHub API."""
    api_url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    data = {"name": repo_name, "private": False}
    response = requests.post(api_url, headers=headers, json=data)

    if response.status_code == 201:
        print(f"Successfully created GitHub repository '{repo_name}'")
        return True
    elif response.status_code == 422 and "already exists" in response.text:
        print(f"GitHub repository '{repo_name}' already exists.")
        return True
    else:
        print(f"Failed to create GitHub repository. Status: {response.status_code}", file=sys.stderr)
        print("Response:", response.json(), file=sys.stderr)
        return False

def set_remote_and_push(directory_path, repo_name):
    """Sets the remote to GitHub and pushes the main branch."""
    remote_url = f"git@github.com:{GITHUB_USERNAME}/{repo_name}.git"
    try:
        remotes = subprocess.run(["git", "remote"], cwd=directory_path, capture_output=True, text=True, check=True).stdout.strip().split('\n')
        if "origin" in remotes:
            subprocess.run(["git", "remote", "set-url", "origin", remote_url], cwd=directory_path, check=True)
            print("Updated existing remote 'origin'.")
        else:
            subprocess.run(["git", "remote", "add", "origin", remote_url], cwd=directory_path, check=True)
            print(f"Added remote 'origin': {remote_url}")
        
        subprocess.run(["git", "push", "-u", "origin", "main"], cwd=directory_path, check=True)
        print("Pushed local 'main' branch to remote repository.")
    except subprocess.CalledProcessError as e:
        print(f"Error during remote setup or push: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <repo_name>")
        sys.exit(1)

    repo_name = sys.argv[1]
    directory_path = os.path.join(os.getcwd(), repo_name)
    
    access_token = get_github_token()
    if not access_token:
        sys.exit(1)

    if not create_local_repo(repo_name, directory_path):
        sys.exit(1)
        
    if not create_github_repo(repo_name, access_token):
        sys.exit(1)
        
    set_remote_and_push(directory_path, repo_name)

if __name__ == "__main__":
    main()
