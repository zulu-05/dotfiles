#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unit tests for the git_operations module using mocks."""

import subprocess
from pathlib import Path
import pytest

from git_tools import git_operations
from git_tools.exceptions import GitRepositoryError

@pytest.fixture
def mock_subprocess(mocker):
    """Fixture to mock subprocess.run."""
    return mocker.patch("subprocess.run")

def test_run_git_command_success(mock_subprocess):
    """Tests a successful git command execution."""
    mock_subprocess.return_value = subprocess.CompletedProcess(
        args=["git", "status"], returncode=0, stdout="clean", stderr=""
    )
    result = git_operations.run_git_command(["status"])
    mock_subprocess.assert_called_with(
        ["git", "status"], cwd=None, capture_output=True, text=True, check=True, encoding='utf-8'
    )
    assert result.stdout == "clean"

def test_run_git_command_failure(mock_subprocess):
    """Tests a failed git command execution."""
    mock_subprocess.side_effect = subprocess.CalledProcessError(
        returncode=128, cmd=["git", "clone", "bad-url"], stderr="Repo not found"
    )
    with pytest.raises(GitRepositoryError) as excinfo:
        git_operations.run_git_command(["clone", "bad-url"])
    
    # Check that our custom error contains the context from the original error
    assert "Repo not found" in str(excinfo.value)
    assert "Return code: 128" in str(excinfo.value)

def test_run_git_command_not_found(mock_subprocess):
    """Tests when the git command itself is not found."""
    mock_subprocess.side_effect = FileNotFoundError
    with pytest.raises(GitRepositoryError, match="command was not found"):
        git_operations.run_git_command(["status"])
