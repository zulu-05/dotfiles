# Cheatsheet: `apt` (Advanced Package Tool)

This guide covers the essential commands for managing software packages on Debian-based Linux systems like Ubuntu using the `apt` command-line tool.

**Note:** Nearly all `apt` commands that modify the system (install, remove, update) require administrative privileges and must be prefixed with `sudo`.

## Part 1: Updating & Upgrading Packages

This is the most common package management task. It's a two-step process: first, you update your local list of available packages, and then you upgrade the packages themselves.

### Common Usage

```bash
# The standard weekly/daily maintenance command.
# First, resynchronize the package index files from their sources.
sudo apt update

# Then, install the newest versions of all packages currently installed.
sudo apt upgrade
```

### Update & Upgrade Commands

|Command|Description|
|---|---|
|`apt update`|**(Update Cache)** This command downloads package information from all configured sources. It does _not_ install or upgrade any packages; it just updates the local cache of what's available. **You should always run this before `upgrade` or `install`.**|
|`apt upgrade`|**(Upgrade Packages)** This command upgrades all of the installed packages to their newest versions, based on the information from `apt update`. It will _not_ remove any packages.|
|`apt full-upgrade`|**(Full Upgrade)** Similar to `upgrade`, but it is "smarter" and will remove currently installed packages if that is needed to upgrade the system as a whole. This is often used during a major distribution version upgrade.|

## Part 2: Searching for Packages

These commands help you find new software and get information about it before you install.

### Common Usage

```bash
# Search for a command-line image viewer.
apt search image viewer

# Get detailed information about the 'neofetch' package.
apt show neofetch
```

### Search Commands

|Command|Description|
|---|---|
|`apt search [query]`|Searches the package names and descriptions for the given query. This is the primary tool for discovering new software.|
|`apt show [package]`|Shows detailed information about a specific package, including its version, size, dependencies, and a full description of what it does.|

## Part 3: Installing & Removing Packages

These commands are for adding new software to your system or removing software you no longer need.

### Common Usage

```bash
# Install the 'htop' utility.
sudo apt install htop

# Install multiple packages at once.
sudo apt install curl wget git

# Remove the 'htop' utility.
sudo apt remove htop

# Remove 'htop' AND its system-wide configuration files.
sudo apt purge htop
```

### Installation & Removal Commands

|Command|Description|
|---|---|
|`apt install [package]`|Installs a new package and all of its required dependencies. You can list multiple packages to install them all at once.|
|`apt remove [package]`|**Removes** a package from the system but **leaves its configuration files behind**. This is useful if you plan to reinstall it later and want to keep your settings.|
|`apt purge [package]`|**Purges** a package. This removes the package _and_ all of its system-wide configuration files. This is a complete removal.|

> **Tip:** You can add the `-y` or `--yes` flag to `install`, `remove`, and `upgrade` commands to automatically answer "yes" to any prompts, making them non-interactive. For example: `sudo apt -y install htop`.

## Part 4: System Cleanup

These commands help you free up disk space by removing unnecessary packages and files.

### Common Usage

```bash
# A common command to run after removing packages to clean up dependencies.
sudo apt autoremove

# A good command to run periodically to free up disk space.
sudo apt clean
```

### Cleanup Commands

|Command|Description|
|---|---|
|`apt autoremove`|Removes packages that were automatically installed to satisfy dependencies for other packages and are now no longer needed. It's good practice to run this after you remove a package.|
|`apt clean`|Clears out the local repository of retrieved package files (`.deb` files). It removes everything from `/var/cache/apt/archives/`. This can free up a significant amount of disk space.|