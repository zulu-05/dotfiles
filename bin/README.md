# Command-Line Tools & Utilities

## Overview

This directory contains a suite of professional-grade, command-line tools written in Python. These tools extend the shell's capabilities with complex functionality, primarily for Git and GitHub repository management.

Each tool is designed as a thin, user-facing wrapper that leverages the robust, tested, and modular `git_tools` library, also contained within this directory.

---

## Available Tools

| Tool                   | Description                                                | Usage                                        |
| ---------------------- | ---------------------------------------------------------- | -------------------------------------------- |
| `mkvenv`               | Creates and bootstraps a Python virtual environment.       | `mkvenv [prompt_name]`                       |
| `rmvenv`               | Safely removes a Python virtual environment.               | `rmvenv`                                     |
| `create_git_repo.py`   | Creates a local repo and a corresponding remote on GitHub. | `create_git_repo.py <repo_name>`             |
| `delete_git_repo.py`   | Deletes a repo from GitHub and the local system.           | `delete_git_repo.py <repo_dir_name>`         |
| `rename_git_repo.py`   | Renames a repo on GitHub and locally.                      | `rename_git_repo.py <old_name> <new_name>`   |
| `download_git_repo.py` | Clones one of your repos from GitHub via SSH.              | `download_git_repo.py <repo_name>`           |
| `upload_git_repo.py`   | Uploads a local-only repo to a new GitHub remote.          | `upload_git_repo.py`                         |
| `list_git_repos.py`    | Interactively lists and inspects your GitHub repos.        | `list_git_repos.py`                          |
| `check_git_repo.py`    | Checks the sync status of a local repo against its remote. | `check_git_repo.py [path]`                   |
| `show_git_repo.py`     | Sets a GitHub repository's visibility to public.           | `show_git_repo.py <repo_name>`               |
| `hide_git_repo.py`     | Sets a GitHub repository's visibility to private.          | `hide_git_repo.py <repo_name>`               |
| `find_and_replace.py`  | Finds and replaces text within files in a directory.       | `find_and_replace.py <find> <replace> [dir]` |
| `resize_image.py`      | Resizes one or more image files to a target width.         | `resize_image.py [files...] --width <px>`    |
| `open_web_server.py`   | Starts a simple web server in the current directory.       | `open_web_server.py`                         |

---

## Setup & Installation

The tools require a few Python packages to function. Install them using the provided `requirements.txt` file:

```bash
pip install -r requirements.txt
```
***

## Developer Guide

To contribute to these tools or modify their behavior, you must set up the full development environment. This ensures code quality, consistency, and correctness.

1. **Install Development Dependencies**
   This includes testing and quality assurance tools.

```bash
pip install -r requirements-dev.txt
```

2. **Run the Test Suite**
   Before committing any changes, ensure all tests pass. The test suite uses mocking to prevent any real network or filesystem operations.

```bash
pytest
```

3. **Activate Quality Assurance Hooks**
   This project uses `pre-commit` to automatically format code and check for errors before each commit. This is a one-time setup.

```bash
pre-commit install
```

Now, every time you run `git commit`, `black`, `flake8`, and `mypy` will automatically run, guaranteeing that all committed code adheres to the project's quality standards.
