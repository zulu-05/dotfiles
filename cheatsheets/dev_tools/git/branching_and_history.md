# `git`: Branching & Inspecting History

This guide covers how to use branches to work on different features in isolation and the essential commands for exploring the project's past, from viewing commit logs to comparing different versions of the code.

## Part 1: Branching & Merging

Branching is the feature that makes Git so powerful. A branch is a movable pointer to a commit, allowing you to work on different features in isolation.

**Workflow Example (Feature Branch):**

```bash
# You are on the 'main' branch. Let's create a new branch for a new feature.
# The -b flag creates the new branch AND checks it out in one step.
git checkout -b new-feature

# Now you are on the 'new-feature' branch. Let's do some work...
# (edit files)
git add .
git commit -m "feat: Implement the core logic for the new feature"

# (edit more files)
git add .
git commit -m "fix: Correct a bug in the new feature"

# The feature is done. Let's go back to the main branch.
git checkout main

# Now, merge the work from 'new-feature' into 'main'.
git merge new-feature

# The 'main' branch now has all the commits from 'new-feature'.
# We can now safely delete the feature branch.
git branch -d new-feature
```

| Command                 | Description                                                                                             |
| ----------------------- | ------------------------------------------------------------------------------------------------------- |
| `git branch`            | Lists all branches in your local repository.                                                            |
| `git branch [name]`     | Creates a new branch named `[name]`.                                                                    |
| `git checkout [branch]` | Switches your working directory to the specified branch.                                                |
| `git merge [branch]`    | Merges the history of the specified branch into your current branch.                                    |
| `git branch -d [name]`  | **D**eletes the specified branch. Git will prevent you from deleting a branch that has not been merged. |

## Part 2: Inspecting History

These commands let you explore the project's past.

### `git log`

Shows the commit history for the current branch.

|Command|Description|
|---|---|
|`git log`|Shows the full commit history with authors, dates, and full messages.|
|`git log --oneline`|A more concise view, showing just the commit hash and the first line of the commit message.|
|`git log --graph --decorate --oneline`|**The Power Alias.** Shows the commit history as a graph, which is essential for visualizing branches and merges.|
|`git log -p [file]`|Shows the history for a specific file, including the **p**atch (the changes) for each commit.|
#### Workflow Demonstrations

**Setup**

To demonstrate the `log` commands, let's first create a simple repository history with a feature branch that gets merged into `main`.

```bash
# Set up the repo and initial commit
git init
echo "Initial content" > file.txt
git add file.txt
git commit -m "Initial commit"

# Create and work on a feature branch
git checkout -b new-feature
echo "Feature work" > feature.txt
git add feature.txt
git commit -m "feat: Implement new feature"

# Return to main and merge the feature
git checkout main
git merge new-feature
```

**`git log`**

The default command shows the full history in detail.

```bash
git log
```

```bash
commit 5d6e7f8... (HEAD -> main, new-feature)
Merge: 1a2b3c4 9d8e7f6
Author: Your Name <you@example.com>
Date:   Sat Jul 27 00:30:00 2025 +0100

    Merge branch 'new-feature'

commit 9d8e7f6...
Author: Your Name <you@example.com>
Date:   Sat Jul 27 00:29:00 2025 +0100

    feat: Implement new feature

commit 1a2b3c4...
Author: Your Name <you@example.com>
Date:   Sat Jul 27 00:28:00 2025 +0100

    Initial commit
```

**`git log --oneline`**

This provides a much more compact view of the history.

```bash
git log --oneline
```

```bash
5d6e7f8 (HEAD -> main, new-feature) Merge branch 'new-feature'
9d8e7f6 feat: Implement new feature
1a2b3c4 Initial commit
```

**`git log --graph --decorate --oneline`**

This "power alias" is the best way to visualize how branches and merges relate to each other.

```bash
git log --graph --decorate --oneline
```

```
* 5d6e7f8 (HEAD -> main, new-feature) Merge branch 'new-feature'
|\
| * 9d8e7f6 feat: Implement new feature
|/
* 1a2b3c4 Initial commit
```

**`git log -p [file]`**

Use the `-p` flag to see the history of a specific file, including the changes (patch) made in each commit.

```bash
git log -p feature.txt
```

```bash
commit 9d8e7f6...
Author: Your Name <you@example.com>
Date:   Sat Jul 27 00:29:00 2025 +0100

    feat: Implement new feature

diff --git a/feature.txt b/feature.txt
--- a/feature.txt
+++ b/feature.txt
@@ -1 +1 @@
-Initial content
+Feature work
```

### `git diff`

Shows the differences between commits, branches, or the working directory.

| Command                        | Description                                                                    |
| ------------------------------ | ------------------------------------------------------------------------------ |
| `git diff`                     | Shows the changes in your working directory that have **not yet been staged**. |
| `git diff --staged`            | Shows the changes that **are staged** and will be in the next commit.          |
| `git diff [branch]`            | Shows the differences between your current branch and another branch.          |
| `git diff [commit1] [commit2]` | Shows the differences between two specific commits.                            |

#### Workflow Demonstrations

**Setup**

For these examples, let's assume we have a repository with an initial commit and a `README.md` file containing the text "Version 1".

```bash
# Initial setup
git init
echo "Version 1" > README.md
git add README.md
git commit -m "Initial commit"
```

**`git diff`**

This command shows unstaged changes.

```bash
# 1. Modify the file in your working directory
echo "Version 2" > README.md

# 2. Run git diff to see the changes that are NOT yet staged
git diff
```

```diff
diff --git a/README.md b/README.md
index 1234567..89abcde 100644
--- a/README.md
+++ b/README.md
@@ -1 +1 @@
-Version 1
+Version 2
```

**`git diff --staged`**

This command shows changes that have been staged but not yet committed.

```bash
# 1. Stage the change from the previous example
git add README.md

# 2. Now, `git diff` shows nothing because there are no unstaged changes
git diff

# 3. Use `git diff --staged` to see what's in the staging area for the next commit
git diff --staged
```

```diff
diff --git a/README.md b/README.md
index 1234567..89abcde 100644
--- a/README.md
+++ b/README.md
@@ -1 +1 @@
-Version 1
+Version 2
```

**`git diff [branch]`**

This shows the difference between your current branch and another one.

```bash
# 1. Create a new branch and add a commit to it
git checkout -b new-feature
echo "A new feature" > feature.md
git add feature.md
git commit -m "feat: Add new feature"

# 2. Switch back to the main branch
git checkout main

# 3. Check the difference between `main` and `new-feature`
git diff new-feature
```

```diff
diff --git a/feature.md b/feature.md
new file mode 100644
index 0000000..fedcba9
--- /dev/null
+++ b/feature.md
@@ -0,0 +1 @@
+A new feature
```

**`git diff [commit1] [commit2]`**

This compares two specific commits directly using their hashes.

```bash
# 1. Get the commit hashes from the log
git log --oneline
# 5d6e7f8 (HEAD -> main) feat: Add new feature
# 1a2b3c4 Initial commit

# 2. Compare the two commits to see what changed between them
git diff 1a2b3c4 5d6e7f8
```

```diff
diff --git a/feature.md b/feature.md
new file mode 100644
index 0000000..fedcba9
--- /dev/null
+++ b/feature.md
@@ -0,0 +1 @@
+A new feature
```

### Advanced Log & Search

|Command|Description|
|---|---|
|`git log --author="[name]"`|Find all commits by a specific person.|
|`git log --grep="[pattern]"`|Search for commits with a specific word or pattern in their message.|
|`git log --since="2 weeks ago"`|Show commits made in the last two weeks. Also works with `--until`.|
|`git log -S"[code]"`|Search for commits that introduced or removed a specific line of code (the "pickaxe" search).|

#### Workflow Demonstrations

**Setup**

For these examples, we'll create a repository with a few commits from different authors and with specific content to make the searches meaningful.

```bash
# Initial setup
git init
git config user.name "Your Name" && git config user.email "you@example.com"
echo "Initial version" > app.js
git add . && git commit -m "feat: Initial project setup"

# Second commit
echo "const API_KEY = '12345';" >> app.js
git add . && git commit -m "feat: Add API key"

# Third commit from another author
git config user.name "Jane Doe" && git config user.email "jane@example.com"
echo "// Remove API key for security" > app.js
git add . && git commit -m "fix: Remove insecure key"
```

**`git log --author`**

This command filters the log to show commits made by a specific person.

```bash
# Search for all commits by "Jane Doe"
git log --author="Jane Doe" --oneline
```

```bash
a1b2c3d (HEAD -> main) fix: Remove insecure key
```

**`git log --grep`**

This command searches the commit messages for a specific pattern.

```bash
# Find all commits with "feat" in their message
git log --grep="feat" --oneline
```

```bash
e4f5g6h feat: Add API key
i7j8k9l feat: Initial project setup
```

**`git log --since`**

This command shows commits made after a certain date.

```bash
# Show all commits made in the last two weeks
git log --since="2 weeks ago" --oneline

# Given the current date of July 26, 2025, this will show all commits in the
# setup above, as they were all created recently.
```

```bash
a1b2c3d (HEAD -> main) fix: Remove insecure key
e4f5g6h feat: Add API key
i7j8k9l feat: Initial project setup
```

**`git log -S`**

The "pickaxe" search finds commits where the number of occurrences of a specific string changed. It's perfect for finding when a specific line of code was added or removed.

```bash
# Find all commits that introduced or removed the string "API_KEY"
git log -S"API_KEY" --oneline -p
```

```bash
commit a1b2c3d...
Author: Jane Doe <jane@example.com>
Date:   Sat Jul 26 23:56:30 2025 +0100

    fix: Remove insecure key

diff --git a/app.js b/app.js
--- a/app.js
+++ b/app.js
@@ -1,2 +1 @@
-Initial version
-const API_KEY = '12345';
+// Remove API key for security

commit e4f5g6h...
Author: Your Name <you@example.com>
Date:   Sat Jul 26 23:56:30 2025 +0100

    feat: Add API key

diff --git a/app.js b/app.js
--- a/app.js
+++ b/app.js
@@ -1 +1,2 @@
 Initial version
+const API_KEY = '12345';
```

## Part 3: Undoing Changes

These commands let you revert mistakes. **Use `reset` with caution on shared branches, as it rewrites history.**

| Command                  | Description                                                                                                                                                                                                         |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `git checkout -- [file]` | **Discards changes in the working directory.** This reverts the specified file to the version from the last commit. **This is a destructive, unrecoverable action.**                                                |
| `git reset HEAD [file]`  | **Unstages** a file. It removes the file from the staging area but leaves the changes in your working directory.                                                                                                    |
| `git reset [commit]`     | **(Use with caution)** Moves the current branch pointer back to a previous commit, effectively erasing commits from the history. This rewrites history and can cause problems if you've already pushed the commits. |
| `git revert [commit]`    | **(The safe way to undo)** Creates a _new_ commit that is the exact opposite of the specified commit. This undoes the changes without rewriting history, making it safe for commits that have already been pushed.  |

#### Workflow Demonstrations

**`git checkout -- [file]` (Discard working directory changes)**

This is for when you want to completely throw away uncommitted changes to a file.

```bash
# Setup: Assume 'file.txt' contains "Version 1"
# 1. Make a change to the file
echo "This is a mistake" > file.txt

# 2. Check the status to see the modification
git status
# On branch main
# Changes not staged for commit:
#   (use "git add <file>..." to update what will be committed)
#   (use "git restore <file>..." to discard changes in working directory)
#	modified:   file.txt

# 3. Discard the changes to bring the file back to its last committed state
git checkout -- file.txt

# 4. Check the status again. The working directory is now clean.
git status
# On branch main
# nothing to commit, working tree clean
```

**`git reset HEAD [file]` (Unstage a file)**

Use this when you have staged a file with `git add` but decide you don't want to include it in the next commit.

```bash
# 1. Modify and stage a file
echo "A new line" >> file.txt
git add file.txt

# 2. Check the status. The file is staged.
git status
# Changes to be committed:
#	modified:   file.txt

# 3. Unstage the file. The changes are removed from the staging area.
git reset HEAD file.txt

# 4. Check the status again. The changes are now back in the working directory, not staged.
git status
# Changes not staged for commit:
#	modified:   file.txt
```

**`git reset [commit]` (Reset to a previous commit)**

This rewrites history by moving the branch pointer. It's best used only on local commits that you haven't pushed yet.

```bash
# Setup: Assume your history has a "Commit 2" on top of "Commit 1"
git log --oneline
# a1b2c3d (HEAD -> main) Commit 2
# e4f5g6h Commit 1

# 2. Reset the branch back one commit, to the state of "Commit 1"
# HEAD~1 refers to the commit before the current HEAD
git reset HEAD~1

# 3. Check the log. "Commit 2" is no longer in the history.
git log --oneline
# e4f5g6h (HEAD -> main) Commit 1

# The changes from "Commit 2" are now unstaged in your working directory.
git status
# Changes not staged for commit:
#	modified:   file.txt
```

**`git revert [commit]` (Safely undo a commit)**

This is the safe way to undo a public commit. It creates a _new_ commit that reverses the specified changes, keeping the project history intact.

```bash
# Setup: Assume your history has a "Commit 2"
git log --oneline
# a1b2c3d (HEAD -> main) Commit 2
# e4f5g6h Commit 1

# 2. Revert the most recent commit (HEAD)
# This will open an editor for you to write a commit message for the revert.
git revert HEAD

# 3. Check the log. A new commit has been added that undoes "Commit 2".
git log --oneline
# i7j8k9l (HEAD -> main) Revert "Commit 2"
# a1b2c3d Commit 2
# e4f5g6h Commit 1
```

## Part 4: Stashing Changes

`git stash` is a temporary holding area for uncommitted changes. It's perfect for when you need to quickly switch context without making a messy commit.

**Workflow Example:**
1. You are working on `feature-A`. You have modified several files but aren't ready to commit.
2. An urgent bug report comes in. You need to switch to the `main` branch to fix it.
3. `git stash` - Your working directory is now clean, and your changes are saved in the stash.
4. `git checkout main`
5. _(Fix the bug, add, commit, and push the fix)_
6. `git checkout feature-A` - Switch back to your feature branch.
7. `git stash pop` - Re-applies your stashed changes, and you can continue where you left off.

|Command|Description|
|---|---|
|`git stash`|Saves your uncommitted changes (both staged and unstaged) to a new stash and cleans your working directory.|
|`git stash list`|Lists all the stashes you have saved.|
|`git stash pop`|Applies the most recent stash and then deletes it from the list.|
|`git stash apply`|Applies the most recent stash but **leaves it in the list**. Useful if you want to apply the same changes to multiple branches.|

#### Workflow Demonstration

This workflow simulates a common scenario: you're in the middle of work when you need to pause and address an urgent issue.

**1. Start working on a feature**

First, let's make some changes that aren't ready to be committed.

```bash
# Setup: We start with a clean repository
# 1. Modify a tracked file
echo "New feature work" >> file.txt

# 2. Create a new, untracked file
echo "Another new file" > new_file.txt

# 3. Check the status. The working directory is "dirty".
git status
# On branch main
# Changes not staged for commit:
#	modified:   file.txt
# Untracked files:
#	new_file.txt
```

**2. Stash the changes to work on something else**

An urgent bug report comes in. We need to save our work and get a clean directory.

```bash
# Stash all changes, including untracked files (-u)
git stash -u
# Saved working directory and index state WIP on main: ...
# Untracked files: 1) new_file.txt

# The working directory is now clean
git status
# On branch main
# nothing to commit, working tree clean

# We can see our saved work in the stash list
git stash list
# stash@{0}: WIP on main: ...
```

**3. Address the urgent issue**

Now that the directory is clean, we can create a hotfix.

```bash
# (Fix the bug, add, commit, and push the fix)
echo "hotfix" > hotfix.txt
git add hotfix.txt
git commit -m "fix: Urgent hotfix"
```

**4. Restore the stashed work**

Once the urgent work is done, we can return to our feature. `git stash pop` re-applies the stashed changes and removes the stash from the list.

```bash
# Pop the most recent stash to get our work back
git stash pop
# On branch main
# Changes not staged for commit:
#   (use "git add <file>..." to update what will be committed)
#   (use "git restore <file>..." to discard changes in working directory)
#	modified:   file.txt
#
# Untracked files:
#   (use "git add <file>..." to include in what will be committed)
#	new_file.txt
# Dropped refs/stash@{0} (...)

# The stash is no longer in the list
git stash list
```

## Part 5: Basic Rebase

Before cleaning up history, it's important to understand what a basic rebase does. Rebasing is an alternative to merging for integrating changes from one branch into another. Instead of creating a merge commit, **rebase replays** the commits from your feature branch on top of the tip of another branch. This results in a cleaner, linear project history.

**Warning:** Like `git reset`, `git rebase` rewrites commit history. **Never rebase a branch that has been pushed and is being used by other collaborators.**

|Command|Description|
|---|---|
|`git rebase [base_branch]`|Re-applies the commits from your current branch onto the tip of `[base_branch]`.|

#### Workflow Demonstration

This example shows how `rebase` creates a linear history compared to the "bubble" created by `git merge`.

**1. Setup: Create a diverged history**

We'll start with a `main` branch, then create a `feature` branch. While we work on the feature, another commit is added to `main`, causing the branches to diverge.

```bash
# Initial setup
git init
echo "A" > file.txt && git add . && git commit -m "Commit A"

# Create a feature branch
git checkout -b new-feature
echo "B" > file.txt && git add . && git commit -m "Commit B"

# Meanwhile, a new commit is added to the main branch
git checkout main
echo "C" > other.txt && git add . && git commit -m "Commit C"

# View the diverged history
git log --graph --oneline --all
```

```bash
* 1d2e3f4 (HEAD -> main) Commit C
| * 4g5h6i7 (new-feature) Commit B
|/
* 7j8k9l0 Commit A
```

**2. Perform the Rebase**

Now, on the `new-feature` branch, we rebase it onto `main`. Git will "replay" Commit B on top of Commit C.

```bash
# Switch to the feature branch and rebase it onto main
git checkout new-feature
git rebase main
# Output:
# Successfully rebased and updated refs/heads/new-feature.

# View the new linear history
git log --graph --oneline --all
```

```bash
* a1b2c3d (HEAD -> new-feature) Commit B
* 1d2e3f4 (main) Commit C
* 7j8k9l0 Commit A
```

Notice how the history is now a straight line. "Commit B" has been reapplied on top of "Commit C".

**3. Final Merge**

You can now merge your feature branch back into `main`, which will be a simple "fast-forward" with no merge commit.

```bash
git checkout main
git merge new-feature
```

### Controlling an In-Progress Rebase

When a rebase is in progress, especially when it stops due to a conflict, you use a different set of flags to control the workflow.

|Command|Description|
|---|---|
|`git rebase --continue`|Resumes the rebase process after you have manually resolved a merge conflict.|
|`git rebase --abort`|Completely cancels the entire rebase operation and returns your branch to the state it was in before you started.|
|`git rebase --skip`|Skips the current commit that is causing a conflict and moves on to the next one.|

#### Workflow Demonstration

This example shows how to handle a merge conflict during a rebase.

**1. Setup: Create a history with a conflict**

We'll create two branches that modify the same line in the same file.

```bash
# Initial setup
git init
echo "Version 1" > file.txt
git add . && git commit -m "Commit A"

# Create feature branch and add a change
git checkout -b new-feature
echo "Version 2 on feature" > file.txt
git add . && git commit -m "Commit B"

# Make a conflicting change on the main branch
git checkout main
echo "Version 2 on main" > file.txt
git add . && git commit -m "Commit C"
```

**2. Attempt the rebase, which will fail**

```bash
# Attempt to rebase the feature branch onto main
git checkout new-feature
git rebase main
```

```bash
Auto-merging file.txt
CONFLICT (content): Merge conflict in file.txt
error: could not apply a1b2c3d... Commit B
hint: Resolve all conflicts manually, mark them as resolved with
hint: "git add/rm <conflicted_files>", then run "git rebase --continue".
hint: You can instead skip this commit: "git rebase --skip".
hint: To abort and get back to the state before "git rebase", run "git rebase --abort".
```

**3. Abort the rebase (Optional)**

If you get overwhelmed, you can always safely cancel the entire operation.

```bash
git rebase --abort
# The branch is now back in the state before you attempted the rebase.
```

**4. Resolve the conflict and continue**

Let's try the rebase again. When it fails, we will fix the conflict.

```bash
# Start the rebase again
git rebase main

# 1. Open the conflicted file. It will look like this:
# <<<<<<< HEAD
# Version 2 on main
# =======
# Version 2 on feature
# >>>>>>> Commit B

# 2. Manually edit the file to be how you want it, removing the markers:
# A final, resolved version

# 3. Add the resolved file to mark the conflict as handled
git add file.txt

# 4. Continue the rebase
git rebase --continue
# Successfully rebased and updated refs/heads/new-feature.
```

## Part 6: Cleaning Up History (`git rebase -i`)

**Interactive Rebase** is the most powerful tool for cleaning up your _local_ commit history _before_ you push it to a remote. It allows you to reorder, edit, combine, and reword your commits.

**Workflow Example (Squashing Commits):**

1. You've made several messy commits on your feature branch: "WIP", "Fix typo", "Add feature".
2. Before merging, you want to combine them into one clean commit.
3. Run `git rebase -i HEAD~3` to interactively rebase the last 3 commits.
4. Your editor will open with a file like this:

```bash
pick a1b2c3d Add feature
pick e4f5g6h Fix typo
pick i7j8k9l WIP
```

5. Change `pick` to `s` (for `squash`) for the commits you want to merge into the one above them:

```bash
pick a1b2c3d Add feature
s e4f5g6h Fix typo
s i7j8k9l WIP
```

6. Save and close the file. A new editor window will open, allowing you to write a single, clean commit message for the combined commit.

|Rebase Command|Action|
|---|---|
|`pick` (p)|Use the commit as-is.|
|`reword` (r)|Use the commit, but pause to let you edit the commit message.|
|`edit` (e)|Use the commit, but pause to let you amend the changes (e.g., add more changes, split the commit).|
|`squash` (s)|**Combine** this commit with the one above it. Git will combine the commit messages.|
|`fixup` (f)|Like `squash`, but it **discards** this commit's message entirely.|
