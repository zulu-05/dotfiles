#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Handles configuration and secret management for the Git Tools project.

This module is responsible for retrieving secrets like the GitHub username
and personal access token from the 'pass' password manager. It is designed
to fail early if secrets cannot be loaded.
"""

import subprocess
import sys
from typing import Final

from .exceptions import ConfigurationError


def _get_secret_from_pass(pass_path: str) -> str:
    """Retrieves a secret from the 'pass' password manager.

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
            f"Stderr: {e.stderr.strip()}"
        )
        raise ConfigurationError(error_message) from e


# --- Module-level constants loaded on import ---
# These will raise a ConfigurationError if the secrets cannot be loaded,
# causing any script that imports them to halt early with a clear error message.
try:
    GITHUB_USERNAME: Final[str] = _get_secret_from_pass("git/github_username")
    GITHUB_TOKEN: Final[str] = _get_secret_from_pass("git/personal_access_token")
except ConfigurationError as e:
    # We catch the exception to print a user-friendly message and exit,
    # preventing a raw traceback for configuration issues.
    print(f"CRITICAL: A configuration error occurred:\n{e}", file=sys.stderr)
    sys.exit(1)
