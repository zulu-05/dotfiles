#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Provides input validation and parsing functions.
"""

import re
from typing import Optional, Tuple


def get_repo_from_remote_url(remote_url: str) -> Optional[Tuple[str, str]]:
    """
    Parses a GitHub repository owner and name from an SSH or HTTPS URL.

    Args:
        remote_url: The full git remote URL.

    Returns:
        A tuple containing (owner, repo_name) if parsing is successful,
        otherwise None.
    """
    # Regex for SSH: git@github.com:owner/repo.git
    ssh_match = re.search(r'git@github\.com:([^/]+)/(.+?)(?:\.git)?$', remote_url)
    if ssh_match:
        return ssh_match.group(1).strip(), ssh_match.group(2).strip()

    # Regex for HTTPS: https://github.com/owner/repo.git
    https_match = re.search(r'https://github\.com/([^/]+)/(.+?)(?:\.git)?$', remote_url)
    if https_match:
        return https_match.group(1).strip(), https_match.group(2).strip()

    return None


def validate_repo_name(repo_name: str) -> bool:
    """
    Validates a repository name against common GitHub naming rules.

    Args:
        repo_name: The repository name to validate.

    Returns:
        True if the name is valid, False otherwise.
    """
    if not repo_name or len(repo_name) > 100:
        print("Error: Repo name must be between 1 and 100 characters.", file=sys.stderr)
        return False
    # Allowed characters: letters, digits, hyphen, underscore, period.
    if not re.match(r'^[a-zA-Z0-9_.-]+$', repo_name):
        print("Error: Repo name contains invalid characters.", file=sys.stderr)
        return False
    if repo_name in {".", ".."}:
        return False
    return True
