# `git`: Basics & Daily Workflow

This guide covers the essential commands for configuring Git on a new machine and for performing the fundamental daily cycle of creating, staging, and saving changes to a repository.

## Part 1: Configuration & Setup

You only need to do this once per machine. These commands configure your identity.

|Command|Description|
|---|---|
|`git config --global user.name "[name]"`|Sets the name that will be attached to your commits and tags.|
|`git config --global user.email "[email]"`|Sets the email address that will be attached to your commits.|
|`git config --global core.editor "nvim"`|Sets the default text editor used for writing commit messages.|
|`git config --global init.defaultBranch main`|Sets the default branch name to `main` for all new repositories.|
|`git config --list`|Shows your current configuration.|

## Part 2: The Daily Workflow

This is the core loop of creating and saving changes to your project.

### Creating a Repository

You start a project in one of two ways:

|Command|Description|
|---|---|
|`git init`|Initializes a new, empty Git repository in the current directory. This creates the hidden `.git/` directory where all history is stored.|
|`git clone [url]`|**Clones** an existing repository from a remote URL (like GitHub) onto your local machine. This is the most common way to start working on a project.|

#### Workflow Demonstrations

**Using `git init`**

This workflow is for starting a brand new project from scratch on your local machine.

```bash
# 1. Create a directory for your new project and navigate into it
mkdir my-new-app
cd my-new-app

# 2. Initialize it as a Git repository
git init
# Output: Initialized empty Git repository in /path/to/my-new-app/.git/

# 3. Check the directory contents, including hidden files
ls -a
# Output: . .. .git

# The presence of the .git directory confirms that this is now a Git repository.
# All your project's history will be stored inside it.
```

**Using `git clone`**

This is the most common workflow. You use it when you want to contribute to an existing project or use it as a starting point.

```bash
# 1. Clone a remote repository using its URL.
# Git creates a new directory named after the repository.
git clone https://github.com/git/git.git
# Output:
# Cloning into 'git'...
# remote: Enumerating objects: 322045, done.
# remote: Counting objects: 100% (369/369), done.
# remote: Compressing objects: 100% (235/235), done.
# remote: Total 322045 (delta 156), reused 288 (delta 124), pack-reused 321676
# Receiving objects: 100% (322045/322045), 154.55 MiB | 15.68 MiB/s, done.
# Resolving deltas: 100% (241859/241859), done.
# Updating files: 100% (3614/3614), done.

# 2. Navigate into the newly created directory
cd git

# A .git directory already exists, and the project is ready to go.
ls -a
# Output: . .. .git .mailmap .travis.yml ... (and all other project files)
```

### Saving Changes

This is the fundamental "save" cycle in Git.

**Workflow Example:**

```bash
# Step 0: Check the state of your repository. This is your most used command.
# It tells you which files are modified, which are staged, and which are untracked.
git status

# Step 1: Stage your changes.
# The "staging area" is a draft of your next commit. This lets you be selective
# about what you save.

# Stage a single file.
git add src/main.rs

# Stage all modified and new files in the current directory and subdirectories.
git add .

# Step 2: Commit your staged changes to the local repository.
# This creates a permanent snapshot of your staged files.
# The -m flag lets you provide a short summary message.
git commit -m "feat: Add user authentication feature"

# If you omit -m, Git will open your configured editor to write a longer message.
git commit
```

|Command|Description|
|---|---|
|`git status`|**Shows the status** of the working directory and the staging area. It is the most important command for orienting yourself.|
|`git add [file]`|**Adds** file contents to the staging area (the "index"). This prepares the content for the next commit.|
|`git commit`|**Commits** the staged snapshot to the project history. Each commit is a permanent, unique snapshot of the project at that point in time.|

### Syncing with Remotes

These commands are for collaborating with others by sending and receiving changes from a remote server like GitHub.

|Command|Description|
|---|---|
|`git push`|**Pushes** your committed changes from your local repository up to the remote repository (e.g., GitHub).|
|`git pull`|**Pulls** down the latest changes from the remote repository and merges them into your current branch. It's a combination of `git fetch` and `git merge`.|

#### Workflow Demonstration

This workflow simulates two developers working on the same project to show how changes are shared.

**1. Developer A: Make and push a change**

First, Developer A makes a change, commits it, and **pushes** it to the central remote repository.

```bash
# Assume we are in a project directory connected to a remote.
# Create a new file to represent a new feature.
echo "Initial feature content" > feature.txt

# Add and commit the new file
git add feature.txt
git commit -m "feat: Add initial feature file"

# Now, push the committed changes to the 'main' branch on the remote 'origin'
git push origin main
# Output:
# Enumerating objects: 3, done.
# Counting objects: 100% (3/3), done.
# Writing objects: 100% (3/3), 256 bytes | 256.00 KiB/s, done.
# Total 3 (delta 0), reused 0 (delta 0), pack-reused 0
# To github.com:your-username/your-repo.git
#  * [new branch]      main -> main
```

**2. Developer B: Pull the change**

Now, Developer B, working on their own copy of the project, can **pull** those changes to get the latest version.

```bash
# Developer B's copy doesn't have the new file yet.
ls
# README.md

# Pull the latest changes from the remote 'origin'
git pull origin main
# Output:
# From github.com:your-username/your-repo
#  * branch            main       -> FETCH_HEAD
# Updating 1a2b3c4..5d6e7f8
# Fast-forward
#  feature.txt | 1 +
#  1 file changed, 1 insertion(+)
#  create mode 100644 feature.txt

# The new file now appears in Developer B's directory.
ls
# README.md feature.txt
```