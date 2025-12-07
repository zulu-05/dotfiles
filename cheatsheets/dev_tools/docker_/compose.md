# Docker: Compose & Orchestration

**Docker Compose** is a tool for defining and running multi-container applications (e.g., App + Database + Cache). Configuration is defined in a `compose.yaml` (or `docker-compose.yml`) file.

### Version Note: V1 vs V2
*   **Old (V1):** Used the hyphenated command `docker-compose`. This was a separate Python script and is now deprecated.
*   **New (V2):** Uses the space command `docker compose`. This is a plugin built directly into the Docker CLI. **Always use this version.**

---

## 1. Command Reference

All commands must be run from the directory containing your `compose.yaml` file.

| Command | Action | Description |
| :--- | :--- | :--- |
| `docker compose up -d` | **Start** | Builds (if needed) and starts all services defined in the YAML file in the background. |
| `docker compose down` | **Stop** | Stops containers and removes the containers and networks created by `up`. |
| `docker compose logs -f` | **Monitor** | Follows the log output of all services simultaneously, aggregated into one stream. |
| `docker compose ps` | **Status** | Lists the current status of the stack's containers. |
| `docker compose build` | **Rebuild** | Forces a rebuild of the images (useful if you changed the Dockerfile but not the image tag). |
| `docker compose restart` | **Bounce** | Restarts the services without removing the containers or networks. |

---

## 2. Workflow: The "Full Stack" Loop

**Scenario:** You are developing a web application (`web`) that depends on a PostgreSQL database (`db`). Your `compose.yaml` defines both services and a shared network.

### Step 1: Spin Up (Initialisation)
Start the entire stack. Docker Compose automatically handles the dependency order (starting the DB before the App if configure) and creates a dedicated virtual network so they can communicate by name.

```bash
$ docker compose up -d

# Output:
# [+] Running 4/4
# ✔  Network myapp_default  Created
# ✔  Volume myapp_db_data   Created
# ✔  Container myapp-db-1   Started
# ✔  Container myapp-web-1  Started
```

### Step 2: Monitor (Aggregated Logs)
Watch the interaction between services. Compose prefixes every log line with the service name and a unique colour, making it easy to spot errors in complex stacks.

```bash
$ docker compose logs -f

# Output:
# db-1   | 2023-10-27 10:00:01 UTC [1] LOG:
# web-1  | [INFO] Connecting to database at host='db' port=5432...
# web-1  | [INFO] Connection successful! Server listening on port 3000.
# web-1  | [INFO] GET /api/users 200 OK
```

### Step 3: Reset (The Clean Slate)
During development, your database might get corrupted, or you might simply want to run a migration test from scratch.

* `down`: Stops containers and removes networks.
* `-v`: **Important.** Removes the named Volumes (deletes the actual database data).

```bash
$ docker compose down -v

# Output:
# [+] Running 3/3
# ✔  Container myapp-web-1  Removed
# ✔  Container myapp-db-1   Removed
# ✔  Volume myapp_db_data   Removed
```

### Step 4: Rebuild (Dependency Updates)
If you modify your code, the container usually updates via Bind Mounts. However, if you modify `requirements.txt` (Python) or `package.json` (Node), you must force a rebuild of the image to install the new dependencies.

```bash
# --build: Forces a build of the image before starting the container
$ docker compose up -d --build

# Output:
# [+] Building 12.5s (8/8) FINISHED
# ...
# ✔  Container myapp-web-1  Recreated
```
