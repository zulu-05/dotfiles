# Cheatsheet: Packer (Plugin Manager)

**Packer** is a "declarative" plugin manager. This means plugins are listed in a specific file, and Packer ensures the installed software matches that list.

In this environment, the plugin registry is located at:
`config/nvim/lua/user/plugins/init.lua`

## 1. The Core Lifecycle Commands

Run these commands inside Neovim (starting with `:`) to manage the plugin ecosystem.

| Command | Description | When to Use |
| :--- | :--- | :--- |
| `:PackerSync` | **The "Do Everything" Command.** It performs an Install, Update, and Clean all at once. | Run this every time `init.lua` is edited. |
| `:PackerStatus` | Lists all installed plugins and their status (active/inactive). | Use this to verify version commits or if a plugin fails to load. |
| `:PackerClean` | Removes any plugins that are currently installed but **no longer listed** in the config file. | Run this to free up disk space after removing a plugin from the config (Included in `Sync`). |
| `:PackerCompile` | Optimises the loader code. It creates a compiled file for faster startup. | Usually runs automatically, but run this manually if a change to a `config` function is not reflecting immediately. |
| `:PackerInstall` | Installs missing plugins but does *not* update existing ones or remove unused ones. | Use this on a fresh machine to get up and running quickly. |

## 2. Workflow: Adding a New Plugin

To add a new tool to the environment (e.g., `github/copilot.vim`), follow this process:

### Step 1: Edit the Registry
Open `config/nvim/lua/user/plugins/init.lua`. Inside the `startup` function, add a new line:

```lua
-- Simple installation
use "github/copilot.vim"

-- OR: Installation with specific configuration
use {
    "windwp/nvim-autopairs",
    config = function()
        -- The architecture keeps specific configs in separate files
        require("user.plugins.config.autopairs")
    end
}
```

### Step 2: Sync
Save the file.
* **Automatic:** The configuration contains an autocommand that *attempts* to run `PackerSync` whenever this file is saved.
* **Manual:** If the auto-sync doesn't trigger, type `:PackerSync` and press Enter.

### Step 3: Verify
A floating window will appear showing the installation progress. Once it displays "Done", the plugin is ready to use.

## 3. Advanced Concepts

This configuration utilises **Lazy Loading** and **Separation of Concerns**.

### Lazy Loading (`ft`, `cmd`, `event`)
In `init.lua`, plugins are often defined with specific triggers:

```lua
use {
    "iamcco/markdown-preview.nvim",
    ft = { "markdown" }
}
```
* **Behaviour:** Neovim does **not** load this plugin into memory at startup.
* **The Trigger:** It waits until a file with the extension `.md` (markdown) is opened. This maintains a fast startup time.

### Config Separation
Instead of containing setup code inside the main `init.lua`, the architecture points to external files:

```lua
config = function()
    require("user.plugins.config.telescope")
end
```
* **Behaviour:** Packer loads the plugin, and then immediately runs the code inside `lua/user/plugins/config/telescope.lua`.
* **Maintenance:** To change settings (like keymaps), edit the specific component file (e.g., `telescope.lua`), rather than the main plugin registry.
