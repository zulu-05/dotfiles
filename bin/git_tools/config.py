#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Handles configuration and secret management for the Git Tools project.

This module is responsible for retrieving secrets like the GitHub username
and personal access token from the 'pass' password manager.
It is designed with a lazy-loading pattern. Secrets are only retrieved from the
'pass' password manager when they are first requested. Subsequent requests
during the same script execution will use a cached value.
"""

import functools
import subprocess
import sys
from typing import Final

from .exceptions import ConfigurationError


def _get_secret_from_pass(pass_path: str) -> str:
    """
    Retrieves a secret from the 'pass' password manager.

    This function provides a robust wrapper around the 'pass' command-line tool,
    with standardized error handling.

    Args:
        pass_path (str): The path to the secret within the password store
            (e.g., 'git/github_username').

    Returns:
        str: The retrieved secret as a string.

    Raises:
        ConfigurationError: If the 'pass' command is not found, fails to
            execute, or returns an empty value.
    """
    try:
        result = subprocess.run(
            ['pass', 'show', pass_path],
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )
        secret = result.stdout.strip()
        if not secret:
            raise ConfigurationError(f"Secret at '{pass_path}' is empty.")
        return secret

    except FileNotFoundError as e:
        # This error occurs if the 'pass' command itself is not installed or in the PATH.
        raise ConfigurationError(
            "The 'pass' command was not found. Is it installed and in your PATH?"
        ) from e

    except subprocess.CalledProcessError as e:
        # This error occurs if 'pass' returns a non-zero exit code, for example
        # if the secret does not exist.
        error_message = (
            f"Failed to retrieve secret from pass for '{pass_path}'.\n"
            f"Does the secret exist? Stderr: {e.stderr.strip()}"
        )
        raise ConfigurationError(error_message) from e


@functools.lru_cache(maxsize=None)
def get_github_username() -> str:
    """
    Lazily retrieves and caches the GitHub username from the pass store.

    Raises:
        ConfigurationError: If the secret cannot be loaded at runtime.
    """
    return _get_secret_from_pass("git/github_username")


@functools.lru_cache(maxsize=None)
def get_github_token() -> str:
    """
    Lazily retrieves and caches the GitHub token from the pass store.

    Raises:
        ConfigurationError: If the secret cannot be loaded at runtime.
    """
    return _get_secret_from_pass("git/personal_access_token")
