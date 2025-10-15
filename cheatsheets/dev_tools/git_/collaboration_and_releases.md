# `git`: Collaboration, Remotes & Releases

This guide covers the commands needed to work with others on a project. It includes syncing changes with remote servers like GitHub, managing remote repositories, and creating tags to mark official release points.

## Part 1: Working with Remotes

A "remote" is a pointer to another copy of the repository, usually on a server like GitHub.

|Command|Description|
|---|---|
|`git remote -v`|Lists all your configured remotes with their URLs.|
|`git remote add [name] [url]`|Adds a new remote. The standard name for the main remote is `origin`.|
|`git fetch [remote]`|**Fetches** all the latest changes from the remote but **does not merge them**. This updates your remote-tracking branches (e.g., `origin/main`).|

**Listing Your Remotes**

After cloning a repository from GitHub, you can use `git remote -v` to see the default remote, which is named `origin`.

```bash
# Show verbose list of remotes
git remote -v

# Output:
# origin	https://github.com/your-username/your-repo.git (fetch)
# origin	https://github.com/your-username/your-repo.git (push)
```

**Syncing a Fork with the Original Repository**

This is the standard workflow for keeping your fork up-to-date with the original project.

```bash
# 1. You have forked a repository. `origin` points to your fork.
git remote -v
# origin	https://github.com/your-username/forked-repo.git (fetch)
# origin	https://github.com/your-username/forked-repo.git (push)

# 2. Add the original repository as a remote named `upstream`.
git remote add upstream https://github.com/original-owner/repo.git

# Verify that the new remote was added
git remote -v
# origin	https://github.com/your-username/forked-repo.git (fetch)
# origin	https://github.com/your-username/forked-repo.git (push)
# upstream	https://github.com/original-owner/repo.git (fetch)
# upstream	https://github.com/original-owner/repo.git (push)

# 3. Fetch the latest changes from the original repository.
# This updates your local copy of the upstream branches (e.g., upstream/main)
git fetch upstream

# 4. Switch to your main branch and merge the changes from the original.
git checkout main
git merge upstream/main
```

## Part 2: Tagging & Releases

A "tag" is a permanent pointer to a specific commit, used to mark release points (e.g., `v1.0.0`).

|Tag Type|Description|
|---|---|
|Annotated|A full Git object. It contains the tagger's name, email, date, and a message. **This is the recommended type for releases.**|
|Lightweight|A simple pointer to a commit, with no extra information.|

**Setup**

First, let's create a commit to tag.

```bash
# Create a new file and commit it
echo "Release content" > version.txt
git add .
git commit -m "feat: Prepare for version 1.0.0"
```

**Creating and Inspecting Tags**

Here's how to create both an annotated and a lightweight tag and see the difference.

```bash
# 1. Create an annotated tag for version 1.0
git tag -a v1.0.0 -m "Release version 1.0.0"

# 2. Use `git show` to see the rich tag object information
git show v1.0.0
# Output shows tagger info, date, and message before the commit details:
# tag v1.0.0
# Tagger: Your Name <you@example.com>
# Date:   Sun Jul 27 00:25:22 2025 +0100
#
# Release version 1.0.0
#
# commit a1b2c3d...
# Author: Your Name <you@example.com>
# ...

# 3. Create a lightweight tag (just a name, no -a or -m)
git tag v1.0.1

# 4. Use `git show` on the lightweight tag. Note the lack of tagger info.
git show v1.0.1
# Output shows only the commit details:
# commit a1b2c3d...
# Author: Your Name <you@example.com>
# ...
```

**Listing and Pushing Tags**

```bash
# 1. List all local tags
git tag
# v1.0.0
# v1.0.1

# 2. Tags are not pushed by default. You must push them explicitly.
git push origin v1.0.0

# 3. Or push all of your tags at once.
git push --tags
```