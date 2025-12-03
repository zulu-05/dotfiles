# Cheatsheet: Gruvbox Theme

**Gruvbox** is a retro groove colour scheme designed for easy viewing. It relies on a specific palette of pastel colours that are distinct but low-contrast enough to prevent eye strain during long coding sessions.

In this environment, the configuration is located at:
`config/nvim/lua/user/plugins/config/gruvbox.lua`

## 1. Configuration Status

The current configuration is **minimal**. It loads the colourscheme without any specific overrides (such as forced transparency or hard contrast). This means it relies on the plugin's defaults and the global Neovim options.

## 2. Switching Modes (Light/Dark)

Gruvbox supports both light and dark modes natively. Neovim controls this via the global `background` option, not a specific plugin command.

| Command | Description |
| :--- | :--- |
| `:set background=light` | **Light Mode.** Switches the palette to the light variation (cream background). |
| `:set background=dark` | **Dark Mode.** Switches the palette to the dark variation (standard coding look). |

To make a permanent change to the default mode, edit `config/nvim/lua/user/core/options.lua` (where global settings usually live) and add `vim.opt.background = "light"`.

## 3. Contrast Settings

Although not currently configured in `gruvbox.lua`, the contrast can be adjusted by setting global variables *before* the colour scheme loads.

If strictly "Hard" (blacker background) or "Soft" (greyer background) contrast is preferred, modify `config/nvim/lua/user/plugins/config/gruvbox.lua` to include these variables before the `colorscheme` command:

```lua
-- Optional overrides (add these before vim.cmd)
vim.g.gruvbox_contrast_dark = "hard" -- Options: "soft", "medium", "hard"
vim.g.gruvbox_contrast_light = "hard"

vim.cmd("colorscheme gruvbox")
```
