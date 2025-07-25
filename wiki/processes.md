# Cheatsheet: Managing System Processes

This guide covers the essential commands for viewing, finding, and terminating running processes on a Linux system.

## Part 1: Viewing Processes (Static Snapshot)

These commands give you a snapshot of the processes running at a single moment in time.

### `ps` (Process Status)

`ps` is the standard tool for viewing running processes. It's most powerful when combined with options.

#### Common Usage

The two most common invocations are `ps aux` and `ps -ef`. They show similar information in slightly different formats.

```bash
# Show all processes for all users in a user-oriented format (most common on Linux). 
ps aux 

# Often piped to grep to find a specific process. 
ps aux | grep "sshd"
```

#### Understanding `ps aux` Output

A line of `ps aux` output looks like this:
`USER  PID  %CPU  %MEM    VSZ   RSS  TTY  STAT  START  TIME  COMMAND` 
`root    1   0.0   0.1 169404 13620  ?    Ss    Jul24  0:02  /sbin/init` 

|Column|Description|
|---|---|
|`USER`|The user who owns the process.|
|`PID`|**Process ID**. The unique number identifying the process. This is what you use with `kill`.|
|`%CPU`|CPU usage percentage.|
|`%MEM`|Memory (RAM) usage percentage.|
|`VSZ`|Virtual memory size of the process in kilobytes.|
|`RSS`|Resident Set Size: the non-swapped physical memory a task has used.|
|`TTY`|The controlling terminal. `?` means it's not attached to a terminal (a system daemon).|
|`STAT`|Process state code (e.g., `S` for sleeping, `R` for running, `Z` for zombie).|
|`START`|The time the process was started.|
|`TIME`|The total CPU time the process has used.|
|`COMMAND`|The command that started the process.|
### `prgrep` (Process Grep)

`pgrep` is a much more direct way to find the PID of a running program without needing `ps | grep`.

#### `pgrep` Options

| Short | Long Flag     | Description                                                       |
| ----- | ------------- | ----------------------------------------------------------------- |
| `-l`  | `--list-name` | Lists the process name along with the PID.                        |
| `-f`  | `--full`      | Matches against the full command line, not just the process name. |
| `-u`  | `--user`      | Find processes owned by a specific user.                          |
| `-a`  | `--list-full` | Lists the PID and the full command line argument list.            |
#### Common Usage

```bash
# Find the PID of the sshd process 
pgrep sshd 

# Find the PID and name of the cron process 
pgrep -l cron 

# Find all processes run by the 'www-data' user 
pgrep -u www-data
```

## Part 2: Viewing Processes (Interactive)

These tools provide a real-time, interactive dashboard of your system's processes.

### `top`: The Classic Dashboard

`top` provides a dynamic real-time view of a running system.

#### Key Interactive Commands (while `top` is running):

- `h`: Show the **h**elp screen.
- `u`: Filter by **u**ser. It will prompt you for a username.
- `P`: Sort processes by **CPU** usage (the default).
- `M`: Sort processes by **M**emory usage.
- `k`: **K**ill a process. It will prompt you for the PID and the signal to send.
- `q`: **Q**uit `top`.

### `htop`: The Modern Alternative

`htop` is an interactive process viewer and a significant improvement over `top`. It is highly recommended.

#### Key Advantages:

- Full color and better visual layout.
- You can scroll vertically and horizontally.
- Killing, renicing, and other actions are done with simple function key presses (e.g., F9 for Kill).
- Easier to sort by clicking on column headers (if your terminal supports it).

#### Key Interactive Commands (while `htop` is running):

- `F2`: Enter the setup screen to customise columns.
- `F3`: Search for a process.
- `F4`: Filter the process list by name.
- `F6`: Bring up the sort-by menu.
- `F9`: Bring up the kill menu for the selected process.
- `q` or `F10`: **Q**uit `htop`.

## Part 3: Terminating Processes

### `kill`: The Standard Tool

The `kill` command sends a signal to a process, usually to terminate it. You must provide the PID.

#### Understanding Signals

A "signal" is a software interrupt delivered to a process. `kill` can send many signals, but two are used 99% of the time.

|Signal Name|Number|Description|
|---|---|---|
|`SIGTERM`|15|**(The Default / The Polite Request)** Asks the process to shut down gracefully, save its work, and exit. **Always try this first.**|
|`SIGKILL`|9|**(The Hammer / The Last Resort)** This is a non-ignorable, immediate termination. The process is killed by the kernel instantly, without a chance to clean up. Use this when a process is frozen.|
#### Common Usage

```bash
# 1. First, find the PID of the process you want to stop 
pgrep -l "my_frozen_app" 
# Output: 12345 my_frozen_app 

# 2. Politely ask the process to stop (sends SIGTERM by default) 
kill 12345 

# 3. If it doesn't stop after a few seconds, use the hammer (sends SIGKILL) 
kill -9 12345 
# or 
kill -KILL 12345
```
**Warning:** Never use `kill -9` on a database or other service that needs to shut down cleanly, as it can lead to data corruption.

### `pkill` & `killall`: The Convenient Alternatives

These commands let you kill processes by name instead of PID. Use them with caution.
- **`pkill <name>`**: Kills all processes whose name matches `<name>`. It's like running `kill $(pgrep <name>)`.
- **`killall <name>`**: Similar to `pkill`, but can be more strict about matching the exact process name.

```bash
# Politely terminate all running 'slack' processes 
pkill slack 

# Forcefully terminate all 'chrome' processes 
killall -9 chrome
```

## Part 4: System Status & Service Management

These commands provide information about the machine itself and the background services it runs.

### `free` (Memory Usage)

The `free` command displays the total amount of free and used physical and swap memory in the system.

|Short|Long Flag|Description|
|---|---|---|
|**-h**|`--human`|**(Human-Readable)** Show all output fields automatically scaled to the shortest three-digit unit (e.g., `1K`, `234M`, `2G`). This is the most useful option.|
|**-m**|`--mega`|Display the amount of memory in megabytes.|
|**-g**|`--giga`|Display the amount of memory in gigabytes.|

#### Example: 

```bash
free -h 
#          total     used     free    shared    buff/cache    available 
# Mem:      15Gi    4.3Gi    8.4Gi     234Mi         2.8Gi         10Gi 
# Swap:    2.0Gi       0B    2.0Gi
```

### `uname` (Unix Name)

The `uname` command prints basic information about the system name and operating system kernel.

|Short|Long Flag|Description|
|---|---|---|
|**-a**|`--all`|**(All)** Print all available system information in a specific order. This is the most common way to use the command.|
|**-s**|`--kernel-name`|Print the kernel name (e.g., `Linux`).|
|**-r**|`--kernel-release`|Print the kernel release (e.g., `5.15.0-78-generic`).|
|**-m**|`--machine`|Print the machine hardware name (e.g., `x86_64`).|
#### Example:

```bash
uname -a 
# Output: Linux my-desktop 5.15.0-78-generic #85-Ubuntu SMP ... x86_64 x86_64 x86_64 GNU/Linux
```

### `systemctl` (System Control)

`systemctl` is the primary tool for managing `systemd`, the system and service manager on modern Linux distributions. It is used to control background services (daemons). **Nearly all `systemctl` commands require `sudo`.**

#### Core Actions

The syntax is `sudo systemctl [action] [service_name]`.

|Action|Description|
|---|---|
|`status`|Shows the detailed runtime **status** of a service, including whether it's active, its main PID, and recent log entries.|
|`start`|**Starts** a service.|
|`stop`|**Stops** a service.|
|`restart`|**Restarts** a service. This is a convenient shortcut for a `stop` followed by a `start`.|
|`reload`|Asks a service to **reload** its configuration without a full restart. This is faster and causes less downtime (if the service supports it).|
|`enable`|**Enables** a service to start automatically at boot time.|
|`disable`|**Disables** a service from starting automatically at boot time.|
#### Examples:

```bash
# Check the status of the Nginx web server 
sudo systemctl status nginx 

# Stop the sshd service 
sudo systemctl stop sshd 

# Start the sshd service and enable it to start on boot 
sudo systemctl start sshd 
sudo systemctl enable sshd 

# Restart the networking service after a config change 
sudo systemctl restart networking
```

