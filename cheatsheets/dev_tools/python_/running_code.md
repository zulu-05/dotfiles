# Cheatsheet: Running Python Code

This guide is a focused reference for the `python3` executable itself—how to run scripts, control the interpreter with flags, and use the interactive mode for experimentation.

## Part 1: Executing Scripts

This is the most common way to run a Python program.

### Basic Execution

You pass the name of the script file as an argument to the `python3` interpreter.

```bash
# Run a script named my_app.py located in the current directory
python3 my_app.py
```

### Direct Execution (Shebang & Permissions)

For command-line tools and scripts, it's common to make them directly executable so you don't have to type `python3` every time. This is a two-step process.

**Step 1: Add a "Shebang" Line** The shebang is a special line at the very top of your script that tells the shell which interpreter to use to run the file. The `env` command is used to find the `python3` executable in your `$PATH`, making your script more portable.

```bash
#!/usr/bin/env python3

import sys

print(f"Hello from a script! You passed {len(sys.argv)} arguments.")
```

**Step 2: Make the Script Executable** Use the `chmod` command to add the "execute" (`x`) permission for your user (`u`).

```bash
chmod u+x my_script.py
```

Now you can run the script directly:

```bash
./my_script.py
# Output: Hello from a script! You passed 1 arguments.
```

## Part 2: The Interactive REPL (Read-Eval-Print Loop)

Running `python3` with no arguments starts the interactive interpreter. This is an excellent tool for quick experiments, testing small code snippets, or performing calculations without needing to create a file.

### Workflow

```bash
# 1. Start the interpreter
python3
# Python 3.13.5 (main, Jun 05 2025, 15:14:05) [GCC 11.4.0] on linux
# Type "help", "copyright", "credits" or "license" for more information.
# >>>

# 2. Run some commands
# >>> import math
# >>> message = "Hello, REPL!"
# >>> print(message.upper())
# HELLO, REPL!
# >>> 2**10
# 1024

# 3. Exit the interpreter
# >>> exit()
```

You can also exit the REPL by pressing `Ctrl+D`.

## Part 3: Interpreter Flags (Command-Line Options)

You can modify the interpreter's behaviour by passing flags before your script name.

### Core Execution Options

| Flag                   | Description                                                                                                                                                                                                  |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **-m [module]**        | **(Module)** Runs a library module as a script. This is the correct and standard way to invoke tools like `venv` and `pip` because it ensures you are using the module from the correct Python installation. |
| **-c "[cmd]"**         | **(Command)** Executes a short string of Python code directly from the command line without needing to create a `.py` file. Very useful for quick, one-line shell commands.                                  |
| **-i**                 | **(Interactive)** Enters the interactive REPL _after_ running a script. This is incredibly useful for debugging, as all the script's variables and functions will be available for you to inspect.           |

### Informational Options

| Flag(s)           | Description                                                                   |
| ----------------- | ----------------------------------------------------------------------------- |
| `-V`, `--version` | **(Version)** Prints the Python version number and exits.                     |
| `-h`, `--help`    | **(Help)** Prints the full help message with all available options and exits. |

### Configuration & Environment Options

| Flag(s) | Description                                                                                                                                |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `-E`    | Ignores all `PYTHON*` environment variables (e.g., `PYTHONPATH`) that could alter Python's behavior.                                       |
| `-s`    | Prevents the user's `site-packages` directory from being added to `sys.path`.                                                              |
| `-S`    | Disables the import of the `site` module, which is responsible for setting up site-specific paths.                                         |
| `-v`    | **V**erbose mode. Prints a message each time a module is initialized, showing its location. Use multiple times (`-vv`) for more verbosity. |

### Practical Examples

**Using `-m` to run modules**
This is the correct way to run built-in tools to ensure you're using the one that belongs to the `python3` executable you specify.

```bash
# Create a virtual environment using the 'venv' module
python3 -m venv my_project_env

# Run pip to install packages, guaranteeing it's the pip for this Python
python3 -m pip install requests
```

**Using `-c` for one-liners**
Execute short commands without creating a file. This is perfect for quick checks.

```bash
# A quick way to pretty-print a JSON string from the command line
echo '{"name": "test", "data": [1, 2, 3]}' | python3 -c "import sys, json; pprint(json.load(sys.stdin))"

# Check the system's PATH variable from within Python
python3 -c "import sys; from pprint import pprint; pprint(sys.path)"
```

**Using `-i` for debugging** 
First, create a simple script `myscript.py`:

```bash
# my_script.py
x = 100
y = [1, 2, 3]

def my_func(val):
    return val * 2
```

Now, run it with the `-i` flag to inspect its state after it runs:

```bash
python3 -i my_script.py
# >>>
# The script runs, and then you are dropped into the REPL.
# Now you can inspect the state of the script.
# >>> x
# 100
# >>> y.append(4)
# >>> y
# [1, 2, 3, 4]
# >>> my_func(x)
# 200
```

**Using `-V` and `-h` for Information**
These flags provide basic information about the interpreter.

```bash
# Check your Python version
python3 --version
# Python 3.13.5

# Display all available command-line options
python3 --help
# usage: python3 [option] ... [-c cmd | -m mod | file | -] [arg] ...
# Options and arguments (and corresponding environment variables):
# ...
```

**Using `-E`, `-s`, and `-S` to Isolate Python**
These flags are for running Python in a "clean" environment, ignoring potentially disruptive user or system configurations.

First, set a `PYTHONPATH` environment variable that points to a directory with a dummy module.

```bash
# Create a dummy library and module
mkdir -p my_libs
echo 'print("Custom module loaded!")' > my_libs/custom_module.py

# Set PYTHONPATH so Python can find this module
export PYTHONPATH=$(pwd)/my_libs

# By default, Python finds and imports the module
python3 -c "import custom_module"
# Custom module loaded!

# Now, use the -E flag to ignore the PYTHONPATH variable
python3 -E -c "import custom_module"
# Traceback (most recent call last):
#   ...
# ModuleNotFoundError: No module named 'custom_module'
```

The `-s` and `-S` flags provide a more surgical isolation by preventing `site-packages` from being added to your path.

#### Using `-v` for Verbose Import Logging

The `-v` flag is excellent for debugging `import` issues by showing exactly where Python is searching for and finding modules.

```bash
# Run a simple import with verbosity on
python3 -v -c "import json"
# ... (lots of output)
# import 'json' # <_frozen_importlib_external.SourceFileLoader object at ...> from '/usr/lib/python3.13/json/__init__.py'
# ...
```