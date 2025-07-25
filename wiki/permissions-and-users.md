# Cheatsheet: Permissions & Users

This guide covers the fundamental concepts of file permissions, user identity, and administrative privileges in Linux.

## Part 1: File Permissions & Ownership

### Understanding the Permission String

When you run `ls -l`, you see a 10-character string like `drwxr-xr-x`. This string is broken into four parts: `[type] [user] [group] [other]`.

`d | rwx | r-x | r-x`
1. **File Type** (1st character):
   - `d`: **D**irectory
   - `-`: Regular file
   - `l`: Symbolic **l**ink
2. **Permission Triplets** (3 sets of 3 characters):
   - **User/Owner**: Permissions for the user who owns the file.
   - **Group**: Permissions for members of the file's group.
   - **Other**: Permissions for everyone else.
3. **The Permissions (r, w, x):**
   - The meaning depends on the file type.

|Permission|Meaning for a **File**|Meaning for a **Directory**|
|---|---|---|
|**`r` (Read)**|You can open and view the contents of the file.|You can list the contents of the directory (i.e., run `ls`).|
|**`w` (Write)**|You can modify and save changes to the file.|You can create, delete, and rename files _inside_ the directory.|
|**`x` (Execute)**|You can run the file as a program or script.|You can enter (`cd`) into the directory.|

### `chmod` (Change Mode)

The `chmod` command changes the permissions of a file or directory.

#### Symbolic Mode (Easier to read)

Uses letters to represent who (`u, g, o, a`), what action (`+, -, =`), and which permission (`r, w, x`).
##### Examples:

```bash
# Make a script executable for the user (owner) 
chmod u+x my_script.sh 

# Add write permission for the group 
chmod g+w shared_file.txt 

# Remove all permissions for 'other' 
chmod o-rwx config.conf 

# Add read permission for everyone 
chmod a+r public_document.txt
```

#### Octal Mode (Faster to type)

Uses numbers to represent the full permission set (`r`=4, `w`=2, `x`=1).

##### Common Octal Values:

- `600` (`rw-------`): Standard for private files (e.g., SSH keys).
- `644` (`rw-r--r--`): Standard for publicly readable files.
- `700` (`rwx------`): Standard for private directories.
- `755` (`rwxr-xr-x`): Standard for executables and public directories.

###### Examples:

```bash
# Set a config file to be read/write by owner only 
chmod 600 sensitive.conf

# Set a script to be executable by everyone 
chmod 755 my_script.sh
```

### `chown` (Change Owner)

The `chown` command changes the user and/or group ownership of a file. You often need `sudo` to run it.

**Syntax:** `chown [user]:[group] [file]`

#### Examples:

```bash
# Make 'www-data' the owner of a file 
sudo chown www-data access.log 

# Make 'user' the owner and 'developers' the group 
sudo chown user:developers app.py 

# Recursively change ownership of an entire directory (-R) 
sudo chown -R user:group /opt/my_app
```

## Part 2: User & Identity Management

These commands help you identify and manage your user account.

### `whoami` (Who am I?)

The simplest command. It prints the username of the currently logged-in user.

```bash
whoami 
# Output: myuser
```

### `passwd` (Password)

The command to change user passwords.

```bash
# Change your own password. The system will prompt you for your old 
# password, then ask you to enter the new one twice. 
passwd 

# As root, you can change any user's password. 
sudo passwd otheruser
```

## Part 3: Privilege Management

### `sudo` (Substitute User Do)

`sudo` is one of the most important commands in Linux. It allows a permitted user to execute a command as another user, most commonly the **superuser** or **root**. It is the standard way to perform administrative tasks without logging in as the root user directly.

#### Common Usage

You simply prefix any command that requires administrative privileges with `sudo`.

```bash
# Update the system's package lists (requires root) 
sudo apt update 

# Install a new package 
sudo apt install nginx 

# View a log file that is normally restricted 
sudo less /var/log/secure 

# Restart a system service 
sudo systemctl restart sshd
```

#### Important `sudo` Variations

| Command                | Description                                                                                                                                                               |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `sudo -i`              | Simulates a full, interactive login as the `root` user. You get a `root` shell (`#` prompt) and the `root` user's environment. Use `exit` to return to your normal shell. |
| `sudo -u <user> [cmd]` | Runs a command as a different user (not necessarily root). For example, `sudo -u www-data ls /var/www`.                                                                   |
| `sudo !!`              | **(Shell Expansion)** A very useful shortcut that re-runs the _previous_ command, but with `sudo` in front of it. Perfect for when you forget to add it the first time.   |
The configuration for who can run `sudo` commands is managed in the `/etc/sudoers` file, which should only ever be edited with the `visudo` command.