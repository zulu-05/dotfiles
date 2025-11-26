# Bash Service Manifest

This directory contains all the modular "services" that make up the shell environment. The services are sourced in numerical order by the main `.bashrc` file, but their initialisation is managed by the `99-startup.sh` coordinator, which respects the explicit dependencies listed below.

This systems turns a monolithic `.bashrc` into a maintainable, decoupled, and extensible set of components.

## Service Overview

| File | Purpose | Key Features / Provides | Dependencies | Config Keys |
| :--- | :--- | :--- | :--- | :--- |
| **`00-core.sh`** | The foundational layer of the service framework. | `service_register()`, `log_*()`, `register_prompt_hook()` | None | `log_level` |
| **`10-config.sh`** | Manages environment configuration with defaults and overrides. | `config_get()`, loads `~/.bashrc.d/config.conf` | `core` | *(Defines all)* |
| **`20-environment.sh`** | Sets up the `PATH` and global environment variables. | `PATH` management, `EDITOR`, WSL variables, `git_token()` | `core` | `None` |
| **`30-aliases.sh`** | Defines common, everyday command aliases. | `ll`, `update`, `reload`, `explorer` (WSL) | `core` | `None` |
| **`40-functions.sh`** | Defines useful, complex shell functions and commands. | `zap()`, `mkcd`, `lsa`, `cdgr`, `gstart` | `core` | `None` |
| **`50-git.sh`** | Provides Git aliases and a status provider for the prompt. | `gst`, `gpl`, `git_service_get_status()` | `core`, `config` | `git_prompt_cache_ttl` |
| **`60-python.sh`** | Manages Python virtual environments. | `mkvenv`, `rmvenv`, automatic venv activation hook | `core`, `config` | `venv_auto_activate`, `venv_cache_ttl`, `max_path_depth` |
| **`70-prompt.sh`** | Generates the interactive, two-line shell prompt. | Sets `PS1` using components (venv, git, path) | `core`, `config`, `git` | `prompt_cache_ttl` |
| **`80-reload.sh`** | Provides the ability to live-reload the shell config. | `safe_reload()`, `timestamp` & `inotify` methods | `core`, `config` | `reload_method`, `config_dir`, `cache_dir` |
| **`90-integrations.sh`** | A placehlder for future third-party service integrations. | *(None currently)* | `core` | `None` |
| **`99-startup.sh`** | The startup coordinator that initialises all services. | The main startup loop that calls `service_start()` on all others. | `core` | `None` |

---

## How to Add a New Service

To extend the shell's functionality, follow this pattern:

1. **Create the File:** Create a new file with a numerical prefix that places it correctly in the sourcing order (e.g., `45-new-feature.sh`).
2. **Define Functions:** Write the `_init` and `_cleanup` functions for the service's logic. Keep functions that are not intended to be called by other services as "private" (e.g., by prefixing with `__`).
3. **Register the Service:** Call `service_register "my_feature" "_init" "_cleanup" "utility" at the end of the file.
4. **Declare Dependencies:** If the service needs functions from another (e.g., `config_get`), declare it: `SERVICE_DEPENDENCIES["my_feature"]="config"`.
5. **Update this Manifest:** Add a new row to the table above to document the new service.
