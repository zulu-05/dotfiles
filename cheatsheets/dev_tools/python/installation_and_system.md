# Cheatsheet: Python System Integration & Installation

This guide covers Python's interaction with the operating system, focusing on installation, inspection, and safe management to avoid common system-level conflicts.

## Part 1: Installation Methods

### On Ubuntu/Debian

Use the system's package manager (`apt`) to install the official, stable version of Python. This ensures maximum compatibility with other system tools.

```bash
# Resynchronises the package index files from their sources.
sudo apt update

# Installs the three essential packages:
# the interpreter (python3),
# the package manager (python3-pip),
# and the virtual environment module (python3-venv)
sudo apt install python3 python3-pip python3-venv
```

## Part 2: Inspecting Your Python Installation

These commands help you find and understand your Python installation.

### Finding Executables

The `which` command searches your shell's `$PATH` to find the exact location of an executable.

```bash
# Find where the python3 executable is located
which python3
# Output: /usr/bin/python3

# Find where the pip executable is located
which pip3
# Output: /usr/bin/pip3
```

### Checking Versions

Always verify the versions of your tools to ensure compatibility.

| Command             | Description                                                               |
| ------------------- | ------------------------------------------------------------------------- |
| `python3 --version` | Shows the version of the Python interpreter.                              |
| `pip3 --version`    | Shows the version of the `pip` package manager and where it is installed. |

```bash
python3 --version
# Output: Python 3.13.5

pip3 --version
# Output: pip 25.1.1 from /usr/lib/python3/dist-packages/pip (python 3.13)
```

### Executable vs. Library Path

You might notice that `which` and `--version` report different paths for the same tool. This is normal and expected.

```bash
which pip3
# Output: /usr/bin/pip3

pip3 --version
# Output: pip 25.1.1 from /usr/lib/python3/dist-packages/pip (python 3.13)
```

- **`which pip3`** shows you the location of the **executable script**. This is a small wrapper file that your shell finds in its `$PATH`. Its only job is to start Python and run the `pip` library.
- **`pip3 --version`** reports the location of the **Python library code**. This is the actual directory containing all the `.py` files that make up the `pip` tool itself.

Think of `/usr/bin/pip3` as a desktop shortcut, and `/usr/lib/python3/dist-packages/pip` as the actual application that the shortcut points to.

### Understanding Package Locations

`pip` installs packages into a directory called `site-packages`. The `site` module helps you find these locations.

|Command|Description|
|---|---|
|`python3 -m site`|Displays detailed path information, including the locations for system-wide packages (`SITE_PACKAGES`) and user-specific packages (`USER_SITE`).|

```bash
python3 -m site
# USER_BASE: "/home/user/.local" (for --user installs)
# USER_SITE: "/home/user/.local/lib/python3.13/site-packages"
# SITE_PACKAGES: [
#   '/usr/lib/python3/dist-packages',
#   '/usr/lib/python3.13/dist-packages',
# ]
```

### The Module Search Path (`sys.path`)

When you write `import my_module`, Python searches a list of directories defined in `sys.path`. This is the key to debugging `ModuleNotFoundError`.

```bash
# Use a short command to pretty-print the sys.path list
python3 -c "import sys; from pprint import pprint; pprint(sys.path)"
# Output:
# [
#  '',  <-- The current directory is always searched first
#  '/usr/lib/python313.zip',
#  '/usr/lib/python3.13',
#  '/usr/lib/python3.13/lib-dynload',
#  '/home/user/.local/lib/python3.13/site-packages', <-- User packages
#  '/usr/lib/python3/dist-packages' <-- System packages
# ]
```

When you write `import my_module`, Python doesn't magically know where to find `my_module.py`. Instead, it searches a specific list of directories. That list is called the **module search path**, and it's stored in a variable named `sys.path`.

#### How to View It

You can see the exact search path your Python interpreter is using with this one-liner:

Bash

```bash
python3 -c "import sys; from pprint import pprint; pprint(sys.path)"
```

#### The Search Order

Python searches the directories in `sys.path` in a specific order and uses the **first match it finds**. The typical order is:

1. **The Script's Directory:** The directory containing the script you are running. If you are in the interactive interpreter, this is an empty string `''`, which means the current working directory.
2. **`$PYTHONPATH` Directories:** Any directories you've added to your `$PYTHONPATH` environment variable (if any).
3. **User `site-packages`:** The directory where user-specific packages are installed (`~/.local/lib/pythonX.Y/site-packages`).
4. **System `site-packages`:** The system-wide directories where packages installed by `apt` or a global `pip` are located (e.g., `/usr/lib/python3/dist-packages`).

#### How to Modify `sys.path`

- **Temporarily (In Code):** The most common and controlled way to modify the path is to append a directory to the `sys.path` list at the beginning of your script. This is useful for complex local project structures.

```python
import sys
from pathlib import Path
   
# Add the parent directory of this script to the search path
# so we can import modules from sibling directories.
script_dir = Path(__file__).parent
sys.path.append(str(script_dir.parent))

import my_sibling_module
```

- **Permanently (Via `$PYTHONPATH`):** As covered in the next section, you can use the `$PYTHONPATH` environment variable to add directories to the path for all Python scripts you run.

#### Practical Use Case: Debugging `ModuleNotFoundError`

When you get a `ModuleNotFoundError: No module named 'some_module'`, `sys.path` is your primary debugging tool.

1. Run `python3 -c "import sys; pprint(sys.path)"` from the same directory where you ran your failing script.
2. Look at the output. Is the directory containing `some_module.py` actually in the list?
3. If not, you know you have a path problem and need to either restructure your project or temporarily modify `sys.path` as shown above.

### Modifying the Search Path: The `PYTHONPATH` Environment Variable

`$PYTHONPATH` is a powerful, and sometimes risky, environment variable that allows you to control Python's module search path from your shell.

#### Concept

`$PYTHONPATH` is an environment variable that contains a list of directory paths, separated by colons (similar to your shell's `$PATH`). When Python starts, it takes these directories and inserts them near the beginning of its `sys.path` list. This means Python will look for modules in these directories _before_ it looks in the standard `site-packages` locations.

#### Workflow Example

This is useful for making a personal library of utility scripts available to all your projects without needing to install it each time.

**1. You have a personal library of scripts:**

```bash
/home/user/my_python_libs/
└── str_utils.py
```

**2. In a different project, you try to import it, which fails:**

```python
# /home/user/some_project/main.py
import str_utils # Fails with ModuleNotFoundError
```

**3. Set `$PYTHONPATH` in your shell:**

```bash
# Add your library's path to the PYTHONPATH variable.
# This can be added to your .bashrc file to make it permanent.
export PYTHONPATH="$HOME/my_python_libs"
```

**4. Now, the import works from anywhere:** When you run `python3 /home/user/some_project/main.py`, Python will now successfully find and import `str_utils`.

#### **Warning: Use with Caution**

While useful for personal scripts, relying on `$PYTHONPATH` for shareable projects is a **bad practice**.

- **It creates "magic" dependencies.** Another developer who clones your project will not have the same `$PYTHONPATH` set, and the code will fail for them with no obvious reason why.
- **It makes environments non-reproducible.** A project's dependencies should be explicitly listed in its `requirements.txt` or `pyproject.toml` file, not hidden in a developer's shell configuration.

For shareable projects, the correct way to make local code importable is to install it in an editable mode with `pip install -e .`.

## Part 3: System Integration & Safety Rules

### The `apt` vs. `pip` Distinction

|Tool|Manages|Scope|
|---|---|---|
|`apt`|**System Software.** Libraries and applications that the entire operating system and other system tools depend on (e.g., `python3-requests`).|System-wide|
|`pip`|**Python Libraries.** Libraries for your specific development projects.|Project-specific (inside a `venv`)|

#### The "Externally Managed Environment" Error (PEP 668)

On modern Linux systems, trying to install a package globally with `pip` will trigger this error. This is a crucial safety feature to prevent you from breaking your OS.

**Example Error:**

```bash
pip install requests
# error: externally-managed-environment
# × This environment is externally managed
# ╰─> To install Python packages system-wide, try apt install
#     python3-requests, or use a virtual environment
```

**What it means:** `pip` is refusing to modify the global, system-wide Python installation because it is managed by `apt`.

**How to Solve It:**

1. **For Project Dependencies (99% of cases):** Create and activate a **virtual environment**. This is the standard, correct solution.

```bash
python3 -m venv venv
source venv/bin/activate
# (venv) $ pip install requests  <-- This will now work correctly.
```

2. **For Global CLI Tools:** Use the `--user` flag.

```bash
pip install --user yt-dlp
```

> **Warning:** The error message may suggest using a `--break-system-packages` flag. **Do not use this.** It is an escape hatch that disables this crucial safety feature and puts your system at risk of corruption.

#### The Danger of `sudo pip install`

The "externally managed" safeguard exists to prevent the historical mistake of running `pip` with `sudo`. This command is dangerous because it can overwrite or delete files managed by `apt`, potentially breaking system utilities that rely on specific library versions. **Avoid this command at all costs.**

### User-Level CLI Tools (`pip install --user`)

This is the correct and safe way to install a Python-based command-line tool that you want to be available everywhere for your user, without interfering with the system or needing a virtual environment.

#### How It Works

The `--user` flag tells `pip` to install packages into your user's home directory instead of the system-wide location. This provides a perfect middle ground between a temporary virtual environment and the dangerous global scope.

- **Libraries are installed to:** `~/.local/lib/pythonX.Y/site-packages/`
- **Executables are installed to:** `~/.local/bin/`

Because these paths are inside your home directory, you never need `sudo` to manage them.

#### The Workflow

Here is the complete process for installing and managing a user-level CLI tool.

```bash
# 1. Ensure ~/.local/bin is in your shell's $PATH.
# Use the 'ppath' alias we created to check.
ppath
# If you don't see '/home/your_user/.local/bin' in the list, add this
# line to your ~/.bashrc or equivalent and restart your shell:
# export PATH="$HOME/.local/bin:$PATH"

# 2. Install a tool. Let's use 'cowsay'.
pip install --user cowsay

# 3. Verify where the executable was installed.
which cowsay
# Output: /home/user/.local/bin/cowsay

# 4. Run the command!
cowsay "Hello, user-level packages!"
#  ___________________________________
# < Hello, user-level packages! >
#  -----------------------------------
#         \   ^__^
#          \  (oo)\_______
#             (__)\       )\/\
#                 ||----w |
#                 ||     ||

# 5. List ONLY the packages you have installed at the user level.
pip list --user
# Package Version
# ------- -------
# cowsay  6.1

# 6. Uninstall the package when you no longer need it.
pip uninstall cowsay
```

### How `pip` Creates Commands: Entry Points

When you install a package like `cowsay` and can immediately run `cowsay` as a command, it's not magic. The package developer has defined an "entry point" that tells `pip` to create a command-line script.

#### Concept: The `[project.scripts]` section

In a modern Python project, the `pyproject.toml` file is used to configure the package. Inside this file, a special section called `[project.scripts]` maps command names to the Python functions they should execute.

When you run `pip install`, `pip` reads this map and automatically generates a small executable wrapper script in the appropriate `bin/` directory (e.g., `~/.local/bin` for user installs, or a venv's `bin/`).

#### Workflow Example

Let's create a minimal project called `greetme` that provides a `greet` command.

**1. Create the project structure:**

```bash
greetme/
├── pyproject.toml
└── greetme/
    ├── __init__.py
    └── cli.py
```

**2. Write the Python function in `greetme/cli.py`:**

```python
# greetme/cli.py
import sys

def main():
    name = sys.argv[1] if len(sys.argv) > 1 else "World"
    print(f"Hello, {name}!")
```

**3. Define the entry point in `pyproject.toml`:** This is the crucial step. We are telling `pip` to create a command named `greet` that, when run, will execute the `main` function inside the `greetme.cli` module.

```toml
# pyproject.toml
[project]
name = "greetme"
version = "0.1.0"

[project.scripts]
greet = "greetme.cli:main"
```

**4. Install the package in editable mode:** From the top-level `greetme/` directory, run:

```bash
# The '-e' flag is for "editable", which is great for development.
# The '.' means "install the project in the current directory".
pip install -e .
```

**5. Verify the command was created:** `pip` has now created a wrapper script in your virtual environment's `bin` directory.

```bash
which greet
# Output: /path/to/your/venv/bin/greet
```

**6. Run your new command!**

```bash
greet
# Hello, World!

greet Alice
# Hello, Alice!
```

**7. (Optional) Inspect the generated script:** If you look at the file `pip` created, you can see it's just a simple script that imports and runs your `main` function. This demystifies the process entirely.

```bash
cat $(which greet)
# #!/path/to/your/venv/bin/python3
# -*- coding: utf-8 -*-
# import re
# import sys
# from greetme.cli import main
# if __name__ == '__main__':
#     sys.exit(main())
```

### Understanding Python Packaging: Wheels vs. Source Distributions

When you run `pip install`, it downloads a package file from PyPI. These files come in two main formats, and the one `pip` chooses has a big impact on installation speed and reliability.

#### Concept: The Two Package Types

1. **Wheels (`.whl` files):**
    - **What they are:** Pre-compiled packages. They are essentially ZIP files containing all the necessary files and metadata, ready to be unpacked directly into your `site-packages` directory.
    - **Analogy:** A pre-assembled piece of furniture.
    - **Result:** **Fast, reliable, and preferred.** The installation is a simple copy operation.

2. **Source Distributions (`.tar.gz` or "sdist"):**
    - **What they are:** Archives containing the raw source code (`.py` files), build scripts (`setup.py` or `pyproject.toml`), and metadata.
    - **Analogy:** A flat-pack box of furniture with instructions and screws.
    - **Result:** **Slow and potentially fragile.** `pip` must execute the build process on your machine to generate the final files before it can install them. This can fail if you are missing system-level dependencies (like a C compiler for a package with C extensions).

`pip` will always try to download and install a Wheel if it can find one that is compatible with your system (Python version, OS, architecture). If it can't, it will fall back to a source distribution.

#### Workflow Example: Seeing the Difference

You can see which type of package `pip` is using with the `--verbose` flag. Let's try to install `numpy`, a package that has many pre-compiled wheels.

```bash
# Use --verbose to see the download details
pip install --verbose numpy
```

**Output when a Wheel is found (The good case):** You will see a line indicating `pip` found a compatible `.whl` file. Notice the filename contains tags for the Python version (`cp310`), architecture (`x86_64`), and OS (`manylinux`).

```bash
  Downloading numpy-1.26.4-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (18.2 MB)
...
Installing collected packages: numpy
Successfully installed numpy-1.26.4
```

**Output when only a Source Distribution is found (The slow case):** If no compatible wheel exists, `pip` will download the `.tar.gz` file and you will see a lot of output as it runs the build process on your machine.

```bash
  Downloading numpy-1.26.4.tar.gz (10.9 MB)
...
  Running setup.py bdist_wheel for numpy ...  <-- You see this build step
...
Successfully installed numpy-1.26.4
```

#### Why It Matters

- **As a user:** If a package installation is slow or fails with compiler errors, it's likely because `pip` had to use a source distribution.
- **As a developer:** When you publish your own packages, you should always provide pre-compiled wheels to ensure your users have a fast and reliable installation experience.

## Part 5: Managing Multiple Python Versions (`pyenv`)

As a developer, you will often need to work on different projects that require different versions of Python (e.g., a legacy project on Python 3.8 and a new one on Python 3.11). `pyenv` is a powerful tool that lets you install multiple Python versions on the same machine and easily switch between them.

#### Concept

`pyenv` works by intercepting the `python` command with a special script called a "shim." When you run `python`, the shim checks for a `.python-version` file in your current directory, or a global setting, to decide which of your installed Python versions to actually run. This allows you to set your Python version on a per-project basis.

#### The Workflow

This is the typical process for managing and switching between Python versions with `pyenv`.

```bash
# 1. See a list of all available Python versions you can install.
pyenv install --list

# 2. Install a specific version of Python. This can take a few minutes as it
# compiles Python from source.
pyenv install 3.9.18

# 3. List all the Python versions currently installed on your system.
# The '*' indicates the currently active version.
pyenv versions
# * system (set by /home/user/.pyenv/version)
#   3.9.18
#   3.10.12

# 4. Set the global default Python version. This is the version that will be
# used in any directory that doesn't have a project-specific version set.
pyenv global 3.10.12

# 5. Now, navigate to a specific project and set a local, project-specific version.
cd ~/my-legacy-project/
pyenv local 3.9.18
# This command creates a hidden .python-version file in the current directory.

# 6. Verify the active version. pyenv automatically switches based on your location.
python --version
# Output: Python 3.9.18

# 7. Move out of that directory, and your version reverts to the global default.
cd ..
python --version
# Output: Python 3.10.12
```

#### Command Reference

|Command|Description|
|---|---|
|`pyenv install [version]`|Installs a specific version of Python.|
|`pyenv versions`|Lists all Python versions installed by `pyenv`.|
|`pyenv global [version]`|Sets the default, system-wide Python version for your user.|
|`pyenv local [version]`|Sets the Python version for the current directory and all subdirectories by creating a `.python-version` file.|
|`pyenv shell [version]`|Sets the Python version for the _current shell session only_. This overrides any `local` or `global` settings.|
|`pyenv which [command]`|Shows the full path to an executable. This helps verify that the shim is working correctly (e.g., `pyenv which python`).|
