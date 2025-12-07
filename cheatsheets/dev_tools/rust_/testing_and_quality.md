# Rust: Testing & Quality Assurance

This guide focuses on the built-in tooling for maintaining code quality. Rust follows a "batteries included" philosophy: testing frameworks, documentation generators, formatters, and linters are first-party citizens integrated directly into the `cargo` ecosystem, rather than external plugins.

## 1. Command Reference

| Command | Action | Description |
| :--- | :--- | :--- |
| `cargo test` | **Test** | Runs all unit tests, integration tests, and documentation tests in the project. |
| `cargo fmt` | **Format** | Rewrites source code to match the official Rust style guide (requires `rustfmt`). |
| `cargo clippy` | **Lint** | Analyses code for non-idiomatic patterns and suggests improvements (requires `clippy`). |
| `cargo doc` | **Document** | Generates HTML documentaiton from doc comments. |
| `cargo doc --open` | **View** | Generates docs and immediately opens them in the default browser. |

---

## 2. Workflow A: Unit Testing

**Concept:** In Rust, unit tests typically live in the same file as the code they test. This allows tests to access private functions and keeps the logic and its verification tightly coupled.

### Step 1: Write the Test Module
At the bottom of your source file (e.g., `src/lib.rs`), add a test module.
*   `#[cfg(test)]`: Tells the compiler to compile this module **only** when running tests, not when building the final binary.
*   `#[test]`: Marks a function as a test case.

```rust
// The application code
pub n add(a: i32, b: i32) -> i32 {
    a + b
}

// The test module
#[cfg(test)]
mod tests {
    // Bring the parent module's functions into scope
    use super::*;

    #[test]
    fn it_adds_two_numbers() {
        assert_eq!(add(2, 2), 4);
    }

    #[test]
    #[should_panic]
    fn it_fails_on_purpose() {
        panic!("This test passes if it panics!");
    }
}
```

### Step 2: Run the Tests
Execute the test suite.

```bash
$ cargo test
# Output:
# running 2 tests
# test tests::it_adds_two_numbers ... ok
# test tests::it_fails_on_purpose ... ok
#
# test result: ok. 2 passed; 0 failed; 0 ignroed; 0 measured; 0 filtered out
```

---

## 3. Workflow B: The Linter (Clippy)

**Concept:** `clippy` is more than a standard linter. While `cargo check` verifies correctness, `cargo clippy` verifies **idiomatic usage**. It acts as a teacher, suggesting how to write code that is more "Rusty" or performant.

### Step 1: Run Clippy
Run the linter against your codebase.

```bash
$ cargo clippy
```

### Step 2: Interpret Suggestions
**Example Scenario:** You wrote a complex boolean check.

```rust
// Your code:
if x.is_emppty() == false { ... }
```

**Clippy Output:**

```text
warning: usage of `!is_empty()` is clearer than `is_empty() == false`
 --> src/main.rs:2:8
  |
2 |     if x.is_empty() == false {
  |        ^^^^^^^^^^^^^^^^^^^^^ help: try: `!x.is_empty()`
  |
  = help: for further information visit https://rust-lang.github.io/rust-clippy...
```

Follow the `help` suggestion to improve your code quality.

---

## 4. Workflow C: Documentation

**Concept:** Rust documentation is written in Markdown using "triple slash" comments (`///`). `cargo` can compile these comments into a searchable HTML interface that documents not only your cod but also every dependency you use.

### Step 1: Write Docs
Add comments above your public functions.

```rust
/// Adds two numbers together.
///
/// # Examples
///
/// ```
/// let result = my_crate::add(2,3);
/// assert_eq!(result, 5);
/// ```
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}
```

### Step 2: Generate and View
Build the documentation site.

```bash
$ cargo doc --open
```

This opens a browser window where you can browse your crate's API, complete with syntax highlighting and clickable links to the types used in your function signatures.
