#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unit tests for the github_api module using mocks."""

import pytest
import requests
from unittest.mock import MagicMock

from git_tools import github_api
from git_tools.exceptions import GitHubAPIError

@pytest.fixture
def mock_requests(mocker):
    """Fixture to mock requests.request."""
    return mocker.patch("requests.request")

def test_create_github_repo_success(mock_requests):
    """Tests successful repository creation."""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_requests.return_value = mock_response

    github_api.create_github_repo("new-repo")
    
    # Check that 'post' was called on the correct URL
    mock_requests.assert_called_once()
    assert mock_requests.call_args[0][0] == "post"
    assert "user/repos" in mock_requests.call_args[0][1]

def test_create_github_repo_already_exists(mock_requests):
    """Tests repository creation when it already exists (status 422)."""
    mock_response = MagicMock()
    mock_response.status_code = 422
    mock_response.json.return_value = {
        "message": "Validation Failed",
        "errors": [{"resource": "Repository", "code": "custom", "field": "name", "message": "name already exists on this account"}]
    }
    # Configure raise_for_status to raise the appropriate error
    mock_response.raise_for_status.side_effect = requests.HTTPError(response=mock_response)
    mock_requests.return_value = mock_response

    # This should not raise an exception, just log a message
    github_api.create_github_repo("existing-repo")

def test_create_github_repo_api_failure(mock_requests):
    """Tests failure during repository creation."""
    mock_response = MagicMock()
    mock_response.status_code = 401  # Unauthorized
    mock_response.raise_for_status.side_effect = requests.HTTPError(response=mock_response)
    mock_requests.return_value = mock_response

    with pytest.raises(GitHubAPIError):
        github_api.create_github_repo("fail-repo")
