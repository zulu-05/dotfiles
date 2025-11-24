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
from typing import List, Optional, Tuple

from .exceptions import GitRepositoryError
from .models import RepoStatus


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


def is_git_repository(path: Path) -> bool:
    """Checks if the given path is the root of a Git repository."""
    try:
        # This command succeeds only if ran inside a Git repository.
        run_git_command(["rev-parse", "--is-inside-work-tree"], cwd=path)
        return True
    except GitRepositoryError:
        return False


def get_current_branch(path: Path) -> str:
    """Gets the current active branch name."""
    result = run_git_command(["rev-parse", "--abbrev-ref", "HEAD"], cwd=path)
    return result.stdout.strip()


def get_remote_url(path: Path) -> Optional[str]:
    """Gets the URL for the remote named 'origin', if it exists."""
    try:
        result = run_git_command(["config", "--get", "remote.origin.url"], cwd=path)
        return result.stdout.strip()
    except GitRepositoryError:
        # This error occurs if the remote 'origin' does not exist.
        return None


def set_remote_origin(path: Path, username: str, repo_name: str) -> None:
    """
    Sets the 'origin' remote for a local Git repository.

    Args:
        path: The path to the Git repository.
        username: The GitHub username (owner of the repository).
        repo_name: The name of the repository.

    Raises:
        GitRepositoryError: If the Git command fails.
    """
    remote_url = f"git@github.com:{username}/{repo_name}.git"
    run_git_command(["remote", "add", "origin", remote_url], cwd=path)
    print(f"Set remote 'origin' to {remote_url}")


def push_to_origin(path: Path, branch_name: str) -> None:
    """
    Pushes the specified branch to the 'origin' remote.

    Args:
        path: The path to the Git repository.
        branch_name: The name of the branch to push.

    Raises:
        GitRepositoryError: If the Git command fails.
    """
    run_git_command(["push", "-u", "origin", branch_name], cwd=path)
    print(f"Pushed branch '{branch_name}' to origin.")


def _get_ahead_behind(cwd: Path) -> Optional[Tuple[int, int]]:
    """Returns (ahead, behind) counts relative to the upstream branch."""
    try:
        # This command gets the tracking branch name (e.g., 'origin/main')
        upstream = run_git_command(["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
                                   cwd=cwd).stdout.strip()
        if not upstream:
            return None

        # Get the ahead/behind counts
        output = run_git_command(["rev-list", "--left-right", "--count", f"{upstream}...HEAD"],
                                 cwd=cwd).stdout.strip()
        behind, ahead = map(int, output.split())
        return ahead, behind
    except GitRepositoryError as e:
        # This typically happens if the upstream branch is not configured
        if "no upstream configured" in e.args[0] or "unknown revision" in e.args[0]:
            return None
        raise


def _get_messy_status(cwd: Path) -> Tuple[bool, int, int]:
    """Returns (is_messy, modified_count, untracked_count)."""
    output = run_git_command(["status", "--porcelain"], cwd=cwd).stdout
    lines = output.strip().splitlines()

    if not lines:
        return False, 0, 0

    modified_count = 0
    untracked_count = 0
    for line in lines:
        if line.startswith("??"):
            untracked_count += 1
        else:
            modified_count += 1

    return True, modified_count, untracked_count


def get_repo_status(repo_path: Path) -> RepoStatus:
    """
    Fetches the complete status of a Git repository by comparing its local state
    with its remote.

    Args:
        repo_path: The path to the Git repository.

    Returns:
        A RepoStatus object containing the detailed status.
    """
    if not is_git_repository(repo_path):
        return RepoStatus(is_repo=False)

    status = RepoStatus(is_repo=True)

    # Fetch latest changes from the remote without merging
    print("Fetching from remote...")
    run_git_command(["fetch"], cwd=repo_path)

    status.current_branch = get_current_branch(repo_path)
    status.remote_url = get_remote_url(repo_path)

    ahead_behind = _get_ahead_behind(repo_path)
    if ahead_behind:
        status.ahead_count, status.behind_count = ahead_behind
        status.upstream_branch = run_git_command(
            ["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
            cwd=repo_path
        ).stdout.strip()

    status.is_messy, status.modified_files, status.untracked_files = _get_messy_status(repo_path)

    return status
