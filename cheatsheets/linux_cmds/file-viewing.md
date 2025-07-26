# Cheatsheet: Viewing File Contents

This guide covers the essential commands for viewing the contents of files directly in the terminal without opening a full text editor.

## `cat` (Concatenate)

The `cat` command reads data from files and outputs their contents to standard output. Its simplest and most common use is to display the _entire_ content of a file on the screen.

**Best for:** Short files where you want to see everything at once.

#### Common Usage

```bash
# Display the contents of a single file 
cat .bashrc 

# Display the contents of multiple files, one after the other 
cat header.txt content.txt footer.txt 

# Concatenate multiple files into a new file 
cat file1.txt file2.txt > combined_file.txt 

# Display a file with line numbers 
cat -n script.sh
```

#### `cat` Options

|Short|Long Flag|Description|
|---|---|---|
|**-n**|`--number`|**(Number)** Numbers all output lines, starting from 1.|
|**-b**|`--number-nonblank`|Numbers only the non-blank lines.|
|**-s**|`--squeeze-blank`|**(Squeeze)** Suppresses repeated empty output lines. If a file has multiple consecutive blank lines, `cat -s` will output only one.|
|**-E**|`--show-ends`|Displays a `$` character at the end of each line. Useful for seeing trailing whitespace.|
### `less` (Pager)

The `less` command is a "pager," a program that lets you view the contents of a file one screen at a time. It is the standard tool for viewing large files. Unlike `cat`, it loads the file instantly without reading the entire file into memory.

**Best for:** Long files like source code, log files, or any text you need to read and search through.

#### Common Usage

```bash
# Open a large file for viewing 
less /var/log/syslog 

# Pipe the output of another command into less for easy viewing 
ps aux | less
```

#### Interactive Commands (Inside `less`)

The real power of `less` is in its interactive commands you can use while viewing a file.

| Key(s)           | Action                                                                                                     |
| ---------------- | ---------------------------------------------------------------------------------------------------------- |
| `q`              | **Q**uit the viewer.                                                                                       |
| `Spacebar` / `f` | Move **f**orward one full screen.                                                                          |
| `b`              | Move **b**ackward one full screen.                                                                         |
| `j` / `↓`        | Move forward one line.                                                                                     |
| `k` / `↑`        | Move backward one line.                                                                                    |
| `g`              | **G**o to the beginning of the file.                                                                       |
| `G`              | **G**o to the end of the file.                                                                             |
| `/pattern`       | **Search forward** for `pattern`. Press `n` to go to the **n**ext match, `N` to go to the previous.        |
| `?pattern`       | **Search backward** for `pattern`.                                                                         |
| `&pattern`       | **Filter:** Shows only the lines that contain `pattern`. Type `&` again with no pattern to show all lines. |

#### `less` Options (Used on Startup)

|Short|Long Flag|Description|
|---|---|---|
|**-N**|`--LINE-NUMBERS`|Displays a line **n**umber at the beginning of each line.|
|**-S**|`--chop-long-lines`|**(Squeeze)** Disables line wrapping. Long lines can be viewed by scrolling horizontally with the left/right arrow keys. Essential for log files.|
|**-i**|`--ignore-case`|Makes searches **i**nsensitive to case, unless the search pattern contains uppercase letters.|
|**-F**|`--quit-if-one-screen`|Automatically exits if the entire file can be displayed on a single screen.|
|**+F**|(N/A)|Starts `less` in "follow" mode, similar to `tail -f`. Press `Ctrl+C` to stop following and start navigating normally.|

### `head`

The `head` command outputs the first part of files.

**Best for:** Quickly checking the beginning of a file to see its headers, column names, or initial content.

#### Common Usage

```bash
# Show the first 10 lines of a file (the default) 
head /var/log/nginx/access.log 

# Show the first 20 lines of a file 
head -n 20 script.py 

# Show the first 100 bytes of a file 
head -c 100 binary_file
```

#### `head` Options

|Short|Long Flag|Description|
|---|---|---|
|**-n N**|`--lines=N`|Prints the first `N` **n**umber of lines instead of the default 10. You can also just use `-N` (e.g., `head -20`).|
|**-c N**|`--bytes=N`|Prints the first `N` **c**haracters (bytes) of the file.|
|**-q**|`--quiet`, `--silent`|Never prints headers giving file names when viewing multiple files.|

### `tail`

The `tail` command outputs the last part of files.

**Best for:** Viewing the most recent entries in log files, especially for monitoring them in real-time.

#### Common Usage

```bash
# Show the last 10 lines of a file (the default) 
tail /var/log/syslog 

# Show the last 50 lines of a file 
tail -n 50 error.log 

# THE KILLER FEATURE: Follow a file in real-time 
# This will display new lines as they are added to the file. 
# Press Ctrl+C to stop. 
tail -f /var/log/nginx/access.log
```

#### `tail` Options

|Short|Long Flag|Description|
|---|---|---|
|**-n N**|`--lines=N`|Prints the last `N` **n**umber of lines instead of the default 10. You can also just use `-N` (e.g., `tail -50`).|
|**-c N**|`--bytes=N`|Prints the last `N` **c**haracters (bytes) of the file.|
|**-f**|`--follow`|**(Follow)** The most useful option. Outputs appended data as the file grows. Ideal for monitoring log files.
