#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Custom exception hierarchy for the Git Tools project.
"""

class GitToolsError(Exception):
    """Base exception for all git tools errors."""
    pass

class GitRepositoryError(GitToolsError):
    """Errors related to local Git repository operations."""
    pass

class GitHubAPIError(GitToolsError):
    """Errors related to GitHub API operations."""
    pass

class ConfigurationError(GitToolsError):
    """Errors related to configuration or secret retrieval."""
    pass

class ValidationError(GitToolsError):
    """Errors related to input validation."""
    pass
