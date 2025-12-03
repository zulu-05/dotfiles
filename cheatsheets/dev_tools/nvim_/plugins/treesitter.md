# Cheatsheet: nvim-treesitter

**Treesitter** is an incremental parsing system. Unlike standard syntax highlighting, which uses Regular Expressions (Regex) to guess what code looks like, Treesitter builds a real-time Abstract Syntax Tree (AST) of the code.

This allows for:
1. **Superior Highlighting:** It understands the difference between a variable definition, a function call, and a keyword, even in complex nested structures.
2. **Smart Indentation:** It calculates indentation based on code structure rather than guessing based on the previous line.
3. **Structural Selection:** Plugins can use it to "select current function" or "swap arguments."

In this environment, the configuration is located at:
`config/nvim/lua/user/plugins/config/treesitter.lua`

## 1. Managing Parsers

Although the configuration handles most installations automatically, manual intervention is sometimes require to keep parsers up to date or to add one-off languages.

| Command | Description |
| :--- | :--- |
| `:TSUpdate` | **Update All.** Updates all currently installed parsers to their latest versions. Run this periodically or if highlighting looks "broken" after a Neovim update. |
| `:TSInstall <lang>` | **Install Single.** Manually installs a specific language parser (e.g., `:TSInstall go`). |
| `:TSInstallInfo` | **Status Check.** Lists all available parsers and puts a checkmark next to the ones currently installed. |
| `:TSModuleInfo` | Shows which Treesitter modules (highlight, indent, etc.) are active for the current buffer. |

## 2. Installed Languages

The configuration ensure the following language parsers are always installed.

**Core & Config**
*   `bash`, `powershell`, `tmux`, `dockerfile`
*   `git_config`, `git_rebase`, `gitignore`
*   `json`, `vim`, `lua`

**Application Development**
*   `python`, `rust`, `c`, `cpp`, `java`, `swift`

**Web Development**
*   `html`, `css`, `javascript`, `typescript`
*   `svelte`, `vue`, `http`

**Documentation**
* `markdown`, `markdown_inline`, `latex`

## 3. Configuration Features

### Auto-Installation
The setting `auto_install = true` is enabled in `treesitter.lua`.
*  **Behaviour:** If a file type is opened that is *not* in the list above, Treesitter will attempt to automatically download and compile the parser for that language immediately.

### Smart Indentation
The setting `indent = { enable = true }` is enabled.
*  **Behaviour:** Neovim's standard `=` operator (re-indent) now uses the Treesitter syntax tree to calculate perfect indentation for supported languages, replacing the older regex-based `indentexpr`.

### Syntax Highlighting
The setting `highlight = { enable = true }` is enabled.
*  **Behaviour:** This overrides standard Vim syntax files. Note that for very large files, Treesitter may automatically disable itself to prevent lag, falling back to standard regex highlighting.
