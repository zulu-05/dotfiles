#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Handles the user interface and console output for the list_git_repos tool.
"""

from typing import Any, Dict, List
from datetime import datetime

def _parse_date(date_string: str) -> str:
    """Converts GitHub's ISO 8601 date string to a readable format."""
    if not date_string:
        return "N/A"
    dt_object = datetime.fromisoformat(date_string.replace("Z", "+00:00"))
    return dt_object.strftime("%Y-%m-%d %H:%M:%S")

def _display_repo_list(repos: List[Dict[str, Any]]) -> None:
    """Prints a numbered list of repositories."""
    print("\nYour GitHub Repositories (most recent first):")
    for i, repo in enumerate(repos):
        print(f"  {i + 1:2d}) {repo['name']}")

def _display_repo_details(repo: Dict[str, Any]) -> None:
    """Prints a detailed summary of a single repository."""
    print("\n--- Details ---")
    print(f"Name:        {repo.get('full_name')}")
    print(f"Description: {repo.get('description') or 'No description provided.'}")
    print(f"Language:    {repo.get('language') or 'N/A'}")
    print(f"Created:     {_parse_date(repo.get('created_at'))}")
    print(f"Last Push:   {_parse_date(repo.get('pushed_at'))}")
    print(f"URL:         {repo.get('html_url')}")

def run_repo_inspector_menu(repos: List[Dict[str, Any]]) -> None:
    """
    Runs the main interactive loop for inspecting repositories.
    """
    while True:
        _display_repo_list(repos)
        try:
            user_input = input("\nEnter a repo number to inspect, or 'q' to quit: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            user_input = 'q'
            print("\nExiting.")

        if user_input == 'q':
            break
        
        try:
            repo_index = int(user_input) - 1
            if 0 <= repo_index < len(repos):
                _display_repo_details(repos[repo_index])
            else:
                print("Invalid number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number or 'q'.")
