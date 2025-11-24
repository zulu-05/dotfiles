#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# Checks the synchronisation status of a local Git repo against its remote.
# -----------------------------------------------------------------------------
import argparse
import sys
from pathlib import Path

try:
    from git_tools import git_operations
    from git_tools.exceptions import GitToolsError
    ffrom git_tools.models import RepoStatus
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from git_tools import git_operations
    from git_tools.exceptions import GitToolsError
    from git_tools.models import RepoStatus

# --- ANSI Colour Codes ---
class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    GRAY = "\033[90m"
    ENDC = "\033[0m"

def _print_status(status: RepoStatus):
    """Formats and prints the repository status to the console."""
    if not status.is_repo:
        print(f"{Colors.RED}Error: Not a Git repository.{Colors.ENDC}")
        return

    # --- 1. The High-Level Summary Line ---
    summary = ""
    if status.is_messy:
        summary = f"{Colors.YELLOW}* Messy{Colors.ENDC}"
    elif status.ahead_count > 0 and status.behind_count > 0:
        summary = f"{Colors.RED}↔Diverged{Colors.ENDC}"
    elif status.ahead_count > 0:
        summary = f"{Colors.YELLOW}↑Ahead{Colors.ENDC}"
    elif status.behind_count > 0:
        summary = f"{Colors.YELLOW}↓Behind{Colors.ENDC}"
    elif not status.remote_url:
        summary = f"{Colors.GRAY}- No Remote{Colors.ENDC}"
    else:
        summary = f"{Colors.GREEN}●Synced{Colors.ENDC}"

    print(f"\nStatus: {summary}")
    print("-" * 40)

    # --- 2. Detailed Information ---
    print(f" {Colors.BLUE}Local Branch:{Colors.ENDC} {status.current_branch}")
    if status.upstream_branch:
        print(f" {Colors.BLUE}Upstream:{Colors.ENDC} {status.upstream_branch}")

    if status.ahead_count or status.behind_count:
        print(f" {Colors.BLUE}Commits:{Colors.ENDC} {status.ahead_count} ahead, {status.behind_count} behind")

    if status.is_messy:
        messy_details = []
        if status.modified_files > 0:
            messy_details.append(f"{status.modified_files} modified")
        if status.untracked_files > 0:
            messy_details.append(f"{status.untracked_files} untracked")
        print(f" {Colors.BLUE}Working Dir:{Colors.ENDC} {', '.join(messy_details)}")

    if status.remote_url:
        print(f" {Colors.BLUE}Remote URL:{Colors.ENDC} {status.remote_url}")

    print("-" * 40)


def main() -> None:
    """Parses arguments and orchestrates the status check."""
    parser = argparse.ArgumentParser(
        description="Check the status of a Git repository against its remote."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Optional path to the Git repository. Defaults to the current directory."
    )
    args = parser.parse_args()

    repo_path = Path(args.path).resolve()

    try:
        status = git_operations.get_repo_status(repo_path)
        _print_status(status)
    except GitToolsError as e:
        print(f"\n{Colors.RED}Error: An operation failed:\n{e}{Colors.ENDC}" file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
