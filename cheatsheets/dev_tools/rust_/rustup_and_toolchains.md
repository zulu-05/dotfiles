# Rust: Toolchains & Installation

This guide focuses on the management of the Rust environment itself. Unlike many languages that rely on system package managers, Rust provides its own first-party tool, `rustup`, to manage installations.

## 1. The Mental Model

To maintain a healthy Rust environment, the distinction between the installer and the compiler must be understood.

*   **`rustc` (The Compiler):** This binary turns Rust code into machine code. It is strict, efficient, and released on a rapid six-week cycle.
*   **`rustup` (The Manager):** This is the "multiplexer." It installs `rustc`, manages standard libraries, and handles cross-compilation targets. Because Rust updates so frequently, `rustup` is essential for keeping the toolchain current without breaking system dependencies.
*   **Toolchains:** A "toolchain" is a complete installation of the compiler, the standard library, and associated binaries (like `cargo`) for a specified release channel (stable, beta, or nightly).

---

## 2. Command Reference

| Command | Action | Description |
| :--- | :--- | :--- |
| `rustup update` | **Upgrade** | Updates all installed toolchains to the latest versions. |
| `rustup default <chain>` | **Switch** | Sets the global default toolchain (e.g., `stable`, `nightly`, `1.70.0`). |
| `rustup show` | **Status** | Shows the active toolchain and version information for the current directory. |
| `rustup component add` | **Extend** | Installs auxiliary tools like `rust-analyzer`, `clippy`, or `rustfmt`. |
| `rustup target add` | **Cross-Compile** | Installs standard library versions for different architectures (e.g., WebAssembly). |
| `rustup doc` | **Learn** | Opens the offline HTML documentation for the standard library. |

---

## 3. Workflow A: The Update Cycle

**Scenario:** A new version of Rust has been released (which happens every six weeks). You want to upgrade your compiler to access new language features.

### Step 1: Run the Update
Execute the update command. `rustup` will download the new binaries for the `stable` channel and any other channels you have installed (like `nightly`).

```bash
$ rustup updated
# Output:
# info: syncing channel updates for 'stable-x86_65-unknown-linux-gnu'
# ...
# stable-x86_64-unknown-linux-gnu updated - rustc 1.75.0 (82e1608df 2023-12-21)
```

### Step 2: Verify Version
Confirm that the active compiler is the new version.

```bash
$ rustc --version
# rustc 1.75.0 (82e1608df 2023-12-21)
```

---

## 4. Workflow B: Living on the Edge (Nightly)

**Scenario:** You want to test a cutting-edge feature (like experimental async traits) that hasn't landed in the stable release yet.

**Concept:** Rust has three channels:

*   **Stable:** Production-ready.
*   **Beta:** The testing ground for the next Stable release.
*   **Nightly:** Built every night. Allows usage of `#![feature(...)]` flags to opt-in to experimental syntax.

### Step 1: Install Nightly
Install the toolchain without making it your system default.

```bash
$ rustup toolchain install nightly
```

### Step 2: Run a Command with Nightly
You do not need to switch your global default to run nightly code. Use the `+<toolchain>` override syntax with `cargo`.

```bash
# Runs 'cargo build' using the nightly compiler, just for this command
$ cargo +nightly build
```

### Step 3: Set Directory Override (Optional)
If a specific project *requires* nightly, set an override just for that folder. This creates a `rust-toolchain.toml` file or an internal override.

```bash
$ cd my-experimental-project
$ rustup override set nightly
```

---

## 5. Workflow C: Cross-Compilation Targets

**Scenario:** You are developing on a Linux machine (x86_64), but you want to compile your code into WebAssembly (Wasm) to run it in a browser.

**Concept:** By default, `rustc` only knows how to compile for the host machine. To compile for other architectures, the standard library for that specific "Target" must be downloaded.

### Step 1: List Targets
View available targets. Installed ones are marked `(installed)`.

```bash
$ rustup target list
# ...
# wasm32-unknown-unknown
# x86_64-pc-windows-gnu
# ...
```

### Step 2: Add the Target
Download the standard library for WebAssembly.

```bash
$ rustup target add wasm32-unknown-unknown
# Output:
# info: downloading component 'rust-std' for 'wasm32-unknown-unknown'
```

### Step 3: Build for Target
Tell `cargo` to build for the new architecture using the `--target` flag.

```bash
$ cargo build --target wasm32-unknown-unknown
# Output:
#     Compiling my-project v0.1.0 ...
#         Finished dev [unoptimized + debuginfo] target(s) in 0.52s
```
