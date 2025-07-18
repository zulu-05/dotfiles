#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unit tests for the validation module."""

import pytest
from git_tools import validation

# --- Tests for get_repo_from_remote_url ---

@pytest.mark.parametrize("url, expected", [
    ("git@github.com:user/repo.git", ("user", "repo")),
    ("git@github.com:user-name/repo-name.git", ("user-name", "repo-name")),
    ("https://github.com/user/repo.git", ("user", "repo")),
    ("https://github.com/user/repo", ("user", "repo")),
    ("https://github.com/user.name/repo.name.git", ("user.name", "repo.name")),
])
def test_get_repo_from_remote_url_valid(url, expected):
    """Tests that valid GitHub URLs are parsed correctly."""
    assert validation.get_repo_from_remote_url(url) == expected

@pytest.mark.parametrize("url", [
    "git@gitlab.com:user/repo.git",
    "https://example.com/user/repo.git",
    "not a url",
    "",
])
def test_get_repo_from_remote_url_invalid(url):
    """Tests that invalid URLs return None."""
    assert validation.get_repo_from_remote_url(url) is None

# --- Tests for validate_repo_name ---

@pytest.mark.parametrize("name", ["repo", "repo-name", "repo.name", "repo_name"])
def test_validate_repo_name_valid(name):
    """Tests valid repository names."""
    assert validation.validate_repo_name(name) is True

@pytest.mark.parametrize("name", [
    "",
    "a" * 101,  # Too long
    "repo/name",  # Invalid character
    ".",
    "..",
    "repo name", # space
])
def test_validate_repo_name_invalid(name, capsys):
    """Tests invalid repository names and checks for error output."""
    assert validation.validate_repo_name(name) is False
    # Check that an error message was printed to stderr
    captured = capsys.readouterr()
    assert "Error:" in captured.err
