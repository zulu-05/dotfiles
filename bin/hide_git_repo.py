#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# Sets a GitHub repository's visibility to PRIVATE.
# -----------------------------------------------------------------------------
import sys
from pathlib import Path

try:
    from git_tools import github_api, config
    from git_tools.exceptions import GitToolsError, ConfigurationError

except ImportError:
    # This allows the script to be run directly for development/testing
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from git_tools import github_api, config
    from git_tools.exceptions import GitToolsError, ConfigurationError


def main() -> None:
    """Parses arguments and orchestrates making a repository private."""
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <repo-name>", file=sys.stderr)
        sys.exit(1)

    repo_name = sys.argv[1]

    try:
        # Lazily get the username from the config module
        owner = config.get_github_username()

        print(f"Setting visibility of '{owner}/{repo_name}' to PRIVATE...")

        # Call the centralised library function
        github_api.update_repo_visibility(owner=owner, repo_name=repo_name, private=True)

    except (GitToolsError, ConfigurationError) as e:
        # Centralised error handling, as per the architecture
        print(f"\nError: An operation failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
