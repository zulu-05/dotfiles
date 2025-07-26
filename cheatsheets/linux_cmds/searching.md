# Cheatsheet: Finding Files & Text

This guide covers the essential tools for searching your filesystem. For each task, we'll cover the classic, universal command and a modern, faster alternative.
- **Finding Files**: `find` (classic) vs. `fd` (modern)
- **Searching Inside Files**: `grep` (classic) vs. `ripgrep` (`rg`) (modern)

## Part 1: Finding Files by Name or Attribute

### `find`: The Classic Tool

`find` is an incredibly powerful and flexible tool that is available on every Unix-like system. Its syntax can be complex, but it can search for files based on almost any attribute.

#### Common Usage

```bash
# Find all Python files in the current directory and subdirectories 
find . -name "*.py" 

# Find all directories named 'node_modules' (case-insensitive) 
find . -type d -iname "node_modules" 

# Find all files larger than 100MB in your home directory 
find ~ -type f -size +100M 

# Find all .tmp files and delete them 
find . -name "*.tmp" -exec rm {} \;
```

#### `find` Options (Expressions)

|Expression|Description|
|---|---|
|`-name "pattern"`|Find files by name. Use wildcards (`*`) in quotes. This is case-sensitive.|
|`-iname "pattern"`|Like `-name`, but **i**ncase-sensitive.|
|`-type [f/d/l]`|Find by type: **f**ile, **d**irectory, or symbolic **l**ink.|
|`-size [+N/-N/N]`|Find files by size. Use `+` for "greater than", `-` for "less than". Suffixes: `c` (bytes), `k` (KB), `M` (MB), `G` (GB).|
|`-mtime [+N/-N/N]`|Find files by **m**odification **time** in days. `+7` (more than 7 days ago), `-7` (within the last 7 days).|
|`-empty`|Find empty files and directories.|
|`-exec cmd {} \;`|**Exec**utes the command `cmd` on every file found. `{}` is replaced by the filename.|

### `fd`: The Modern Alternative

`fd` is a simple, fast, and user-friendly alternative to `find`. It is not installed by default, but is highly recommended.

**Key Advantages:**
- **Intuitive Syntax:** No need for complex expressions.
- **Very Fast:** Uses parallel directory traversal.
- **Smart by Default:** Ignores hidden files and directories (like `.git`) and respects your `.gitignore` rules automatically.
- **Colorized Output.**

#### Common Usage (Comparing with `find`)

|Task|`find` Command|`fd` Command (Simpler)|
|---|---|---|
|Find all `.md` files|`find . -name "*.md"`|`fd -e md`|
|Find a specific file|`find . -name "docker-compose.yml"`|`fd docker-compose.yml`|
|Find all `png` files (case-insensitive)|`find . -iname "*.png"`|`fd -e png` (default is case-insensitive)|
|Find all directories|`find . -type d`|`fd -t d`|
#### `fd` Options

|Short|Long Flag|Description|
|---|---|---|
|`-e`|`--extension`|Filter by file **e**xtension.|
|`-t`|`--type`|Filter by file **t**ype (`f` for file, `d` for directory, `l` for symlink).|
|`-s`|`--size`|Filter by file **s**ize (e.g., `+10M`, `-5k`).|
|`-x`|`--exec`|E**x**ecutes a command for each search result. e.g., `fd -e png -x chmod 644`.|
|`-H`|`--hidden`|Include **h**idden files and directories in the search.|
|`-I`|`--no-ignore`|**I**gnore `.gitignore` files and search all files.|
## Part 2: Searching for Text Inside Files

### `grep`: The Classic Tool

`grep` is the standard Unix utility for searching plain-text data sets for lines that match a regular expression.

#### Common Usage

```bash
# Find all occurrences of 'service_register' in a file 
grep "service_register" ./40-functions.sh 

# Find 'error' (case-insensitive) in all log files 
grep -i "error" /var/log/*.log 

# Recursively find all files containing 'GITHUB_TOKEN' in the current project 
grep -r "GITHUB_TOKEN" . 

# List only the names of files that contain a match 
grep -l "import" ./**/*.py
```

#### `grep` Options

|Short|Long Flag|Description|
|---|---|---|
|`-i`|`--ignore-case`|Makes the search case-**i**nsensitive.|
|`-r`|`--recursive`|**R**ecursively searches all files in a directory.|
|`-v`|`--invert-match`|In**v**erts the match, showing lines that _do not_ contain the pattern.|
|`-l`|`--files-with-matches`|Only lists the names of **f**i**l**es that contain a match.|
|`-n`|`--line-number`|Shows the line **n**umber for each match.|
|`-C N`|`--context=N`|Shows `N` lines of **c**ontext around each match.|
### `ripgrep` (`rg`): The Modern Alternative

`ripgrep` (`rg`) is a line-oriented search tool that recursively searches your current directory for a regex pattern. It is a replacement for `grep` that is focused on speed and usability.

**Key Advantages:**
- **Extremely Fast:** Generally the fastest text search tool available.
- **Recursive by Default:** You don't need the `-r` flag.
- **Git-Aware by Default:** Automatically respects your `.gitignore` and doesn't search hidden files/directories.
- **Beautiful Output:** Colorized, includes line numbers, and is easy to read.

#### Common Usage (Comparing with `grep`)

|Task|`grep` Command|`rg` Command (Simpler & Faster)|
|---|---|---|
|Recursively find `my_function`|`grep -r "my_function" .`|`rg "my_function"`|
|Find `TODO` (case-insensitive)|`grep -ri "TODO" .`|`rg -i "TODO"`|
|List files containing `important`|`grep -rl "important" .`|`rg -l "important"`|
|Find text only in Python files|`grep -r "class" --include "*.py"`|`rg "class" -t py`|
#### `rg` Options

|Short|Long Flag|Description|
|---|---|---|
|`-i`|`--ignore-case`|Makes the search case-**i**nsensitive.|
|`-v`|`--invert-match`|In**v**erts the match, showing lines that _do not_ contain the pattern.|
|`-l`|`--files-with-matches`|Only lists the names of **f**i**l**es that contain a match.|
|`-t`|`--type`|Search only in files of a specific **t**ype (e.g., `py`, `md`, `html`).|
|`-U`|`--unrestricted`|**U**nrestricted search. Ignores `.gitignore` files and searches hidden files. Use up to 3 times (`-UUU`) to search binaries.|
|`-w`|`--word-regexp`|Only show matches that form a whole **w**ord. `rg -w "cat"` won't match "caterpillar".|
