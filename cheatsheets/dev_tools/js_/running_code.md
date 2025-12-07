# Node.js: Running Code & Scripts

This guide focuses on the various way to execute JavaScript within the Node ecosystem: direct execution, project scripts, and temporary binary execution.

## 1. The Mental Model

While it is possible to run a file directly using `node index.js`, strictly adhering to this practice is discouraged for professional projects.

*   **The Problem:** Real applications often require environment variables, specific flags, or pre-processing (like TypeScript compilation) before they can run.
*   **The Solution:** The `scripts` section of `package.json`. This acts as the public interface for the project. It abstracts *how* the code runs (the implementation details) from the command used to run it.
*   **The Path:** Uniquely, when a command is run via `npm run`, Node automatically adds `node_modules/.bin` to the `$PATH`. This allos tools like `jest` or `tsc` to be run by name without needing to specify their full path.

---

## 2. Command Reference

| Command | Action | Description |
| :--- | :--- | :--- |
| `node <file>` | **Direct** | Runs a specific JavaScript file immediately. |
| `npm start` | **Lifecycle** | A shortcut for `npm run start`. Usually launches the production server. |
| `npm test` | **Lifecycle** | A shortcut for `npm run test`. Runs the test suite. |
| `npm run <name>` | **Script** | Executs a named script defined in `package.json`. |
| `npx <pkg>` | **Execute** | Downloads and runs a binary from the npm registry without installing it globally. |

---

## 3. Workflow A: The Script Runner

**Scenario:** You have a TypeScript project. To run it, you must first compile the code using `tsc`, then run the output file `dist/index.js`. Typing these commands every time is tedious and error-prone.

### Step 1: Define the Script
Open `package.json` and locate the `"scripts"` object. Define a new command named `build`.

```json
{
    "name": "my-project",
    "scripts": {
        "start": "node dist/index.js",
        "build": "tsc"
    }
}

### Step 2: Execute
Run the script using the name you defined.

```bash
$ npm run build
```

### Why this is better
1. **Abstraction:** You don't need to remember *which* compiler flags are used; you just know you need to "build".
2. **Context:** `npm` found the `tsc` binary inside `node_modules/.bin/`. If you tried to run `tsc` directly in your terminal, it would fail unless you had installed TypeScript globally.

---

## 4. Workflow B: The `npx` Execution

**Scenario:** You want to use a CLI tool once, such as `create-react-app` to scaffold a project, or `cosway` for a joke. You do not want to clutter your system by installing these tools permanently with `npm install -g`.

**Concept:** `npx` (Node Package Execute) checks if the package is installed locally. If not, it downloads the package to a temporary cache, runs it, and then clears it.

### Step 1: Run without Installing
Execute the package directly by name.

```bash
$ npx cowsay "Hello from a temporary binary!"

# Output:
#  ______________________________
# < Hello from a temporary binary! >
#  ------------------------------
#         \   ^__^
#          \  (oo)\_______
#             (__)\       )\/\
#                 ||----w |
#                 ||     ||
```

### Step 2: Verify System Hygiene
Check if the package was installed globally. It will not be there.

```bash
$ npm list -g cowsay
# Output: (empty)
```

---

## 5. Workflow C: The REPL

**Scenario:** You want to quickly test a snippet of JavaScript logic (like a regex match or a math calculation) without creating a file.

### Step 1: Enter Interactive Mode
Type `node` without arguments.

```bash
$ node
# Welcome to Node.js v18.16.0.
# Type ".help" for more information.
>
```

### Step 2: Experiment
Type JavaScript code directly.

```bash
> const name = "Developer"
> `Hello, ${name.toUpperCase()}`
'Hello, DEVELOPER'
```

### Step 3: Exit
Press `Ctrl+C` twice or type `.exit`.
