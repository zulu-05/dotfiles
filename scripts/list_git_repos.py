#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# A script to list and inspect your GitHub repositories.
# -----------------------------------------------------------------------------
import sys
import requests
from datetime import datetime
from git_api_helpers import GITHUB_USERNAME, get_github_token

# --- Helper Functions ---

def make_api_request(url, access_token):
    """Makes an authenticated request to the GitHub API and handles errors."""
    headers = {"Authorization": f"token {access_token}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making API request to {url}: {e}", file=sys.stderr)
        return None

def get_all_repos(access_token):
    """Fetches all repositories for the configured user, handling pagination."""
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos?per_page=100&page={page}"
        data = make_api_request(url, access_token)
        if not data:
            break
        repos.extend(data)
        if len(data) < 100:
            break
        page += 1
    # Sort repositories by the last push date, most recent first.
    repos.sort(key=lambda r: r.get("pushed_at", ""), reverse=True)
    return repos

def parse_date(date_string):
    """Converts GitHub's ISO 8601 date string to a readable format."""
    if not date_string:
        return "N/A"
    dt_object = datetime.fromisoformat(date_string.replace("Z", "+00:00"))
    return dt_object.strftime("%Y-%m-%d %H:%M:%S %Z")

def display_repo_list(repos):
    """Prints a numbered list of repositories."""
    print("\nYour GitHub Repositories:")
    for i, repo in enumerate(repos):
        print(f"  {i + 1:2d}) {repo['name']}")

# --- Detail Display Functions ---

def show_description(repo):
    print("\n--- Description ---")
    print(repo.get("description") or "No description provided.")

def show_dates(repo):
    print("\n--- Dates ---")
    print(f"  Created:       {parse_date(repo.get('created_at'))}")
    print(f"  Last Push:     {parse_date(repo.get('pushed_at'))}")

def show_languages(repo, access_token):
    print("\n--- Top 3 Languages ---")
    lang_url = repo.get("languages_url")
    if not lang_url:
        print("Language data not available.")
        return

    lang_data = make_api_request(lang_url, access_token)
    if not lang_data:
        print("Could not fetch language data.")
        return

    total_bytes = sum(lang_data.values())
    if total_bytes == 0:
        print("No languages detected.")
        return

    top_langs = sorted(lang_data.items(), key=lambda item: item[1], reverse=True)[:3]
    for lang, bytes_count in top_langs:
        percentage = (bytes_count / total_bytes) * 100
        print(f"  - {lang:<15} {percentage:.2f}%")

def show_tree(repo, access_token):
    print("\n--- Directory Tree ---")
    branch = repo.get("default_branch", "main")
    tree_url = f"https://api.github.com/repos/{repo['full_name']}/git/trees/{branch}?recursive=1"
    
    tree_data = make_api_request(tree_url, access_token)
    if not tree_data or "tree" not in tree_data:
        print("Could not fetch directory tree.")
        return
    
    paths = sorted([item['path'] for item in tree_data['tree'] if 'path' in item])
    
    structure = {}
    for path in paths:
        parts = path.split('/')
        current_level = structure
        for part in parts:
            current_level = current_level.setdefault(part, {})

    def print_tree(d, indent=''):
        for i, (key, value) in enumerate(d.items()):
            is_last = i == len(d) - 1
            connector = "└── " if is_last else "├── "
            print(f"{indent}{connector}{key}")
            new_indent = indent + ("    " if is_last else "│   ")
            if value:
                print_tree(value, new_indent)

    print_tree(structure)

def repo_detail_menu(repo, access_token):
    """Displays a menu of options for a selected repository."""
    while True:
        print(f"\n--- Details for: {repo['name']} ---")
        print("1) Description")
        print("2) Dates (Created/Last Push)")
        print("3) Top Languages")
        print("4) Directory Tree")
        print("5) All Details")
        print("q) Back to list")

        try:
            choice = input("Choose an option: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            choice = 'q'
            print()

        if choice == '1': show_description(repo)
        elif choice == '2': show_dates(repo)
        elif choice == '3': show_languages(repo, access_token)
        elif choice == '4': show_tree(repo, access_token)
        elif choice == '5':
            show_description(repo)
            show_dates(repo)
            show_languages(repo, access_token)
            show_tree(repo, access_token)
        elif choice == 'q': break
        else: print("Invalid option. Please try again.")

def main():
    """Main function to run the repository inspector."""
    access_token = get_github_token()
    if not access_token:
        sys.exit(1)

    print("Fetching repository data from GitHub...")
    repos = get_all_repos(access_token)
    if repos is None:
        sys.exit(1)

    while True:
        display_repo_list(repos)
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
                repo_detail_menu(repos[repo_index], access_token)
            else:
                print("Invalid number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number or 'q'.")

if __name__ == "__main__":
    main()

