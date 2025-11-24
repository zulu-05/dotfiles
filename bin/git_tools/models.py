#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
Defines data structures and models for the git_tools library.
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class RepoStatus:
    """A structured representation of a Git repository's status."""
    is_repo: bool
    current_branch: Optional[str] = None
    remote_url: Optional[str] = None
    upstream_branch: Optional[str] = None
    ahead_count: int = 0
    behind_count: int = 0
    is_messy: bool = False
    untracked_files: int = 0
    modified_files: int = 0
