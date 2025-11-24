#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# Shared helper functions for Git and GitHub URL parsing.
#
# NOTE: Secret management has been moved to the `git_tools.config` module
# to centralise logic and enable lazy loading.
# -----------------------------------------------------------------------------
import re


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
