# Cheatsheet: Colour Schemes & Theming

Neovim separates the logic of **Syntax Highlighting** (identifying what is a variable versus a string) from "Colour Schemes** (aassigning specific hex codes to those identifiers).

In this environment, the active theme is configured in:
`config/nvim/lua/user/plugins/config/gruvbox.lua`

## 1. Core Commands

Neovim allows themes to be switched on the fly without restarting the editor.

| Command | Description |
| :--- | :--- |
| `:colorscheme [name]` | **Switch Theme.** Sets the active colour scheme. Press `<Tab>` after typing the space to cycle through all installed themes. |
| `:colorscheme` | **Check Status.** Typing the command without arguments prints the name of the currently active theme. |
| `:set background=dark` | **Dark Mode.** Tells the theme to use its dark palette. |
| `:set background=light` | **Light Mode.** Tells the theme to use its light palette. |

## 2. The Installed Theme: Gruvbox

The currently installed external theme is **Gruvbox**. It is a "Retro Groove" scheme known for its specific pastel palette.

### Configuration Style: Global Variables
Older or simpler themes like Gruvbox often use global Vim variables for configuration. These must be set **before** the `colorscheme` command is run.

**Example Override (in `config/gruvbox.lua`):**
```lua
-- Set contrast to 'hard', 'medium' (default), or 'soft'
vim.g.gruvbox_contrast_dark = "hard"

-- Apply the theme
vim.cmd("colorscheme gruvbox")
```

## 3. Handling Modern Lua Themes (Examples)

While Gruvbox uses global variables, many newer themes (like `tokyonight.nvim`, `catppuccin`, or `kanagawa`) use a Lua `setup({})` function. If you install one of these in the future, the configuration pattern changes slightly.

**Example (Hypothetical `tokyonight` config):**
```lua
-- Modern themes often require a setup call to change options
require("tokyonight").setup({
    style = "storm", -- specific style options
    transparent = true,
    terminal_colors = true,
})

vim.cmd("colorscheme tokyonight")
```

## 4. Built-in Themes

Neovim comes with several themes pre-installed which are always available, even if your plugin manager breaks.

* `default`: The standard, high-contrast theme.
* `habamax`: A popular high-contrast, accessibility-focused dark theme.
* `lunaperch`: A minimal, modern dark theme included in Neovim 0.10+.
* `quiet`: A low-contrast light theme.

**Troubleshooting Workflow:**
If an external theme causes errors, revert to a built-in one to regain usability:
1. Run `:colorscheme habamax`
2. Debug the configuration.
