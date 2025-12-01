#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# Safely finds and removes a standard Python virtual environment.
# Intended to be called by the 'rmvenv' shell function.
# -----------------------------------------------------------------------------
import shutil
import sys
from pathlib import Path

# --- Configuration ---
VENV_DIR = Path(".venv")

# --- ANSI Colour Codes ---
class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    ENDC = "\033[0m"

def main() -> None:
    """Main script logic."""
    print(f"Searching for virtual environment at './{VENV_DIR}'...")

    if not VENV_DIR.exists() or not VENV_DIR.is_dir():
        print(f"{Colors.YELLOW}No virtual environment found. Nothing to do.{Colors.ENDC}")
        sys.exit(0)

    # Safety check: Confirm this looks like a venv by checking for the Python executable
    python_executable = VENV_DIR / "bin" / "python"
    if not python_executable.exists():
        print(f"{Colors.RED}Error: Directory './{VENV_DIR}' exists but does not appear to be a valid virtual environment.{Colors.ENDC}", file=sys.stderr)
        sys.exit(1)

    # Confirmation prompt
    try:
        confirm = input(f"{Colors.YELLOW}Are you sure want to permanently delete the virtual environment './{VENV_DIR}'? [y/N]: {Colors.ENDC}")
        if confirm.lower() != 'y':
            print("Operation cancelled.")
            sys.exit(0)
    except (KeyboardInterrupt, EOFError):
        print("\nOperation cancelled.")
        sys.exit(1)

    # Delete the repository
    print(f"Deleting './{VENV_DIR}'...", end="", flush=True)
    try:
        shutil.rmtree(VENV_DIR)
        print(f"{Colors.GREEN}done{Colors.ENDC}")
    except OSError as e:
        print(f"{Colors.RED}failed{Colors.ENDC}")
        print(f"\n{Colors.RED}Error: Could not remove directory.\n{e}{Colors.ENDC}", file=sys.stderr)
        sys.exit(1)

    print(f"\n{Colors.GREEN}✅ Virtual environment removed successfully!{Colors.ENDC}")

if __name__ == "__main__":
    main()
