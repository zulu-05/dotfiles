#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Handles all local Git repository operations.

This module provides a secure wrapper for running Git commands and encapsulates
high-level operations like initializing a repository, creating commits, and
managing remotes.
"""

import logging
import subprocess
from pathlib import Path
from typing import List, Optional

from .exceptions import GitRepositoryError


def run_git_command(
    args: List[str], cwd: Optional[Path] = None
) -> subprocess.CompletedProcess[str]:
    """Runs a git command securely and captures its output.

    This function is a wrapper around subprocess.run that provides standardized
    error handling, converting subprocess errors into a custom GitRepositoryError.
    It ensures that commands are run without a shell and that errors are
    descriptive.

    Args:
        args (List[str]): A list of strings representing the git command and
            its arguments (e.g., ['clone', 'some_url']).
        cwd (Optional[Path]): The working directory from which to run the
            command. Defaults to the current working directory.

    Returns:
        subprocess.CompletedProcess[str]: A CompletedProcess instance on success.

    Raises:
        GitRepositoryError: If the 'git' command is not found or if the command
                            returns a non-zero exit code.
    """
    command = ['git'] + args
    logging.debug(f"Running command: {' '.join(command)}")
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )
        return result
    except FileNotFoundError as e:
        raise GitRepositoryError(
            "The 'git' command was not found. Is Git installed and in your PATH?"
        ) from e
    except subprocess.CalledProcessError as e:
        # Provide rich context upon command failure.
        error_message = (
            f"Git command failed: {' '.join(command)}\n"
            f"Return code: {e.returncode}\n"
            f"Stderr: {e.stderr.strip()}\n"
            f"Stdout: {e.stdout.strip()}"
        )
        raise GitRepositoryError(error_message) from e

# ... other documented functions would follow ...
