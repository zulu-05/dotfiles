# Cheatsheet: Python Environments & Dependencies

This guide covers the modern, best-practice workflow for managing Python projects, focusing on virtual environments and reproducible dependency management.

## Part 1: The Principle of Isolation

The most important rule in modern Python development is: **every project must have its own isolated environment.**

**The Problem:** If you install all your packages globally, you will inevitably run into conflicts. Project A might need version 1.0 of a library, while Project B needs version 2.0. Installing one will break the other.

**The Solution:** A **virtual environment** is a self-contained directory that holds a specific version of the Python interpreter and its own set of independent libraries. This ensures that the dependencies for one project do not affect any other project on your system.

## Part 2: Virtual Environments (`venv`)

Python's built-in `venv` module is the standard tool for creating lightweight virtual environments.

### The `venv` Workflow

This is the standard sequence of commands you will use for every new Python project.

```bash
# 1. Create a new directory for your project and enter it.
mkdir my-python-project
cd my-python-project

# 2. Create the virtual environment.
# 'python3 -m venv' tells Python to run the 'venv' module.
# The second 'venv' is the name of the directory to create. This is the standard name.
python3 -m venv venv

# You will now see a 'venv/' directory. This directory should be added to your .gitignore file.
ls -F
# venv/

# 3. Activate the virtual environment.
# This modifies your shell's PATH to prioritize the Python and pip executables
# inside the 'venv' directory.
source venv/bin/activate

# Your shell prompt will change to show that the environment is active.
# (venv) $ 

# 4. Work on your project... install packages, write code...

# 5. When you are done, deactivate the environment to return to your global shell.
deactivate

# Your shell prompt returns to normal.
# $
```

### `venv` Commands

|Command|Description|
|---|---|
|`python3 -m venv [dir_name]`|**Creates** a new virtual environment in a directory named `[dir_name]`. The standard convention is to name it `venv`.|
|`source [dir_name]/bin/activate`|**Activates** the environment. You must run this every time you start a new terminal session to work on the project.|
|`deactivate`|**Deactivates** the environment, returning you to your system's global Python installation.|

## Part 3: Package Management (`pip`)

`pip` is Python's official package installer. When a virtual environment is active, `pip` will install packages _inside_ that environment, keeping your global Python installation clean.

### Main Commands

| Command     | Description                                                    |
| ----------- | -------------------------------------------------------------- |
| `install`   | Installs packages.                                             |
| `uninstall` | Uninstalls packages.                                           |
| `list`      | Lists installed packages.                                      |
| `freeze`    | Outputs installed packages in requirements format.             |
| `show`      | Shows detailed information about an installed package.         |
| `search`    | Searches the Python Package Index (PyPI) for packages.         |
| `check`     | Verifies that installed packages have compatible dependencies. |
| `download`  | Downloads packages without installing them.                    |
| `wheel`     | Builds "wheel" archives from your project.                     |
| `help`      | Shows help for a command.                                      |

#### Workflow 1: Project Setup & Dependency Management

This sequence shows the typical lifecycle of adding, documenting, and removing a dependency in a project.

```bash
# You are inside an active virtual environment.

# 1. Check what's currently installed.
pip list
# Package    Version
# ---------- -------
# pip        24.0
# setuptools 69.5.1

# 2. Install a new package for your project.
pip install requests

# 3. Get detailed information about the package you just installed,
# including what other dependencies it brought in.
pip show requests
# Name: requests
# Version: 2.32.3
# ...
# Requires: certifi, charset-normalizer, idna, urllib3

# 4. After confirming your code works, update your project's
# requirements file to include the new package for your teammates.
pip freeze > requirements.txt

# 5. Later, you decide to use a different library and no longer need 'requests'.
pip uninstall requests
```

#### Workflow 2: Checking Environment Health

These commands are useful for maintaining an existing project.

```bash
# 1. Check if any of your project's dependencies are out of date.
pip list --outdated
# Package  Version Latest Type
# -------- ------- ------ -----
# Flask    3.0.2   3.0.3  wheel

# 2. After installing or updating packages, it's good practice
# to verify that there are no version conflicts in your environment.
pip check
# No broken requirements found.
```

#### Workflow 3: Offline Installation

This workflow is for installing packages on a machine that does not have an internet connection.

```bash
# --- On a machine WITH internet ---

# 1. Create a directory to hold the packages.
mkdir offline_packages

# 2. Download a package AND all of its dependencies into that directory.
pip download requests -d ./offline_packages/

# 3. Transfer the 'offline_packages' directory to the offline machine.

# --- On the OFFLINE machine ---

# 4. Install the packages from the local directory, telling pip not to
# look for them on the internet.
pip install --no-index --find-links=./offline_packages/ requests
```

#### Workflow 4: Building a Distributable Package

This is for when you are the developer of a Python package and you want to create a distributable file that others can install.

```bash
# You are in the root of your Python project, which has a setup.py or pyproject.toml file.

# 1. Ensure the 'wheel' package is installed.
pip install wheel

# 2. Run the wheel command. The '.' refers to the current directory.
pip wheel . -w dist

# Command will build your project and place the resulting .whl file
# in a new 'dist/' directory.
# Processing /path/to/my_project
#   Building wheel for my_project (setup.py) ... done
#   Stored in directory: ...
# Successfully built my_project
# ls dist/
# my_project-1.0.0-py3-none-any.whl

# 3. You can now distribute this .whl file, and others can install it.
pip install ./dist/my_project-1.0.0-py3-none-any.whl
```

### `pip install` Options

This is the most complex command with the most options.

#### Core Functionality

| Flag(s)                    | Description                                                                                                                                                                                                                                                                           |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-r, --requirement <file>` | Install from the given **r**equirements file. This is the cornerstone of reproducible environments.                                                                                                                                                                                   |
| `-U, --upgrade`            | **U**pgrade the specified package(s) to the newest available version.                                                                                                                                                                                                                 |
| `--user`                   | Install to the user `site-packages` directory, which is specific to your user account and does not require root privileges.                                                                                                                                                           |
| `-e, --editable <path>`    | Installs a project in **e**ditable mode. Instead of copying the files, `pip` creates a link to your source code. This means any changes you make to the source code are immediately reflected in the installed package without needing to reinstall. Essential for local development. |

##### Workflow Examples

```bash
# Workflow 1: Setting up a project from a requirements file
# You've just cloned a repository and need to install its dependencies.
source venv/bin/activate
pip install -r requirements.txt

# Workflow 2: Upgrading a specific package
# You find out there's a new version of Flask with a feature you need.
pip install --upgrade Flask
# or
pip install -U Flask

# Workflow 3: Local package development
# You are developing 'my-local-package' and want to test it in another project.
cd /path/to/my-other-project
source venv/bin/activate
# Install 'my-local-package' in editable mode.
pip install -e /path/to/my-local-package
# Now, any changes you make in '/path/to/my-local-package' will be
# immediately available in 'my-other-project' without reinstalling.
```

#### Package Source Options

| Flag(s)                       | Description                                                                                                         |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `-i, --index-url <url>`       | The base URL of the Python Package **I**ndex. Use this to install from a private or alternative package repository. |
| `--extra-index-url <url>`     | An additional index URL to use alongside the main one.                                                              |
| `--no-index`                  | Ignores the package index entirely. Only looks for packages in locations specified with `--find-links`.             |
| `-f, --find-links <url/path>` | A URL or local path to a directory where `pip` can **f**ind package archives (wheels or source distributions).      |

##### Workflow Examples

```bash
# Workflow 1: Installing from a private repository
# Your company has a private PyPI server for internal packages.
pip install --index-url https://private.pypi.org/simple \
            --extra-index-url https://pypi.org/simple \
            my-internal-package
# This tells pip to look for 'my-internal-package' on the private server first,
# but still fall back to the public PyPI for other dependencies like 'requests'.

# Workflow 2: Installing from local files (offline installation)
# You have downloaded all necessary .whl files into a folder named 'local_packages'.
pip install --no-index --find-links=./local_packages/ requests
# --no-index tells pip NOT to connect to the internet.
# --find-links tells pip to look for the packages in the specified local folder.
```

#### Dependency Handling

|Flag(s)|Description|
|---|---|
|`--no-deps`|**No Dep**endencies. Do not install the dependencies of the packages you are installing.|
|`--pre`|Include **pre**-release and development versions. By default, `pip` only finds stable versions.|

##### Workflow Examples

```bash
# Workflow 1: Installing a package for an environment with managed dependencies
# You are in an environment (like a Docker container) where you know all
# dependencies are already installed and you just need to add one specific tool.
pip install --no-deps my-tool

# Workflow 2: Testing a beta version of a library
# You want to test the upcoming beta release of Django.
pip install --pre django
```

### `pip uninstall` Options

| Flag(s)                    | Description                                                       |
| -------------------------- | ----------------------------------------------------------------- |
| `-r, --requirement <file>` | Uninstall all the packages listed in the given requirements file. |
| `-y, --yes`                | Don't ask for confirmation of removal. Essential for scripting.   |

#### Workflow Example: Decommissioning a Project

This is useful when you are archiving a project and want to clean up its virtual environment to save space.

```bash
# You are inside the project's active virtual environment.

# 1. Uninstall all packages listed in the requirements file without
#    being prompted for each one.
pip uninstall -r requirements.txt -y

# 2. Verify that the environment is now clean (except for pip itself).
pip list
# Package    Version
# ---------- -------
# pip        24.0
# setuptools 69.5.1
```

### `pip list` Options

|Flag(s)|Description|
|---|---|
|`--outdated`|Lists all installed packages that have a newer version available on PyPI.|
|`--user`|Only list packages installed in the user `site-packages` directory.|
|`--local`|Only list packages installed in the current environment (hides globally-installed packages if you are in a `venv`).|
|`--format <format>`|Changes the output format. `freeze` (the default), `columns` (more readable), or `json`.|

#### Workflow Example: Environment Maintenance & Inspection

These flags are your primary tools for understanding the state of your Python environment.

```bash
# Workflow 1: Checking for potential updates in a project
source venv/bin/activate
pip list --outdated
# Package            Version Latest  Type
# ------------------ ------- ------- -----
# Flask              3.0.2   3.0.3   wheel
# Werkzeug           3.0.2   3.0.3   wheel

# Workflow 2: Seeing what you've installed globally for your user
# (Run this outside of any virtual environment)
pip list --user
# Package Version
# ------- -------
# cowsay  6.1
# httpie  3.2.2

# Workflow 3: Getting a clean list of only project-specific packages
# Sometimes a venv is created with access to system packages. --local filters them out.
source venv/bin/activate
pip list --local
# This will only show packages installed inside the 'venv/' directory.
```

## Part 4: Reproducible Environments (`requirements.txt`)

To share your project with others or to deploy it to a server, you need a way to specify its exact dependencies. This is done with a `requirements.txt` file.

### The End-to-End Workflow

This workflow ensures that anyone can perfectly replicate your project's environment.

**Developer A (Initial Setup):**

```bash
# 1. Create and activate the environment.
mkdir my-app && cd my-app
python3 -m venv venv
source venv/bin/activate

# 2. Install the necessary packages.
pip install requests flask

# 3. Generate the requirements file.
# 'pip freeze' lists all installed packages with their exact versions.
# The '>' redirects that output into a file.
pip freeze > requirements.txt

# 4. Add the venv directory to .gitignore and commit requirements.txt to Git.
echo "venv/" > .gitignore
git init
git add .
git commit -m "Initial project setup with dependencies"
```

**Developer B (or a Server) Sets Up the Project:**

```bash
# 1. Clone the repository.
git clone https://github.com/user/my-app.git
cd my-app

# 2. Create and activate a fresh virtual environment.
python3 -m venv venv
source venv/bin/activate

# 3. Install all the dependencies from the requirements file in one command.
# The -r flag stands for 'requirement'.
pip install -r requirements.txt

# The environment now has the exact same package versions as Developer A.
```

## Part 5: Best Practice (`pip-tools`)

For larger projects, `pip freeze` can be problematic because it mixes your direct dependencies (like `flask`) with their sub-dependencies (like `werkzeug`). This makes updates difficult. `pip-tools` provides a superior workflow.

**The `pip-tools` Workflow:**

1. **Install `pip-tools`:** `pip install pip-tools`
2. **Create `requirements.in`:** In this file, you list _only_ the packages your project directly imports.

```bash
# requirements.in
flask
requests
```

3. **Compile the file:** Run the `pip-compile` command.

```bash
pip-compile requirements.in
```

This generates a `requirements.txt` file that is beautifully commented and contains your direct dependencies _and_ all their sub-dependencies, pinned to the latest compatible versions.

```bash
#
# This file is autogenerated by pip-compile with Python 3.13
#
# ...
click==8.1.7
    # via flask
flask==3.0.3
    # via -r requirements.in
# ... and so on
```

4. **Install the dependencies:** You can now install from the generated file.

```bash
pip install -r requirements.txt
```

Or, even better, use `pip-sync`, which ensures your environment _exactly_ matches the requirements file, removing any packages that don't belong.

```bash
pip-sync
```

This gives you the best of both worlds: a simple file (`requirements.in`) to manage your direct dependencies, and a perfectly reproducible lock file (`requirements.txt`) for installation.