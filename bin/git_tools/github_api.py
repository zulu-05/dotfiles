#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Handles interactions with the GitHub REST API.
"""

import requests
from requests.exceptions import RequestException

from .config import GITHUB_TOKEN
from .exceptions import GitHubAPIError


def _make_api_request(method: str, url: str, **kwargs) -> requests.Response:
    """
    A private helper to make authenticated requests to the GitHub API.

    Args:
        method: The HTTP method ('get', 'post', 'patch', 'delete').
        url: The API endpoint URL.
        **kwargs: Additional arguments to pass to requests (e.g., json, timeout).

    Returns:
        The requests.Response object.

    Raises:
        GitHubAPIError: For connection errors or non-2xx status codes.
    """
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    try:
        response = requests.request(
            method, url, headers=headers, timeout=15, **kwargs
        )
        response.raise_for_status()
        return response
    except RequestException as e:
        raise GitHubAPIError(f"Failed to connect to GitHub API: {e}") from e


def create_github_repo(repo_name: str) -> None:
    """Creates a new public repository on GitHub."""
    api_url = "https://api.github.com/user/repos"
    data = {"name": repo_name, "private": False}
    try:
        _make_api_request("post", api_url, json=data)
        print(f"Successfully created GitHub repository '{repo_name}'")
    except GitHubAPIError as e:
        if e.__cause__ and isinstance(e.__cause__, requests.HTTPError):
            if e.__cause__.response.status_code == 422:
                print(f"GitHub repository '{repo_name}' already exists. Proceeding...")
                return
        raise  # Re-raise if it's not the "already exists" error


def delete_github_repo(owner: str, repo_name: str) -> None:
    """
    Deletes a repository from GitHub.

    Args:
        owner: The owner of the repository (e.g., your username).
        repo_name: The name of the repository to delete.

    Raises:
        GitHubAPIError: If the API call fails.
    """
    api_url = f"https://api.github.com/repos/{owner}/{repo_name}"
    _make_api_request("delete", api_url)
    print(f"Successfully deleted GitHub repository: {owner}/{repo_name}")


def rename_github_repo(owner: str, old_name: str, new_name: str) -> None:
    """
    Renames a repository on GitHub.

    Args:
        owner: The owner of the repository.
        old_name: The current name of the repository.
        new_name: The new name for the repository.

    Raises:
        GitHubAPIError: If the API call fails.
    """
    api_url = f"https://api.github.com/repos/{owner}/{old_name}"
    data = {"name": new_name}
    _make_api_request("patch", api_url, json=data)
    print(f"Successfully renamed GitHub repo from '{old_name}' to '{new_name}'")
