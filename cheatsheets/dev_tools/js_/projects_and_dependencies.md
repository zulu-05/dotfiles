# Node.js: Projects & Dependencies

This guide focuses on the specific architecture of Node.js projects: the manifest (`package.json`), the storage (`node_modules`), and the manager (`npm`).

## 1. The Mental Model

To manage a Node.js project effectively, it is necessary to unlearn some Python habits.

*   **No Virtual Environments::** Unlike Python, which requires creating a specific `venv` to avoid global conflicts, Node.js isolates dependencies by default. Every project has its own `node_modules` directory containing the libraries it needs. The runtime looks in the local folder first, never the system global folder (unless explicitly told to).
*   **The Manifest (`package.json`):** This file defines the project identity and lists the dependencies (e.g., "I need React version 18 or higher"). It is human-readable and editable.
*   **The Lockfile (`package-lock.json`):** This file is machine-generated and describes the *exact* tree of dependencies currently installed (e.g., "I installed React 18.2.0, which pulled in scheduler 0.23.0"). It ensures that every developer on the team has the exact same bytes on their disk.

---

## 2. Command Reference

| Command | Alias | Action |
| :--- | :--- | :--- |
| `npm init -y` | | **Initialise.** Creates a `package.json` with default settings (skips the questionnaire). |
| `npm install <pkg>` | `npm i` | **Add.** Downloads a package and adds it to `dependencies`. |
| `npm install` | `npm i` | **Hydrate.** Installs all dependencies listed in `package.json` (used after cloning). |
| `npm uninstall <pkg>` | `npm un` | **Remove.** Deletes the package and removes it from the manifest. |
| `npm update` | | **Upgrade.** Updates packages to the latest versions allowed by the semvver range in `package.json`. |
| `npm outdated` | | **Check.** Lists packages that have newer versions available. |
| `npm audit` | | **Security.** Scans the dependency tree for known security vulnerabilities. |

---

## 3. Workflow A: New Project Setup

**Scenario:** You are starting a fresh project and want to install a utility library like `lodash`.

### 1. Initialise
Create a directory and generate the manifest.

```bash
$ mkdir my-node-app && cd my-node-app
$ npm init -y
# Output: Wrote to .../my-node-app/package.json
```

### 2. Install a Library
Install `lodash`. NPM downloads it from the registry and places it in the local storage.

```bash
$ npm install lodash
# Output:
# added 1 package, and audited 2 packages in 1s
```

### 3. Inspect
Verify the structure. You will see that `package.json` was modified, `package-lock.json` was created, and the code lives in `node_modules`.

```bash
$ ls -F
node_modules/   package-lock.json   package.json
```

---

## 4. Workflow B: Dependency Types (The Critical Distinction)

Node.js strictly separates libraries required to *run* the code from tools required to *write* it.

*   **`dependencies`:** Libraries the code imports at runtime (e.g., `express`, `react`, `lodash`).
*   **`devDependencies`:** Tools used during development, testing, or building (e.g., `jest`, `typescript`, `eslint`).

**Scenario:** You have installed `lodash` (for runtime). Now you need `jest` to run tests.

### 1. Install as Dev Dependency
Use the `--save-dev` (or `-D`) flag.

```bash
$ npm install -D jest
```

### 2. Verify Placement
Open `package.json` to confirm the separation. This ensures that when you deploy to production, you don't install heavy testing tools.

```json
{
    "dependencies": {
        "lodash": "^4.17.21"
    },
    "devDependencies": {
        "jest": "^29.7.0"
    }
}
```

---

## 5. Workflow C: Reproducible Installs (CI/CD)

**Scenario:** You have cloned a team member's repository, or a CI/CD pipeline is running a build. You need to ensure the environment is *identical* to the original developer's.

**The Risk:** Running `npm install` might update `package-lock.json` if it notices a newer minor version of a dependency is available. This can cause "works on my machine" bugs.

### The Solution: Clean Install (`npm ci`)
Instead of `install`, use the `ci` command.

1. It deletes the existing `node_modules` folder.
2. It installs the *exact* versions specified in `package-lock.json`.
3. It errors out if `package.json` and `package-lock.json` are out of sync.

```bash
# 1. Clone th repo
$ git clone <url>
$ cd <repo>

# 2. Install strictly from the lockfile
$ npm ci
# Output:
# added 500 packages in 2s
```
