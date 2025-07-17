# Dotfiles Architecture

This document provides a deep dive into the internal architecture of this unified development environment. The system is designed as a collection of distinct but interconnected components that together create a cohesive user experience.

***

## Core Philosophy

The primary goal is to replace a monolithic set of configuration files with a scalable, version-controlled system where functionality is encapsulated into logical components. This improves maintainability, portability, and clarity across the entire development toolchain, from the shell to the editor.

***

## Core Components

The architecture is built upon several key directories, each with a distinct responsibility. The `install.sh` script uses symbolic links to make these components available to the system from their expected locations.

* **`~/.bashrc` & `~/.profile`**
    The main entrypoints for an interactive shell session. Their role is minimal: load the modular bash services and then kick off the startup process.

    ```bash
    # From ~/.bashrc:
    # Source all .sh files from the .bashrc.d directory to register services.
    if [ -d "$HOME/.bashrc.d" ]; then
        for file in "$HOME/.bashrc.d/"*.sh; do
            # ... sourcing logic ...
        done
    fi

    # Kick off the entire service architecture by starting the 'startup' coordinator.
    if declare -f service_start >/dev/null; then
        service_start "startup"
    fi
    ```

* **`.bashrc.d/`**
    Contains all modular bash "service" files. This is the heart of the shell customization, handling aliases, functions, environment variables, and the prompt. Each file is self-contained but registers itself with the core system.

* **`config/nvim/`**
    The home for the entire Neovim configuration. It is managed by `packer.nvim` and contains all Lua files for options, plugins, and keymaps. The installer links this directory to `~/.config/nvim`.

    ```lua
    -- From config/nvim/init.lua, showing plugin management:
    require("packer").startup(function(use)
      -- Packer can manage itself
      use "wbthomason/packer.nvim"

      -- Theme
      use "gruvbox-community/gruvbox"

      -- Fuzzy Finder (Telescope) and its dependency
      use "nvim-lua/plenary.nvim"
      use { 'nvim-telescope/telescope.nvim', tag = '0.1.x' }
    end)
    ```

* **`scripts/`**
    A collection of custom, executable Python scripts that extend the shell's capabilities with complex tooling (e.g., Git repository management). The installer links this directory to `~/scripts`, which is then added to the system's `$PATH`.

    ```python
    # From scripts/download_git_repo.py, showing it's a standalone CLI tool:
    def main():
        """Parses command-line arguments and initiates the download."""
        if len(sys.argv) != 2:
            print(f"Usage: {sys.argv[0]} <repo-name>", file=sys.stderr)
            sys.exit(1)

        repo_to_download = sys.argv[1]
        download_repo(repo_to_download)

    if __name__ == "__main__":
        main()
    ```

* **`00-core.sh`**
    The foundational layer of the bash service framework. It provides the service registry, lifecycle functions, logging, and the `PROMPT_COMMAND` hook system. It is the first service sourced.

    ```bash
    # From 00-core.sh, showing the service registry arrays:
    declare -A BASH_SERVICES=()         # Registry: [name]="init_func cleanup_func type"
    declare -A SERVICE_STATUS=()        # Status: [name]="running|stopped|error"
    declare -A SERVICE_DEPENDENCIES=()  # Dependencies: [name]="dep1 dep2"
    ```

* **`99-startup.sh`**
    The startup coordinator for the bash services. It ensures all registered services are started in the correct, dependency-aware order. It is the last service sourced.

    ```bash
    # From 99-startup.sh, showing the startup loop:
    startup_service_init() {
        log_info "Coordinator starting all registered services..."
        for service in "${!BASH_SERVICES[@]}"; do
            # Avoid starting self, which would cause an infinite loop.
            if [[ "$service" != "startup" ]]; then
                service_start "$service"
            fi
        done
        log_info "All services have been initialized by the coordinator."
    }
    ```

***

## Key Design Patterns

### Service-Oriented Shell

The shell is not a single script but a collection of services that register themselves with a core engine. This allows features to be added or removed cleanly and manages dependencies explicitly.

A minimal service file has a clear structure: an init function, a cleanup function, and a call to `service_register`.

```bash
# Example of a simple service definition (e.g., in 30-aliases.sh):

# Defines all aliases for the shell.
aliases_service_init() {
    alias ll='ls -alFh'
    alias update='sudo apt update && sudo apt upgrade -y'
    # ... more aliases
}

# Unsets all aliases defined by this service.
aliases_service_cleanup() {
    unalias ll update # ... etc
}

# Register the service with the core system.
service_register "aliases" \
    "aliases_service_init" \
    "aliases_service_cleanup" \
    "utility"
```

### Hybrid Shell-Editor Integration

This is a powerful pattern that combines the convenience of a shell command with the rich, interactive UI of Neovim.

* **Example (`zap` command):** The `zap` shell function does not perform the search itself. Instead, its sole responsibility is to launch Neovim with a specific startup command that invokes the Telescope plugin.

```bash
# From 40-functions.sh: The shell function acts as a frontend.
zap() {
    local pattern=""
    local directory="."
    # ... argument parsing logic ...

    # The core logic: launch nvim with a command to run Lua code.
    nvim --cmd "lua require('telescope.builtin').live_grep({ search_dirs = {'${directory}'}, default_text = '${pattern}' })"
}
```


* **Benefit:** This approach offloads the complex, interactive work to the tool best suited for it (the editor's UI), while keeping the entrypoint as a simple, memorable command in the shell. It bridges the gap between the terminal and the editor.

### Centralised `PROMPT_COMMAND` Hooks

Directly modifying the shell's `PROMPT_COMMAND` variable is fragile and can lead to conflicts. This system avoids this by using a central queue.
1. The core service sets `PROMPT_COMMAND` to a single master function:

```bash
# From 00-core.sh
PROMPT_COMMAND="_run_prompt_hooks"
```

2. Other services then register their own functions to be run by this master function.

```bash
# From 60-python.sh, registering the venv auto-activation function: 
python_venv_init() { 
	register_prompt_hook "__auto_activate_venv" 
	# ... 
}
```

### Service Decoupling and Communication

Services are designed to be independent but can declare dependencies and communicate through well-defined functions.
1. A service declares its dependencies in the `SERVICE_DEPENDENCIES` array. The core engine ensures dependencies are started first.

```bash
# From 70-prompt.sh: The prompt needs config values and git status.
SERVICE_DEPENDENCIES["prompt"]="config git"
```

2. One service can then call a function explicitly provided by another. The `prompt` service doesn't know _how_ to get the Git status; it just asks the `git` service.

```bash
# From 70-prompt.sh, inside the prompt-building logic: 
_git_component() { 
	# Call the function provided by the git service (50-git.sh) 
	local git_status 
	git_status=$(git_service_get_status) 
	# ... use the status string ... 
}
```

This allows the implementation of the `git` service's status function to change (e.g., to add more caching or details) without requiring any modifications to the `prompt` service.