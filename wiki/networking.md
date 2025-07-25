# Cheatsheet: Networking

This guide covers the essential commands for diagnosing connectivity, managing remote sessions, transferring files, and interacting with web services from the command line.

## Part 1: Connectivity & Interface Management

These commands are for checking the status of your network connections.

### `ping`

The `ping` command is the fundamental tool for checking if a remote host is reachable. It sends small data packets (ICMP ECHO_REQUEST) and waits for a reply.

#### Common Usage

```bash
# Ping a domain to check for internet connectivity and DNS resolution.
# Press Ctrl+C to stop.
ping google.com

# Ping a specific IP address on your local network.
ping 192.168.1.1

# Send only 4 packets and then stop automatically.
ping -c 4 google.com
```

#### `ping` Options

|Short|Long Flag|Description|
|---|---|---|
|**-c N**|`--count=N`|**(Count)** Stop after sending `N` packets. This is the most common option to prevent `ping` from running forever.|
|**-i N**|`--interval=N`|**(Interval)** Wait `N` seconds between sending each packet. The default is 1 second.|
|**-W N**|`--timeout=N`|**(Wait)** Time to wait for a response, in seconds. If a reply isn't received in this time, the packet is considered lost.|

### `ip`

The `ip` command is the modern, powerful tool for viewing and manipulating network interfaces, routing, and tunnels. It replaces the older, deprecated `ifconfig` command.

#### Common Usage

```bash
# Show information for all network interfaces (the most common use case).
ip addr show

# A common alias for the above command.
alias ipa='ip -c addr show' # -c adds color

# Show the system's routing table.
ip route show
```

#### `ip` Subcommands

The `ip` command is a suite of tools. You always use it with a subcommand.

|Subcommand|Description|
|---|---|
|`addr`|**(Address)** The most important subcommand. Manages the IP addresses on your network devices. `ip addr show` lists your IPs.|
|`route`|**(Route)** Manages the IP routing table. `ip route show` shows how your system will send traffic to different networks (e.g., your default gateway).|
|`link`|**(Link)** Manages the physical or logical network devices themselves. `ip link show` lists your interfaces (e.g., `eth0`, `wlan0`).|
|`neigh`|**(Neighbor)** Manages the ARP table, which maps IP addresses to MAC addresses on the local network.|

## Part 2: Remote Access & File Transfer

### `ssh` (Secure Shell)

`ssh` is the standard tool for securely logging into and executing commands on a remote computer.

#### Common Usage

```bash
# Connect to a remote server as a specific user.
ssh username@remote-server.com

# Connect to a server on a non-standard port (e.g., 2222 instead of 22).
ssh -p 2222 username@remote-server.com

# Generate a new SSH key pair for passwordless login.
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# Copy your public key to a remote server to enable passwordless login.
ssh-copy-id username@remote-server.com
```

#### `ssh` Options

|Short|Long Flag|Description|
|---|---|---|
|**-p N**|`--port=N`|Specifies the **p**ort to connect to on the remote host.|
|**-i [path]**|(N/A)|Specifies an **i**dentity file (private key) to use for authentication. Useful if you have multiple keys.|
|**-v**|`--verbose`|**V**erbose mode. Prints debugging messages about the connection progress. Use `-vv` or `-vvv` for even more detail.|
|**-L**|(N/A)|**L**ocal port forwarding. Forwards a port from your local machine to the remote server.|
|**-R**|(N/A)|**R**emote port forwarding. Forwards a port from the remote server to your local machine.|

### `scp` (Secure Copy)

`scp` copies files between hosts on a network, using SSH for the underlying data transfer.

#### Common Usage

The syntax is `scp [options] source destination`. The remote path is specified with the `user@host:` prefix.

```bash
# Copy a local file to a remote server.
scp ./local_file.txt username@remote-server.com:/remote/path/

# Copy a file from a remote server to your local machine.
scp username@remote-server.com:/remote/path/remote_file.txt ./

# Recursively copy an entire directory to a remote server.
scp -r ./local_directory username@remote-server.com:/remote/path/
```

#### `scp` Options

|Short|Long Flag|Description|
|---|---|---|
|**-r**|`--recursive`|**(Recursive)** Required to copy entire directories.|
|**-P N**|(N/A)|**(Port)** Specifies the remote host **p**ort. Note that this is a capital `P`, unlike `ssh`'s lowercase `p`.|
|**-v**|`--verbose`|**V**erbose mode. Prints debugging information.|
|**-C**|`--compress`|**C**ompression. Compresses the data as it's being transferred, which can speed up transfers over slow connections.|

## Part 3: Web & API Interaction

### `wget`

`wget` is a straightforward, non-interactive command-line utility for downloading files from the web.

#### Common Usage

```bash
# Download a file.
wget https://example.com/some_file.zip

# Download a file and save it with a different name.
wget -O new_name.zip https://example.com/some_file.zip

# Continue a partially downloaded file.
wget -c https://example.com/large_file.iso
```

#### `wget` Options

|Short|Long Flag|Description|
|---|---|---|
|**-O [file]**|`--output-document=[file]`|**(Output)** Specifies the **o**utput filename.|
|**-c**|`--continue`|**(Continue)** Resumes getting a partially-downloaded file.|
|**-r**|`--recursive`|**(Recursive)** Downloads a full website by following links.|
|**-q**|`--quiet`|**(Quiet)** Turns off `wget`'s output.|

### `curl`

`curl` is an extremely versatile tool for transferring data with URLs. While it can download files, its real power is in its ability to make complex HTTP requests for testing APIs.

#### Common Usage

```bash
# Download a file (similar to wget).
curl -O https://example.com/some_file.zip

# Display the contents of a URL directly in the terminal.
curl https://example.com

# Make a POST request with JSON data to an API endpoint.
curl -X POST -H "Content-Type: application/json" -d '{"key":"value"}' https://api.example.com/v1/users

# View only the HTTP response headers.
curl -I https://example.com
```

#### `curl` Options

|Short|Long Flag|Description|
|---|---|---|
|**-O**|`--remote-name`|**(Output)** Saves the output to a local file with the same name as the remote file.|
|**-o [file]**|`--output [file]`|Saves the output to a specific local `file`.|
|**-I**|`--head`|Fetches the HTTP **h**eaders only.|
|**-L**|`--location`|Follows HTTP redirects.|
|**-X [METHOD]**|`--request [METHOD]`|Specifies the HTTP request **m**ethod (e.g., `GET`, `POST`, `PUT`, `DELETE`).|
|**-H [header]**|`--header [header]`|Adds a custom HTTP **h**eader to the request (e.g., `-H "Authorization: Bearer <token>"`).|
|**-d [data]**|`--data [data]`|Sends the specified **d**ata in a POST request.|
