# Cheatsheet: Python Standard Library Essentials

This guide is a quick reference for some of the most important "batteries included" with Python that developers use daily for common tasks.

## Part 1: Modern Filesystem Paths (`pathlib`)

The `pathlib` module provides a modern, object-oriented way to handle filesystem paths. It is safer, more intuitive, and more readable than the older string-based `os.path` functions.

### The Old Way vs. The New Way

**The Old Way (using `os.path`):**

```bash
import os

home = os.path.expanduser("~")
config_path = os.path.join(home, ".config", "my_app", "settings.json")

if os.path.exists(config_path):
    print(f"Config file found at: {config_path}")
```

**The Modern Way (using `pathlib`):**

```bash
from pathlib import Path

# The '/' operator is overloaded to intelligently join path components.
config_path = Path.home() / ".config" / "my_app" / "settings.json"

if config_path.exists():
    print(f"Config file found at: {config_path}")
```

### `pathlib` Workflow & Common Attributes

`Path` objects make path manipulation feel natural.

```bash
from pathlib import Path

# Create a Path object for the current directory
p = Path.cwd()

# Create a new path object for a file inside it
log_file = p / "logs" / "app.log"

# --- Common Attributes ---
print(f"Full Path: {log_file}")         # .../logs/app.log
print(f"Parent Dir: {log_file.parent}") # .../logs
print(f"Filename: {log_file.name}")     # app.log
print(f"File Stem: {log_file.stem}")     # app
print(f"Extension: {log_file.suffix}")   # .log

# --- Common Methods ---
if not log_file.parent.exists():
    log_file.parent.mkdir(parents=True)

# Write text to the file (handles opening/closing automatically)
log_file.write_text("INFO: Application started.\n")

# Read text from the file
content = log_file.read_text()
print(content)
```

## Part 2: System Interaction (`os` and `sys`)

These modules provide the primary interface to the operating system and the Python interpreter itself.

|Module|Common Use|Example|
|---|---|---|
|`os`|**Operating System Interface.** The most common use is accessing environment variables via the `os.environ` dictionary-like object.|`api_key = os.environ.get("API_KEY", "default_value")`|
|`sys`|**System-specific Parameters.** The most common use is accessing command-line arguments passed to your script via the `sys.argv` list.|`import sys`<br>`if len(sys.argv) > 1:`<br>    `filename = sys.argv[1]`<br>`else:`<br>    `sys.exit("Error: Missing filename argument")`|

## Part 3: Data Handling (`json`)

The `json` module is the standard tool for working with JSON (JavaScript Object Notation) data, which is the de facto standard for APIs and configuration files.

### Serializing (Python to JSON)

"Serializing" or "dumping" means converting a Python object (like a dictionary or list) into a JSON string.

|Function|Description|
|---|---|
|`json.dumps()`|**(Dump String)** Converts a Python object into a JSON-formatted string.|
|`json.dump()`|**(Dump to File)** Serializes a Python object and writes it directly to a text file.|

**Example:**

```bash
import json

# A Python dictionary
data = {
    "user": "admin",
    "permissions": ["read", "write"],
    "is_active": True,
    "session_id": 12345
}

# Convert the dictionary to a JSON string
# indent=4 makes the output human-readable
json_string = json.dumps(data, indent=4)
print(json_string)

# Write the dictionary directly to a file
with open("data.json", "w") as f:
    json.dump(data, f, indent=4)
```

### Deserializing (JSON to Python)

"Deserializing" or "loading" means parsing a JSON string or file and converting it back into a Python object.

|Function|Description|
|---|---|
|`json.loads()`|**(Load String)** Parses a JSON-formatted string and returns a Python object.|
|`json.load()`|**(Load from File)** Reads from a text file containing JSON data and returns a Python object.|

**Example:**

```bash
import json

# A JSON string
json_data_string = '{"name": "test", "status": "ok", "values": [1, 2, 3]}'

# Parse the string into a Python dictionary
python_dict = json.loads(json_data_string)
print(python_dict["status"])  # Output: ok

# Assume we have a 'data.json' file from the previous example
with open("data.json", "r") as f:
    data_from_file = json.load(f)

print(data_from_file["user"]) # Output: admin
```

## Part 4: Running External Commands (`subprocess`)

The `subprocess` module is the modern, standard way to run external commands and manage their input and output. It replaces older, less secure functions like `os.system`.

### The Modern Way: `subprocess.run()`

The `subprocess.run()` function is the recommended entry point for most use cases. It waits for the command to complete and returns a `CompletedProcess` object containing information about the result.

| Argument              | Description                                                                                                                             |
| --------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `capture_output=True` | Captures the command's standard output and standard error streams so you can inspect them.                                              |
| `text=True`           | Decodes the captured output and error streams as text using the default encoding, which is more convenient than working with raw bytes. |
| `check=True`          | If the command returns a non-zero exit code (indicating an error), a `CalledProcessError` exception is raised automatically.            |

### Workflow: Capturing Command Output

This example shows how to run a command and safely handle both its successful output and potential errors.

```python
import subprocess

try:
    # The command and its arguments are passed as a list of strings for safety.
    result = subprocess.run(
        ["ls", "-l", "/non_existent_dir"],
        capture_output=True,
        text=True,
        check=True  # This will cause an exception if the command fails
    )
    print("--- STDOUT ---")
    print(result.stdout)

except FileNotFoundError:
    print("Error: The 'ls' command was not found on this system.")
except subprocess.CalledProcessError as e:
    print(f"Command failed with exit code {e.returncode}")
    print("--- STDERR ---")
    print(e.stderr)

```

### Workflow: Piping Commands

You can pipe the output of one command into the input of another, just like using the `|` operator in a shell.

```python
import subprocess

# Equivalent to running: ps aux | grep python
try:
    # Run the first command and capture its output
    ps_process = subprocess.run(["ps", "aux"], capture_output=True, text=True, check=True)
    
    # Use the stdout of the first command as the input for the second
    grep_process = subprocess.run(
        ["grep", "python"],
        input=ps_process.stdout,
        capture_output=True,
        text=True,
        check=True
    )

    print("Grep found the following python processes:")
    print(grep_process.stdout)
    
except subprocess.CalledProcessError as e:
    print(f"A command in the pipeline failed: {e.stderr}")
```

## Part 5: Dates and Times (`datetime`)

The `datetime` module supplies classes for manipulating dates and times, a fundamental task in programming. It provides tools for getting the current time, performing calculations, and formatting time information as text.

### Core Objects

| Class           | Description                                                                                   |
| --------------- | --------------------------------------------------------------------------------------------- |
| **`datetime`**  | An object containing full date and time information (year, month, day, hour, minute, second). |
| **`date`**      | An object representing just the date (year, month, day).                                      |
| **`time`**      | An object representing just the time of day.                                                  |
| **`timedelta`** | Represents a duration or the difference between two `date` or `datetime` objects.             |

### Workflow: Common Operations

This workflow shows how to create `datetime` objects and perform calculations with them.

```python
from datetime import datetime, timedelta

# 1. Get the current date and time
now = datetime.now()
print(f"Current time: {now}")

# 2. Create a specific date and time
release_date = datetime(2025, 10, 26, 12, 0, 0)
print(f"Release date: {release_date}")

# 3. Calculate the difference between two datetimes
time_until_release = release_date - now
print(f"Time until release: {time_until_release}")

# A timedelta object has useful attributes for easy access
print(f"That's {time_until_release.days} days and {time_until_release.seconds} seconds.")

# 4. Perform date arithmetic using timedelta
one_week_prior = release_date - timedelta(weeks=1)
print(f"One week prior to release: {one_week_prior}")
```

### Parsing and Formatting (`strptime` and `strftime`)

You often need to convert between `datetime` objects and strings.

- **`strptime`** (**str**ing **p**arse **t**ime): Parses a string into a `datetime` object. 
- **`strftime`** (**str**ing **f**ormat **t**ime): Formats a `datetime` object into a string.


```python
from datetime import datetime

# Formatting a datetime object into a clean string
now = datetime.now()
formatted_string = now.strftime("%Y-%m-%d %H:%M:%S")
print(f"Formatted as a string: {formatted_string}")

# Parsing a date string back into a datetime object
date_string = "2025-07-26 18:30:00"
parsed_date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
print(f"Parsed from a string: {parsed_date}")
```