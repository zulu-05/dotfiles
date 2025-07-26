# Cheatsheet: Filesystem Interaction

This guide covers the essential commands for navigating, listing, and inspecting the Linux filesystem.

## Part 1: Inspecting Directories & Disk Space
### `ls` (List Directory Contents) 

The `ls` command is the primary tool for listing files and directories.

#### Common Usage

`ls` is almost always used via shorter, more powerful aliases.

```bash
# The most common alias: a long, detailed, human-readable list of all files. 
alias ll='ls -alFh' 

# A quick, multi-column list of visible files. 
alias l='ls -CF' 

# A detailed list sorted by most recently modified time. 
ls -lt 

# A detailed list sorted by largest file size. 
ls -lS
```

#### `ls` options

##### 1. Display Format

These options change _how_ the list of files is presented.

| Short  | Long Flag                | Description                                                                                                                                              |
| ------ | ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **-l** | `--format=long`          | **(Long Listing)** The most important option. Displays files in a detailed, multi-column list including permissions, owner, size, and modification date. |
| **-1** | `--format=single-column` | Forces output into a single column, with one file per line. Useful for piping the output to other commands.                                              |
| **-C** | `--format=vertical`      | The default behavior. Displays files in multiple columns, sorted vertically.                                                                             |
##### 2. File Filtering

These options control which files are shown.

|Short|Long Flag|Description|
|---|---|---|
|**-a**|`--all`|**(All)** Shows all files, including hidden dotfiles (e.g., `.git`) and the special `.` and `..` directories.|
|**-A**|`--almost-all`|**(Almost All)** A more practical version of `-a`. Shows dotfiles but omits the `.` and `..` entries, which usually just add noise.|
|**-d**|`--directory`|Lists directories themselves, not their contents. `ls -ld my_dir` shows info for `my_dir` itself.|
|**-R**|`--recursive`|**(Recursive)** Lists the contents of all subdirectories. The `tree` command is a better alternative for this.|
##### 3. Output Sorting 

These options change the default alphabetical sort order.

|Short|Long Flag|Description|
|---|---|---|
|**-t**|`--sort=time`|**(Time)** Sorts by modification time, with the newest files listed first. Incredibly useful for seeing what you've worked on recently.|
|**-S**|`--sort=size`|**(Size)** Sorts by file size, with the largest files listed first. Great for finding what's taking up space.|
|**-r**|`--reverse`|**(Reverse)** Reverses any sorting order. `ls -tr` will show the _oldest_ files first.|
|**-X**|`--sort=extension`|Sorts alphabetically by file extension, grouping all `.py` files, `.txt` files, etc., together.|
##### 4. Information Formatting

These options change the details within the listing, especially when used with `-l`.

|Short|Long Flag|Description|
|---|---|---|
|**-h**|`--human-readable`|**(Human-Readable)** When used with `-l`, displays file sizes in a friendly format (e.g., `4.0K`, `1.2M`) instead of raw bytes. This is almost always desired.|
|**-i**|`--inode`|Displays the inode number for each file, useful for low-level filesystem diagnostics.|
##### 5. Visuals and Classification

These options add visual cues to the output.

| Short                         | Long Flag    | Description                                                                                                                                                       |
| ----------------------------- | ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **--color**=`[when]`          | (N/A)        | Controls when to use color. `when` can be `always`, `never`, or `auto` (the default).                                                                             |
| **-F**                        | `--classify` | **(Classify)** Appends a character to filenames to indicate their type: `/` for a directory, `*` for an executable, `@` for a symbolic link, and `\|` for a FIFO. |
| **--group-directories-first** | (N/A)        | A useful extension that lists all directories first, followed by all other files.                                                                                 |
### `tree`

The `tree` command provides a more visual, recursive listing of files in a classic indented tree-like format. It is often a better choice than `ls -R`.

#### Common Usage

```bash
# Display the current directory, 2 levels deep 
tree -L 2 

# Display directories only 
tree -d 

# Display all files, including hidden ones, with full paths 
tree -af
```

#### `tree` Options

|Short|Long Flag|Description|
|---|---|---|
|**-L N**|`--level=N`|Descends only **N** **l**evels deep from the root of the tree. `tree -L 2` is very common for a quick project overview.|
|**-d**|(N/A)|Lists **d**irectories only.|
|**-f**|(N/A)|Prints the **f**ull path prefix for each file.|
|**-C**|(N/A)|Turns on **c**olorization, using the `LS_COLORS` environment variable.|
|**-a**|(N/A)|Shows **a**ll files, including hidden dotfiles.|

### `du` (Disk Usage)

The `du` command is used to estimate and summarize file and directory space usage.

#### Common Usage

```bash
# Show a human-readable summary of the current directory's total size. 
du -sh . 

# Show the human-readable size of every file and directory in the current level. 
du -sh * 

# Find the largest subdirectories (a very common and useful pattern). 
du -h --max-depth=1 | sort -rh
```

#### `du` Options

##### 1. Formatting the Output

|Short|Long Flag|Description|
|---|---|---|
|**-h**|`--human-readable`|**(Human-Readable)** Prints sizes in powers of 1024 (e.g., `1K`, `234M`, `2G`). This is the most useful option.|
|**-k**|`--kilobytes`|Displays sizes in 1024-byte blocks (kilobytes).|
|**-m**|`--megabytes`|Displays sizes in 1024*1024-byte blocks (megabytes).|
##### 2. Controlling Summarisation

| Short  | Long Flag       | Description                                                                                                                                          |
| ------ | --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| **-s** | `--summarize`   | Displays only a total for each argument. For example, `du -s .` shows only the grand total for the current directory.                                |
| **-c** | `--total`       | Produces a grand **t**otal line at the very end of the output.                                                                                       |
| **-d** | `--max-depth=N` | Prints the total for a directory (or file, with `-a`) only if it is N or fewer levels below the starting point. `--max-depth=0` is the same as `-s`. |
| **-a** | `--all`         | Writes counts for all **f**iles, not just directories.                                                                                               |

### `df` (Disk Free)

Reports the amount of available disk space on the entire filesystem.

#### Common Usage:

```bash
# See how much space is free on all your mounted drives in a human-readable format. 
df -h 

# Include the filesystem type in the report (e.g., ext4, nfs). 
df -hT 

# Check available inodes instead of blocks. 
df -i
```

#### `df` Options

| Short  | Long Flag          | Description                                                                                                                              |
| ------ | ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------- |
| **-h** | `--human-readable` | **(Human-Readable)** Prints sizes in a friendly format. This is the most common way to use `df`.                                         |
| **-T** | `--print-type`     | Includes the filesystem **t**ype (e.g., `ext4`, `nfs`) in the output.                                                                    |
| **-i** | `--inodes`         | Reports on **i**node usage instead of block usage. Useful for diagnosing "no space left on device" errors when space appears to be free. |
| -a     | `--all             | Includes pseudo, duplicate, and inaccessible file systems in the output.                                                                 |

## Part 2: Navigating the Filesystem

### `cd` (Change Directory)

The `cd` command is the most fundamental tool for moving through the filesystem.

#### Common Usage

```bash
# Go up one level 
cd .. 

# Go up two levels 
cd ../.. 

# Go to your home directory 
cd ~ 

# Go back to the last directory you were in 
cd -
```

#### `cd` Special Directories

While `cd` doesn't have many options, it understands several special directory shortcuts.

|Path|Description|
|---|---|
|`.`|The current directory.|
|`..`|The parent directory (the directory one level above the current one).|
|`~`|The current user's home directory (e.g., `/home/user`).|
|`-`|The previous working directory. This is stored in the `$OLDPWD` environment variable.|
### Other Navigation Commands

#### `pwd` (Print Working Directory)

Displays the full, absolute path of the directory you are currently in. It takes no common options.

```bash
pwd
# Output: /home/user/dotfiles/wiki
```

#### Directory Stack (`pushd`, `popd`, `dirs`)

This is a powerful system for bookmarking directories, acting like a browser's history tab.

- **`pushd <dir>`**: "Pushes" your current location onto a memory list (the "stack") and then `cd`s to `<dir>`.
- **`popd`**: "Pops" the most recent directory off the stack and `cd`s you back to it.
- **`dirs -v`**: **Essential companion**. Displays the current stack as a numbered list so you know where you are and where `popd` will go.

##### Workflow Example:

```bash
# You are in ~/dotfiles. Let's bookmark it and go to /var/log 
pushd /var/log 

# Check the stack. Note that /var/log is at the top (index 0). 
dirs -v 
# Output: 
# 0 /var/log 
# 1 ~/dotfiles 

# Now, go back to the start. 
popd
```

## Part 3: Manipulating Files & Directories

These commands create, modify, and delete files and directories.

### `mkdir` (Make Directory)

Creates new directories.

#### Common Usage

```bash
# Create a single directory 
mkdir my_new_folder 

# Create a nested directory structure all at once 
mkdir -p project/src/components
```

#### `mkdir` Options

|Short|Long Flag|Description|
|---|---|---|
|**-p**|`--parents`|**(Parents)** Creates parent directories as needed. `mkdir -p a/b/c` will create `a` and `a/b` if they don't exist. This is extremely useful.|
|**-v**|`--verbose`|Prints a message for each created directory.|
### `touch`

Creates an empty file if it doesn't exist. If it _does_ exist, `touch` updates the file's modification and access timestamps to the current time.

#### Common Usage

```
# Create a new, empty file 
touch new_file.txt 

# Create multiple files at once 
touch file1.html file2.css 

# Update the 'last modified' date of an existing file 
touch existing_file.py
```

### `cp` (Copy)

Copies files or directories.

#### Common Usage

```bash
# Copy a file in the current directory 
cp source.txt destination.txt 

# Copy a file into another directory 
cp source.txt ./my_folder/ 

# Recursively copy a directory (including all its contents) 
cp -r src/ build/
```

#### `cp` Options

| Short  | Long Flag       | Description                                                                                                                                                                    |
| ------ | --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **-r** | `--recursive`   | **(Recursive)** Required to copy a directory and its contents.                                                                                                                 |
| **-i** | `--interactive` | **(Interactive)** Prompts for confirmation before overwriting an existing file. A common safety alias is `alias cp='cp -i'`.                                                   |
| **-v** | `--verbose`     | Explains what is being done.                                                                                                                                                   |
| **-a** | `--archive`     | **(Archive)** A powerful combination of flags (`-dR --preserve=all`) that recursively copies files while preserving permissions, ownership, and timestamps. Ideal for backups. |
### `mv` (Move / Rename)

Moves a file to a different directory, or renames a file if the destination is in the same directory.

#### Common Usage

```bash
# Rename a file 
mv old_name.txt new_name.txt 

# Move a file into a different directory 
mv new_name.txt ./my_folder/ 

# Move a file and rename it at the same time 
mv important.log ./archive/important_2025-07-25.log
```

#### `mv` Options

|Short|Long Flag|Description|
|---|---|---|
|**-i**|`--interactive`|**(Interactive)** Prompts for confirmation before overwriting an existing file. A common safety alias is `alias mv='mv -i'`.|
|**-n**|`--no-clobber`|**(No Clobber)** Never overwrites an existing file. The opposite of `-f`.|
|**-v**|`--verbose`|Explains what is being done.|
#### Examples:

```bash
# Rename a file 
mv old_name.txt new_name.txt 

# Move a file into a different directory 
mv new_name.txt ./my
```