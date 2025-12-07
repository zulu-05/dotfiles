# Node.js: Modules & Asynchrony

This guide focuses on the two pillars of Node.js code structure: the module system (how files talk to each other) and the event loop (how code waits for operations to finish).

## 1. The Mental Model (The Dual System)

Node.js is currently in a transition period between two distinct module systems.

*   **CommonJS (CJS):** The legacy, synchronous system used by Node since its inception. It uses `require()` and `module.exports`. If you see a `.js` file without configuration, Node assumes it is CommonJS.
*   **ES Modules (ESM):** The modern, asynchronous standard shared with browsers. It uses `import` and `export`. This is the future of the ecosystem.

### Configuring the Project
By default, Node treats `.js` files as CommonJS. To use modern syntax, the project must explicitly opt-in.

Open `package.json` and add the "type" field:

```json
{
    "name": "my-project",
    "version": "1.0.0",
    "type": "module"
}
```

*Now, all `.js` file in this project are treated as ES Modules.*

---

## 2. Workflow A: CommonJS (Legacy)

**Scenario:** You are writing a quick utility script, or working in an older codebase that hasn't been migrated.

### Step 1: Exporting Logic

In `utils.js`, attach functions to the `module.exports` object.

```javascript
// utils.js
function add(a, b) {
    return a + b;
}

// You can export a single object or function
module.exports = { add };
```

### Step 2: Importing Logic
In `index.js`, use `require()` to load the module synchronously.

```javascript
// index.js
const { add } = require('./utils');

console.log(add(2, 2)); // Output: 4
```

---

## 3. Workflow B: ES Modules (Modern)

**Scenario:** You are building a new application and want to use modern syntax that is compatible with frontend frameworks like React or Vue. **Ensure** `"type": "module"` **is set in** `package.json`.

### Step 1: Exporting Logic
In `utils.js`, use the `export` keyword.

```javascript
// utils.js

// Named Export (Preferred)
export function add(a, b) {
    return a + b;
}

// Default Export
export default function log(msg) {
    console.log(msg);
}

### Step 2: Importing Logic
In `index.js`, use `import`. Note that in Node.js (unlike bundlers like Webpack), you **must include the file extension**.

```javascript
// index.js
import log, { add } from './utils.js'; // Note the .js extension

log(add(5, 5)); // Output: 10
```

---

## 4. The Async/Await Pattern

Node.js is single-threaded and non-blocking. Heavy operations (like reading files or network requests) do not stop the code; they return a **Promise**. To handle this cleanly without "callback hell," the `async/await` syntax is used.

**Key Rule:** You can only use `await` inside a function marked `async` (or at the top level of an ES Module).

### The Standard Boilerplate
Use this pattern for robust I/O operations. It ensures that the code pauses until the operation is finished, and any errors are caught gracefully.

```javascript
import fs from 'node:fs/promises'; // Use the promise-based version of standard libraries

async function main() {
    try {
        // 1. Await the result. The code pauses here.
        console.log("Reading file...");
        const data = await fs.readFile('./data.txt', 'utf-8');

        // 2. Process the data
        console.log("File content:", data);

    } catch (error) {
        // 3. Handle errors (e.g., file not found)
        console.error("Critical Error:", error.message);
```
