# Node.js: Installation & Version Management

This guide focuses on manging the Node.js runtime environment. It explains why system-level package managers are avoided in favour of version managers like `nvm`.

## 1. The Mental Model

Using `apt install nodejs` (or the equivalent on macOS/Windows) is generally considered an anti-pattern for professional development.

*   **The Versioning Problem:** System repositories often contain outdated versions of Node.js. Furthermore, one project might require Node 14 (legacy), while another requires Node 20 (modern). A single system-wide installation cannot satisfy both simultaneously.
*   **The Permissions Problem:** System installations are owned by `root`. This forces the use of `sudo` when installing global packages, which creates security risks and file ownership conflicts.
*   **The Solution:** `nvm` (Node Version Manager). It installs multiple versions of Node.js inside the user's home directory. This allows switching versions instantly without administrator privileges.

---

## 2. Command Reference

| Command | Action | Description |
| :--- | :--- | :--- |
| `nvm install <ver>` | **Install** | Downloads and installs a specific version (e.g., `18`, `20.10.0`, `--lts`). |
| `nvm use <ver>` | **Activate** | Switches the current shell session to the specified version. |
| `nvm ls` | **List Local** | Shows all versions currently installed on the machine. |
| `nvm ls-remote` | **List Remote** | Lists all versions available for download from the official registry. |
| `nvm alias default <ver>` | **Set Default** | Sets the version that `nvm` uses automatically when a new terminal is opened. |
| `nvm which current` | **Locate** | Shows the path to the currently active Node executable. |

---

## 3. Workflow A: Installing & Switching

**Scenario:** You normally use the latest stable version (LTS), but you need to fix a bug in a legacy application that only runs on Node 14.

### Step 1: Install the LTS (Long Term Support)
Install the current industry-standard version. This should be your daily driver.

```bash
$ nvm install --lts
# Output: Now using node v20.11.0 (npm v10.2.4)
```

### Step 2: Install the Legacy Version
Install the specific older version required for the bug fix.

```bash
$ nvm install 14
# Output: Now using node v14.21.3 (npm v6.14.18)
```

### Step 3: Switch Contexts
Verify that your environment has changed. Note that the `npm` version changes alongside the `node` version.

```bash
$ node -v
# v14.21.3

$ nvm use --lts
# Now using node v20.11.0

$ node -v
# v20.11.0
```

---

## 4. Workflow B: Project-Specific Versions

**Scenario:** You are working on a team project. You want to ensure every developer uses the exact same Node version to avoid "it works on my machine" issues.

### Step 1: Create the Config File
Create a file named `.nvmrc` in the project root containing just the version number.

```bash
$ echo "18.16.0" > .nvmrc
```

### Step 2: Automate the Switch
When you enter the directory, tell `nvm` to use the version specified in the file. (If you don't have it installed, `nvm` will tell you).

```bash
$ cd my-project
$ nvm use
# Output: Found '/path/to/my-project/.nvmrc' with version <18.16.0>
# Now using node v18.16.0 (npm v9.5.1)
```

---

## 5. Workflow C: Global Tools
**Scenario:** You need a CLI tool like `typescript`, `yarn`, or `nodemon` available everywhere in your terminal, not just inside a specific project.

**Concept:** When using `nvm`, "Global" packages are not truly system-wide. They are installed into the `lib` folder of the **currently active** Node version.

### Step 1: Install Globally
Use the `-g` flag. Note that you do **not** need `sudo` because `nvm` owns the directory.

```bash
$ npm install -g typescript
# Output: added 1 package in 2s
```

### Step 2: Verification
Check where the binary is located. It will be deep inside the `.nvm` directory.

```bash
$ which tsc
# /home/user/.nvm/versions/node/v20.11.0/bin/tsc
```

### Critical Warning
If you install `typescript` while using Node 20, and then switch to Node 14 (`nvm use 14`), `tsc` will stop working or disappear. You must re-install global tools for each Node version you use regularly.
