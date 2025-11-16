# Neovim Configuration

This directory contains the complete, modular configuration for Neovim, built with Lua. It is designed to be fast, extensible, and easy to maintain, mirroring the service-oriented philosophy of the parent dotfiles project.

***

## ✨ Features

*   **Modern & Fast**: Fully written in Lua. Plugins are lazy-loaded where possible to ensure near-instant startup times.
*   **Plugin Management**: Handled by the excellent `packer.nvim`.
*   **Fuzzy Finding**: Powered by `telescope.nvim` for lightning-fast file navigation, live grepping, and more.
*   **Superior Syntax Highlighting**: Uses `nvim-treesitter` for more accurate and detailed code highlighting.
*   **Rich Markdown Toolkit**:
    *   **Live Browser Preview**: Accurate, real-time preview of Markdown files in your browser (`:MarkdownPreview`).
    *   **Terminal Preview**: Fast, beautiful in-editor preview for quick reading (`:Glow`).
    *   **Aesthetic Writing**: In-place syntax concealing makes writing Markdown a pleasure (`headlines.nvim`).
*   **Theming**: Comes with the popular `gruvbox` colorscheme.

***

## 📋 Prerequisites

For all features to work correctly, the following external dependencies must be installed:

*   **Neovim (v0.9+):** The core editor.
*   **`git`:** For `packer.nvim` and Telescope's git integration.
*   **`ripgrep` (`rg`):** A fast search tool required by Telescope for `live_grep`.
*   **`nodejs` & `npm`:** Required by `markdown-preview.nvim`.
*   **`glow`:** The command-line tool used by `glow.nvim`.

***

## 🚀 Installation

The main `install.sh` script in the root of the dotfiles repository handles symlinking this directory to `~/.config/nvim`.

After the first installation, you must open Neovim and run `:PackerSync` to install all the plugins.

***

## ⌨️ Key Mappings

The leader key is set to `Space`.

### General

| Keymap | Action |
| :--- | :--- |
| `jk` | Exit Insert Mode (in Insert Mode) |

### Telescope (Fuzzy Finder)

| Keymap | Action |
| :--- | :--- |
| `<leader>ff` | Find Files in the current directory |
| `<leader>fg` | Find text using Live Grep in the current directory |
| `<leader>gf` | Find Files in the current Git repository |
| `<leader>fb` | Find currently open Buffers |

### Markdown Plugins

| Command | Action |
| :--- | :--- |
| `:MarkdownPreview` | Open a live preview in your web browser. |
| `:Glow` | Open a rendered preview in a floating terminal window. |

***

## 📂 Directory Structure

This configuration uses a modular structure to keep files organized and maintainable. All custom configuration lives within the `lua/user/` directory.

*   `init.lua`: The main entrypoint. Its only job is to load the other modules.
*   `lua/user/core/`: For core editor settings (options, keymaps) that don't depend on plugins.
*   `lua/user/plugins/init.lua`: The central Packer file where all plugins are declared.
*   `lua/user/plugins/config/`: Contains a separate Lua file for each plugin's specific configuration. This makes it easy to add, remove, or modify plugin settings in isolation.
