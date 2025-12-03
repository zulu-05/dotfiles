# Cheatsheet: Telescope (Fuzzy Finder)

Telescope is a highly extensible fuzzy finder over lists. While mostly used for finding files, it is technically a modal interface that can filter any list (git commits, help tags, open buffers, etc.) based on fuzzy string matching.

## The Core Concept: "Fuzzy" Matching

Telescope allows you to type characters that appear *anywhere* in the string, not just the beginning.

* **Strict Search:** Searching for `nvim` only matches files starting with `nvim...`.
* **Fuzzy Search:** Searching for `nvc` will match **nv**im/**c**onfig.

## Global Keymaps (This Environment)

In this configuration (`config/nvim/lua/user/plugins/config/telescope.lua`), the following keys are mapped to the standard Telescope built-in functions. The **Leader Key** is set to `<Space>`.

| Keymap | Function | Mnemonic | Usage Scenario |
| :--- | :--- | :--- | :--- |
| `<Space>ff` | `find_files` | **F**ind **F**iles | **Filename Search.** The default way to open files. It scans the current directory but ignores hidden files and `.gitignore` patterns (e.g. `node_modules/`, `.venv/`). |
| `<Space>fg` | `live_grep` | **F**ind **G**rep | **Content Search.** Searches for *text inside* every file in the project. Requires `ripgrep` installed on the system. |
| `<Space>gf` | `git_files` | **G**it **F**iles | **Context Aware.** Like `find_files`, but strictly limits the search to files tracked by Git. Useful in massive repos to filter out build artifacts. |
| `<Space>fb` | `buffers` | **F**ind **B**uffers | **Tab Switcher.** Lists only the files you currently have open in Neovim. Use this to switch contexts quickly. |

## Workflow Examples

### 1. The "Filename" Workflow (`<Space>ff`)
Use this when you know **what** the file is named, but not where it is located.

* **Goal:** Open `config/nvim/lua/user/core/keymaps.lua`.
* **Action:**
  1. Press `<Space>ff`.
  2. Type `keylua`.
  3. Telescope filters the list down to `keymaps.lua`.
  4. Press `<Enter>`.

### 2. The "Content" Workflow (`<Space>fg`)
Use this when you know **code** functionality, but not which file contains it.

* **Goal:** Find where the `mkvenv` alias is defined.
* **Action:**
  1. Press `<Space>fg`.
  2. Type `alias mkvenv`.
  3. Telescope shows a preview of `30-aliases.sh` or `60-python.sh` (wherever the text exists).
  4. Press `<Enter>` to jump exactly to that line of code.

## Navigation & Interface

When the Telescope window opens, you are placed in **Insert Mode** to start typing your query immediately.

| Key | Action | Note |
| :--- | :--- | :--- |
| `<Ctrl-n>` | Selection Down | Standard Neovim list navigation. |
| `<Ctrl-p>` | Selection Up | Standard Neovim list navigation. |
| `<Enter>` | Confirm | Opens the selected item. |
| `<Ctrl-c>` | Close | Closes Telescope from Insert Mode. |
| `<Esc>` | Normal Mode | Switches Telescope to Normal Mode (allows `j`/`k` navigation). |
| `jk` | Normal Mode | **(Custom)** Uses this setup's global "Fast Escape" to exit typing mode. |

## Troubleshooting

* **"Live Grep" isn't working:** This function relies on an external system tool called `ripgrep` (`rg`). If typing in the prompt returns no results, ensure `ripgrep` is installed on your OS.
* **Hidden Files:** By default, `find_files` respects `.gitignore`. If you need to find a file inside `.git/` or a simplified `.env`, they may not appear unless you use specific flags or commands (not mapped by default in this config).
