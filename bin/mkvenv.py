#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# Creates and bootstraps a standard Python virtual environment.
# Intended to be called by the 'mkvenv' shell function.
# -----------------------------------------------------------------------------
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

# --- Configuration ---
VENV_DIR = Path(".venv")

# --- ANSI Colour Codes ---
class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    ENDC = "\033[0m"


def run_command(command: list[str], message: str):
    """Runs a command and prints a status message."""
    print(f"{Colors.BLUE} -> {message}...{Colors.ENDC}", end="", flush=True)
    try:
        subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        print(f"{Colors.GREEN}done{Colors.ENDC}")
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}failed{Colors.ENDC}")
        print(f"\n{Colors.RED}Error output:\n{e.stderr}{Colors.ENDC}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    """Main script logic."""
    parser = argparse.ArgumentParser(description="Create a Python virtual environment.")
    parser.add_argument(
        "prompt",
        nargs="?",
        default=".venv",
        help="The prompt name to use for the virtual environment. Defaults to '.venv'."
    )
    args = parser.parse_args()

    print(f"{Colors.BLUE}Setting up Python virtual environment at './{VENV_DIR}'...{Colors.ENDC}")

    # Handle existing venv
    if VENV_DIR.exists():
        try:
            confirm = input(f"{Colors.YELLOW}Virtual environment './{VENV_DIR}' already exists. Overwrite? [y/N]: {Colors.ENDC}")
            if confirm.lower() != 'y':
                print("Operation cancelled.")
                sys.exit(0)
            print(f"Removing existing '{VENV_DIR}' directory...")
            shutil.rmtree(VENV_DIR)
        except (KeyboardInterrupt, EOFError):
            print("\nOperation cancelled.")
            sys.exit(1)

    # Step 1: Create the virtual environment
    run_command(
        [sys.executable, "-m", "venv", "--prompt", args.prompt, str(VENV_DIR)],
        f"Creating base environment with prompt '{args.prompt}'"
    )

    # Determine the path to the Python executable inside the new venv
    python_executable = VENV_DIR / "bin" / "python"

    # Step 2: Upgrade pip
    run_command(
        [str(python_executable), "-m", "pip", "install", "--upgrade", "pip"],
        "Upgrading pip"
    )

    # Step 3: Install common utility packages
    run_command(
        [str(python_executable), "-m", "pip", "install", "wheel", "setuptools"],
        "Installing wheel and setuptools"
    )

    print(f"\n{Colors.GREEN}✅ Virtual environment created successfully!{Colors.ENDC}")


if __name__ == "__main__":
    main()
