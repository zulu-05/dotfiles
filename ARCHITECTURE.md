# Bash Service Architecture

This document provides a deep dive into the internal architecture of this service-oriented Bash environment.

***

## Core Philosophy
The primary goal is to replace a monolithic `.bashrc` with a scalable system where functionality is encapsulated into independent, manageable services. This improves maintainability, robustness, and clarity.

***

## Core Components
The architecture relies on a few key files that form the system's kernel.

* **`~/.bashrc`**: The main entrypoint for interactive shells. Its only jobs are to source all service files from `~/.bashrc.d/` and then start the entire system by calling `service_start "startup"`.
* **`~/.bashrc.d/`**: A directory containing all the modular service files.
* **`00-core.sh`**: The foundational layer. It provides:
    * **Service Registry**: Associative arrays (`BASH_SERVICES`, `SERVICE_STATUS`, `SERVICE_DEPENDENCIES`) track all services, their status, and their relationships.
    * **Service Lifecycle Functions**: `service_register` and `service_start` manage the state of each service.
    * **Logging**: A centralized logging system (`log_info`, `log_warn`, `log_error`).
    * **`PROMPT_COMMAND` Hook System**: A central, non-conflicting mechanism for services to execute logic before each prompt.
* **`10-config.sh`**: Provides a centralized key-value store (`BASH_CONFIG`) and safe accessors (`config_get`) for all other services to use.
* **`99-startup.sh`**: The last service to be registered. Its `startup_service_init` function iterates through all other registered services and starts them, ensuring a dependency-aware initialization.

***

## Service Lifecycle
1.  **Registration**: As `~/.bashrc` sources each file in `~/.bashrc.d/`, the `service_register` function is called. This populates the `BASH_SERVICES` array with the service's metadata (init function, cleanup function, and type) but does not execute anything yet.
2.  **Startup**: The main `.bashrc` file calls `service_start "startup"`. This triggers the startup coordinator, which then calls `service_start` for every other registered service.
3.  **Dependency Resolution**: Before starting a service, `service_start` in `00-core.sh` checks its dependencies in the `SERVICE_DEPENDENCIES` array and recursively starts them first. For example, the `prompt` service will not start until its dependencies, `config` and `git`, are running.
4.  **Shutdown**: An `EXIT` trap is set to call the `_cleanup_services` function when the shell closes. This function iterates through all "running" services and executes their registered cleanup function, ensuring a graceful shutdown.

***

## Key Design Patterns

### Service Types (`utility` vs. `daemon`)
The service registration accepts a type, which is critical for lifecycle management.

* **`utility`**: The default type for services that set up the environment, such as defining aliases. Their init function runs once in the foreground.
* **`daemon`**: For services that run a persistent background process, such as the `auto_reload` service when using the `inotify` method. When a daemon is started, its Process ID (PID) is stored in the `SERVICE_PIDS` array, and it is sent a `TERM` signal during cleanup.

### Centralized `PROMPT_COMMAND` Hooks
Directly modifying `PROMPT_COMMAND` is fragile. This system avoids conflicts by setting `PROMPT_COMMAND` to a single master function, `_run_prompt_hooks`. Services that need to run before the prompt is drawn (like `python_venv` for auto-activation or `auto_reload` for timestamp checks) call `register_prompt_hook` during their initialization.

### Performance Caching
To ensure the prompt remains fast, services that perform potentially slow lookups on every command implement their own caching. The `git`, `python_venv`, and `prompt` services all use associative arrays to store results and timestamps, only re-computing the data after a configurable Time-To-Live (TTL) has expired.

### Service Decoupling and Communication
Services are designed to be decoupled. They communicate via the core system or by calling functions explicitly provided by other services. For example, the `prompt` service is not aware of *how* the Git status is calculated; it simply calls the `git_service_get_status` function provided by the `git` service. This allows the implementation of the `git` service to change without requiring any modifications to the `prompt` service.
