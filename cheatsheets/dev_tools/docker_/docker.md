# Cheatsheet: Docker & Containerisation

**Docker** allows you to package applications and their dependencies into isolated units called containers. This guide covers the conceptual model, a comprehensive command reference, and real-world developer workflows.

## 1. The Mental Model

To use Docker effectively, you must distinguish between these core concepts:

* **Dockerfile:** The **Recipe**. A text document containing commands to assemble an image.
* **Image:** The **Blueprint**. An immutable, read-only template built from the Dockerfile.
* **Container:** The **House**. A mutable, running instance of an image. You can have many containers from one image.
* **Volume:** The **Hard Drive**. A persistent storage area managed by Docker, unrelated to the container's lifecycle.
* **Bind Mount:** The **Portal**. A link between a folder on your host machine and a folder inside the container.

---

## 2. Command Reference

### Image Management (The Blueprints)

| Command                     | Description                                                                 |
| :-------------------------- | --------------------------------------------------------------------------- |
| `docker build -t <name> .`  | **Build** an image from the `Dockerfile` in the current directory.          |
| `docker images`             | **List** all images stored locally.                                         |
| `docker rmi <image>`        | **Delete** an image from the local cache.                                   |
| `docker pull <image>`       | **Download** an image from a registry (like Docker Hub) without running it. |
| `docker tag <src> <target>` | **Alias** an image (e.g., tagging `myapp:latest` as `myapp:v1`).            |

### Container Lifecycle (The Instances)

| Command               | Description                                                                        |
| :-------------------- | ---------------------------------------------------------------------------------- |
| `docker run <image>`  | **Create & Start** a new container. (See flags below).                             |
| `docker ps`           | **List** currently running containers.                                             |
| `docker ps -a`        | **List All** containers, including stopped ones (essential for debugging crashes). |
| `docker stop <name>`  | **Graceful Stop**. Sends SIGTERM to the main process.                              |
| `docker kill <name>`  | **Force Stop**. Sends SIGKILL (immediate shutdown).                                |
| `docker start <name>` | **Resume**. Starts an existing, stopped container.                                 |
| `docker rm <name>`    | **Delete**. Removes a stopped container. Use `-f` to force-delete a running one.   |

### `docker run` Flags (Essential)

These flags are commonly used to configure the container at startup.

| Flag     | Function                                       | Example                                                          |
| :------- | ---------------------------------------------- | ---------------------------------------------------------------- |
| `-d`     | **Detached**. Runs in the background.          | `docker run -d nginx`                                            |
| `-p`     | **Ports**. Maps `Host:Container`.`             | `docker run -p 8080:80 nginx` (Localhost:8080 hits Container:80) |
| `--name` | **Name**. Assigns a human-readable name.       | `docker run --name my-web nginx`                                 |
| `-v`     | **Volume**. Mounts storage.                    | `docker run -v $(pwd):/app node`                                 |
| `-e`     | **Env**. Sets environment variables.           | `docker run -e NODE_ENV=prod node`                               |
| `--rm`   | **Cleanup**. Deletes container when it stops.  | `docker run --rm python python script.py`                        |
| `-it`    | **Interactive**. Allocates a TTY (for shells). | `docker run -it ubuntu bash`                                     |

### Inspection & Debugging

| Command                        | Description                                                              |
| :----------------------------- | ------------------------------------------------------------------------ |
| `docker logs <name>`           | **Read Output**. Shows stdout/stderr. Add `-f` to follow (tail).         |
| `docker exec -it <name> <cmd>` | **Execute**. Runs a command inside a *running* container (e.g., `bash`). |
| `docker inspect <name>`        | **Details**. Returns low-level JSON info (IP address, mounts, config).   |
| `docker stats`                 | **Monitor**. Live stream of CPU, RAM, and Net usage for all containers.  |

---

## 3. Workflow A: The "Quick Utility" Loop

**Scenario:** You need a quick web server (Nginx) to test some static HTML files, or a Postgres database for a quick experiment, but you don't want to install them on your actual machine.

### Step 1: Run the container
Run the container in the background (`-d`), mapping port 8080 on your machine to port 80 in the container (`-p`).

```bash
$ docker run -d -p 8080:80 --name my-web-server nginx:alpine

# Output:
# Unable to find image 'nginx:alpine' locally
# alpine: Pulling from library/nginx
# ...
# 1234567890abcdef... (The new Container ID)
```

### Step 2: Verify it works
Check the process list to confirm it is "Up".

```bash
$ docker ps

# Output:
# CONTAINER ID  IMAGE         STATUS        PORTS                 NAMES
# 1234567890ab  nginx:alpine  Up 5 seconds  0.0.0.0:8080->80/tcp  my-web-server
```

### Step 3: Cleanup
When finished, stop the container and remove it to free up the name.

```bash
$ docker stop my-web-server
# my-web-server

$ docker rm my-web-server
# my-web-server
```

---

## 4. Workflow B: The "Debug" Loop

**Scenario:** A container is crashing immediately upon startup, or the application inside isn't behaving correctly. `docker ps` shows nothing because the container is already dead.

### Step 1: Analyse Logs
Use `docker ps -a` (all) to find the container ID, then check the logs.

```bash
$ docker ps -a
# CONTAINER ID  IMAGE      STATUS                     NAMES
# a1b2c3d4e5f6  my-py-app  Exited (1) 10 seconds ago  agitated_turing

$ docker logs a1b2c3d4e5f6
# Output:
# Traceback (most recent call last):
#     File "app.py", line 10, in <module>
#         import requests
# ModuleNotFoundError: No module named 'requests'
```

### Step 2: Interactive Entry
To fix this, you might want to open a shell *inside* the image to test commands manually.

* **If the container is running:** Use `exec`
* **If the container crashes instantly:** Use `run` with a shell override.

```bash
# -i: Interactive (keep STDIN open)
# -t: TTY (allocate a terminal)
# --rm: Delete this debug container when we exit
$ docker run -it --rm my-py-app /bin/bash

# The prompt changes. You are now INSIDE the container.
root@container:/app# pip list
# Package    Version
# ---------- -------
# pip        20.0.1
# (requests is missing!)

root@container:/app# exit
```

---

## Workflow C: The "Development" Loop (Bind Mounts)

**Scenario:** You are developing a Node.js or Python app. You want to run the code inside Docker (to match production), but you want your changes to apply instantly when you save a file on your host machine.

### Step 1: Run with Volume Mapping
We map the current directory `$(pwd)` to the `/app` folder inside the container.

```bash
# -w /app: Set working directory inside container
# -v $(pwd):/app: Sync current folder to /app
# nodemon app.js: A tool that watches for file changes
$ docker run -dp 3000:3000 \
      -w /app -v "$(pwd):/app" \
      node:18-alpine \
      nodemon app.js
```

### Step 2: Edit Code
1. Open `app.js` in your local editor (VS Code, Neovim).
2. Change `console.log("Hello")` to `console.log("Hello World").`
3. Save the file.

### Step 3: Observe
Because of the Bind Mount (`-v`), the file inside the container updates instantly. `nodemon` sees the change and restarts the app automatically.

---

## 6. Workflow D: The "Full Stack" Loop (Compose)

**Scenario:** Developing an application that requires a PostgreSQL database. Configuration is defined in a `compose.yaml` (or `docker-compose.yml`) file.

**Note:** Modern versions use `docker compose` (space), not `docker-compose` (dash).

### Step 1: Spin Up
Start the entire stack in the background.

```bash
$ docker compose up -d

# Output:
# [+] Running 2/2
# ✔ Container my-app-db-1   Started
# ✔ Container my-app-web-1  Started
```

### Step 2: Monitor Logs
Watch the logs of all services simultaneously.

```bash
$ docker compose logs -f

# Output:
# db-1   | database system is ready to accept connections
# web-1  | Connecting to database...
# web-1  | Connected! Listening on port 3000
```

### Step 3: Reset Environment
Sometimes the database state gets messy, and a fresh slate is required.

```bash
# Stop containers and remove the Volumes (-v) containing the database data
$ docker compose down -v

# Output:
# [+] Running 3/3
# ✔ Container my-app-web-1  Removed
# ✔ Container my-app-db-1   Removed
# ✔ Volume my-app_db_data   Removed
```

---

## 7. System Hygiene (Disk Space)

Docker objects can consume significant disk space over time (old images, stopped containers, build caches).

| Command                  | Action                                                                                                                              |
| :----------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `docker system df`       | **Disk Usage.** Shows how much space images and containers are taking up.                                                           |
| `docker system prune`    | **Safe Cleanup.** Deletes stopped containers, unused networks, and dangling images (layers with no relationship to a tagged image). |
| `docker system prune -a` | **Aggressive Cleanup.** Deletes **ALL** images not currently used by a running container.                                           |
| `docker volume prune`    | **Deep Clean.** Deletes all unused volumes. **Warning:** This will permanently delete database data.                                |

```bash
$ docker system df
# TYPE
# Images
# Containers

$ docker system prune
# WARNING! This will remove:
#   - all stopped containers
#   - all networks not used by at least one container
#   - all dangling images (untagged builds)
#
# Are you sure you want to continue? [y/N] y
# ...
# Total reclaimed space: 1.8GB
```
