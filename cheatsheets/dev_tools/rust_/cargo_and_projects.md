# Rust: Cargo & Projects

This guide focuses on `cargo`, the official package manager and build system for Rust. It handles the entire project lifecycle, from scaffolding to release.

## 1. The Mental Model

A standard Rust project follows a strict convention managed by two key files:

*   **`Cargo.toml` (The Manifest):** This is the human-readable configuration file. It defines the project metadata (name, version) and its direct dependencies. It is equivalent to `package.json` in Node.js.
*   **`Cargo.lock` (The Snapshot):** This file is machine-generated. It records the exact version of every direct and transitive dependency used in the last successful build. It ensures reproducibility across different machines.

### Standard Directory Structure
Cargo enforces a specific layout so that configuration is minimised.

```text
├── Cargo.toml      # Configuration
├── Cargo.lock      # Dependency snapshot (appears after first build)
├── src/
│   └── main.rs     # Entry point for Binaries
│   └── lib.rs      # Entry point for Libraries
└── target/         # Compiled artifacts (ignored by git)
```

---

## 2. Command Reference

| Command | Action | Description |
| :--- | :--- | :--- |
| `cargo new <name>` | **Scaffold** | Creates a new directory with a valid project structure. |
| `cargo init` | **Initialise** | Converts the *current* directory into a Cargo project. |
| `cargo check` | **Validate** | Verifying the code compiles without producing an executable (Fast). |
| `cargo build` | **Compile** | Compiles the code into the `target/debug` directory. |
| `cargo run` | **Execute** | Compiles and immediately runs the binary. |
| `cargo add <crate>` | **Install** | Downloads a library from crates.io and adds it to `Cargo.toml`. |
| `cargo tree` | **Inspect** | Displays a tree visualisation of the dependency graph. |
| `cargo clean` | **Reset** | Deletes the `target/` directory to free space or force a rebuild. |

---

## 3. Workflow A: New Project Initialisation

**Scenario:** You are starting a new project. You must decide if it is a **Binary** (an executable application) or a **Library** (code to be shared/imported by others).

### Option 1: Binary Application
Use this for CLI tools, servers, or games.

*   **Flag:** `--bin` (Default behaviour).
*   **Entry Point:** `src/main.rs`.

```bash
$ cargo new my-cli-tool
# Created binary (application) `my-cli-tool` package
```

### Option 2: Shared Library
Use this for helper logic or parsing engines.

*   **Flag:** `--lib`.
*   **Entry Point:** `src/lib.rs`.

```bash
$ cargo new my-parser --lib
# Created library `my-parser` package
```

---

## 4. Workflow B: The Build Loop

**Concept:** Rust compilation involves complex optimisation via LLVM, which can be slow. To maintain flow, developers use different commands for development versus deployment.

### 1. The "Check" Loop (Development)
While writing code, you only care if your syntax is correct and types match. Use `check`. It skips the final code generation step, making it much faster than a full build.

```bash
$ cargo check
# Output:
#     Checking my-cli-tool v0.1.0
#         Finished dev [unoptimized + debuginfo] target(s) in 0.22s
```

### 2. The "Run" Loop (Testing)
To see your program run. This compiles in **Debug Mode** (unoptimised, with debug symbols).

```bash
$ cargo run
# Output: Hello, world!
```

### 3. The "Release" Build (Deployment)
When ready to ship, compile with optimisations. This takes longer but produces a fast binary.

```bash
# --release: Enables heavy optimisations and strips debug info
$ cargo build --release
# Output:
#     Compiling my-cli-tool v0.1.0
#         Finished release [optimized] target(s) in 1.45s

# The binary is located at: target/release/my-cli-tool
```

## 5. Workflow C: Dependency Management

**Scenario:** You want to add JSON serialisation to your project using the popular `serde` crate.

### Step 1: Add the Dependency
Use `cargo add`. You can specify "features" (optional parts of the library) in the same command.

```bash
$ cargo add serde --features derive
# Output:
#     Updating crates.io index
#         Adding serde v1.0.193 to dependencies
#             Features:
#             + derive
```

### Step 2: Inspection
You noticed that `serde` pulled in other dependencies. Use `tree` to understand why.

```bash
$ cargo tree
# Output:
# my-cli-tool v0.1.0 (/path/to/project)
# └── serde v1.0.193
#     └── serde_derive v1.0.193 (proc-macro)
#         ├── proc-macro2 v1.0.70
#         ├── quote v1.0.33
#         └── syn v2.0.41
```
