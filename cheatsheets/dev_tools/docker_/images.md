# Docker: Images & Building

This guides focuses on the "blueprints"-building images from Dockerfiles, managing versions/tags, and maintaining disk hygiene.

**Key Concept:** An **Image** is an immutable, read-only template (the class). A **Container** is a running instance of that image (the object).

## 1. Command Reference

### Image Management

| Command | Action | Description |
| :--- | :--- | :--- |
| `docker build -t <name> .` | **Build** | Creates an image from the `Dockerfile` in the current directory (`.`). |
| `docker images` | **List** | Shows all images stored in the local cache, including size and ID. |
| `docker tag <src> <tgt>` | **Alias** | Creates a new tag for an existing image ID (e.g., tagging `latest` as `v1.0`). |
| `docker rmi <name>` | **Delete** | Removes an image from the local cache. |
| `docker pull <name>` | **Download** | Pulls an image from a registry (like Docker Hub) without running it. |
| `docker history <name>` | **Inspect** | Shows the individual layers that make up an image (useful for optimising size). |

### System Hygiene (Disk Space)

Docker objects allow storage to accumulate quickly. These commands help reclaim space.

| Command | Action | Description |
| :--- | :--- | :--- |
| `docker system df` | **Usage** | Shows the total space consumed by images, containers, and volumes. |
| `docker system prune` | **Cleanup** | Deletes stopped containers, unused networks, and **dangling** images (build failures). |
| `docker system prune -a` | **Deep Clean** | Deletes **ALL** images that are not currently being used by a running container. |

---

## 2. Workflow A: The Build Cycle

**Scenario:** You have written a `Dockerfile` for your application and need to package it into a versioned artifact for deployment.

### Step 1: Build the Image
Run the build command. The `-t` flag assigns a name (repository) to the image. The `.` at the end tells Docker to use the files in the current directory.

```bash
$ docker build -t myapp .
# Output:
# [+] Building 2.3s (8/8) FINISHED
# ...
# writing image sha256:a1b2c3d4e5f6...
# naming to docker.io/library/myapp
```

### Step 2: Verification
Check the local registry to see the new image and its size. By default, it is given the `latest` tag.

```bash
$ docker images
# REPOSITORY  TAG     IMAGE ID      CREATED         SIZE
# myapp       latest  a1b2c3d4e5f6  10 seconds ago  150MB
```

### Step 3: Versioning (Tagging)
The `latest` tag is mutable and dagerous for production. Creates a specific version tag (`v1.0`) pointing to this specific build.

```bash
# docker tag [SOURCE_IMAGE} [TARGET_IMAGE]
$ docker tag myapp myapp:v1.0
```

### Step 4: Test the Artifact
Run the image briefly to ensure it works before pushing or deploying.

```bash
# --rm ensures the test container is deleted immediately after it stops
$ docker run --rm myapp:v1.0
# Output:
# Server started on port 3000...
```

---

## 3. Workflow B: The Cleanup Cycle

**Scenario:** You have been debugginng a `Dockerfile` all day, running the build command 20 times. You noticed your hard drive is filling up.

### Step 1: Diagnose Disk Usage
Check how much space Docker is consuming.

```bash
$ docker system df
# Output:
# TYPE        TOTAL  ACTIVE  SIZE   RECLAIMABLE
# Images      25     2       4.5GB  3.8GB (84%)
# Containers  2      2       100MB  0B (0%)
```

*Note: "Reclaimable" space usually consist of "Dangling images": intermediate layers from builds that were overwritten and are no longer named.*

### Step 2: Prune Dangling Images
Run the standard prune command. This is safe; it will **not** delete images that are tagged (like `myapp:v1.0`).

```bash
$ docker system prune
# Output:
# WARNING! This will remove:
#     - all stopped containers
#     - all networks not used by at least one container
#     - all dangling images
#
# Are you sure you want to continue? [y/N] y
# ...
# Total reclaimed space: 3.8GB
```

### Step 3: Deep Clean (Optional)
If you need to free up maximum space and are willing to re-download base images (like `python` or `node`) the next time you build, use the aggressive prune.

```bash
$ docker system prune -a
# This deletes EVERTHING not currently in use by a running container.
```
