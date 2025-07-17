#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# Shared helper functions and configuration for GitHub API scripts.
# -----------------------------------------------------------------------------
import sys
import subprocess
import re

# --- Centralized Configuration ---
# Your GitHub username. All scripts will import it from here.
GITHUB_USERNAME = "zulu-05"

def get_github_token():
    """Retrieves the GitHub token from the 'pass' secret manager."""
    try:
        token = subprocess.check_output(['pass', 'show', 'github_token']).decode().strip()
        if not token:
            print("Error: 'pass' returned an empty token for 'github_token'.", file=sys.stderr)
            return None
        return token
    except FileNotFoundError:
        print("Error: The 'pass' command was not found. Is it installed and in your PATH?", file=sys.stderr)
        return None
    except subprocess.CalledProcessError:
        print("Error: Failed to retrieve 'github_token' from 'pass'. Does the secret exist?", file=sys.stderr)
        return None

def get_repo_from_remote_url(remote_url):
    """
    Parses a GitHub repository owner and name from an SSH or HTTPS URL.
    Returns a tuple (owner, repo_name) or (None, None) on failure.
    """
    # Regex for SSH: git@github.com:owner/repo.git
    ssh_match = re.search(r'git@github\.com:([^/]+)/(.+?)(?:\.git)?$', remote_url)
    if ssh_match:
        return ssh_match.group(1), ssh_match.group(2)

    # Regex for HTTPS: https://github.com/owner/repo.git
    https_match = re.search(r'https://github\.com/([^/]+)/(.+?)(?:\.git)?$', remote_url)
    if https_match:
        return https_match.group(1), https_match.group(2)

    return None, None
