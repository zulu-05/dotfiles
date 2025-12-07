# Docker: Containers & Runtime

This guide focuses on the "instances"-running applications, debugging crashes, and setting up development environments.

## 1. Command Reference

### Lifecycle Management

| Command | Action | Description |
| :--- | :--- | :--- |
| `docker run <image>` | **Start** | Creates and starts a new container from an image. |
| `docker ps` | **List** | Shows currently running containers. |
| `docker ps -a` | **List All** | Shows running AND stopped containers. **Crucial for debugging crashes.** |
| `docker stop <name>` | **Stop** | Gracefully shuts down the process (sends `SIGTERM`). |
| `docker kill <name>` | **Kill** | Immediately stops the process (sends `SIGKILL`). |
| `docker rm <name>` | **Delete** | Removes a stopped container from the system. |
| `docker logs <name>` | **Output** | Shows the container's stdout/stderr history. Add `-f` to follow live. |
| `docker exec -it <name> <cmd>` | **Enter** | Runs a specific command (like `/bin/bash`) inside a *running* container. |

### Essential `docker run` Flags

These flags are used to configure the container at the moment of creation.

| Flag | Function | Usage Example |
| :--- | :--- | :--- |
| `-d` | **Detached** | Runs the container in the background. |
| `-p <host>:<cont>` | **Ports** | Maps the host machine's port to the container's port. |
| `--name <name>` | **Identity** | Assigns a human-readable name (instead of a random hash). |
| `--rm` | **Cleanup** | Automatically deletes the container when it stops. |
| `-v <host>:<cont>` | **Bind Mount** | Syncs a host folder to a container folder (for development). |
| `-it` | **Interactive** | Allocates a pseudo-TTY (required for shells like `bash`). |

---

## 2. Workflow A: The "Quick Utility" Loop

**Scenario:** You need a disposable web server (Nginx) to test some static HTML files, or a quick database for an experiemnt, without installing software on your host machine.

### Step 1: Run the container
Start the container in the background (`-d`), mapping port 8080 on your machine to port 80 in the container (`-p`), and give it a name so it is easy to reference.

```bash
$ docker run -d -p 8080:80 --name my-web nginx:alpine
# Output:
# Unable to find image 'nginx:alpine' locally
# alpine: Pulling from library/nginx
# ...
# 1234567890abcdef... (The new Container ID)
```

### Step 2: Verify it works
Check the process list to confirm the status is "Up".

```bash
$ docker ps
# Output:
# CONTAINER ID  IMAGE         STATUS        PORTS                 NAMES
# 1234567890ab  nginx:alpine  Up 5 seconds  0.0.0.0:8080->80/tcp  my-web
```

### Step 3: Cleanup
When finished, stop the container and remove it to free up the name.

```bash
$ docker stop my-web
# my-web

$ docker rm my-web
# my-web
```

---

## 3. Workflow B: The "Debug" Loop

**Scenario:** You try to start a container, but `docker ps` shows nothing. It crashed immediately upon startup.

### Step 1: Find the Corpse
Since `docker ps` only shows running containers, use the `-a` (all) flag to find the one that died.

```bash
$ docker ps -a
# Output:
# CONTAINER ID  IMAGE      STATUS                     NAMES
# a1b2c3d4e5f6  my-py-app  Exited (1) 10 seconds ago  agitated_turing
```

### Step 2: Check the Autopsy (Logs)
Use the Container ID from the previous step to read the crash report.

```bash
$ docker logs a1b2c3d4e5f6
# Output:
# Traceback (most recent call last):
#     File "app.py", line 10, in <module>
#         import requests
# ModuleNotFoundError: No module named 'requests'
```

### Step 3: Live Inspection
To fix this, you often need to look inside the image manually. Use `run` with `-it` (interactive) and overwrite the default startup command with a shell (`/bin/bash` or `/bin/sh`).

```bash
# --rm: Delete this debug container automatically when we exit
$ docker run -it --rm my-py-app /bin/bash

# The prompt changes. You are now INSIDE the container.
root@container:/app# ls -la
# ... list files ...
root@container:/app# pip list
# ... verify installed packages ...
root@container:/app# exit
```

---

## 4. Workflow C: The "Dev" Loop (Bind Mounts)

**Scenario:** You are developing a Node.js or Python application. You want the code to run inside Docker (to match the production environment), but you want changes saved in your local editor to update the running application instantly (**Hot Reloading**).

### Step 1: Run with Volume Mapping
We map the current directory `$(pwd)` to the `/app` folder inside the container.

```bash
# -w /app: Set working directory inside container
# -v $(pwd):/app: Sync current folder to /app (The Bind Mount)
# nodemon app.js: A tool that watches for file changes
$ docker run -dp 3000:3000 \
      -w /app -v "$(pwd):/app" \
      node:18:alpine \
      nodemon app.js
```

### Step 2: Edit & Observe
1. Open `app.js` in your local editor (Neovim/VS Code).
2. Change `console.log("Hello")` to `console.log("Hello World")`.
3. Save the file.
4. Because of the `-v` flag, the file inside the container updates instantly.
5. `nodemon` detects the change and restarts the server automatically.
