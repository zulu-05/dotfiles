# Bash Service Architecture

## 1. High-Level Overview

This document outlines the architecture of a modular, service-oriented Bash environment. This framework replaces a traditional, monolithic `.bashrc` file with a scalable system where functionality is encapsulated into independent, manageable services.

The primary advantages of this architecture are:
- **Maintainability**: Functionality is isolated into separate files (e.g., aliases, Git functions, Python environment handling), making it easier to debug, update, or remove features without affecting the entire system.
- **Scalability**: New features can be added by creating new service files without modifying core logic.
- **Robustness**: A centralized core provides common utilities like logging, configuration management, and a standardized service lifecycle, ensuring consistent behavior and graceful error handling.
- **Clarity**: The system's structure and dependencies are explicit, making the startup process understandable and deterministic.

---

## 2. Core Components

The architecture is built upon a few key files and directories, each with a distinct responsibility.

### `~/.bashrc`
This is the main entrypoint for an interactive shell session. Its role is minimal and strictly limited to:
1.  Setting standard, non-service-related shell options (e.g., `HISTCONTROL`).
2.  Sourcing all service files located in `~/.bashrc.d/` to register them with the core system.
3.  Initiating the entire service framework by calling `service_start "startup"`.

### `~/.bashrc.d/`
This directory contains all the modular service files. The files are sourced in alphanumeric order, which is why core components have low numbers (e.g., `00-core.sh`).

### `00-core.sh`
This is the foundational layer of the entire architecture. It is sourced first and provides the core infrastructure that all other services depend on. Its responsibilities include:
- **Service Registry**: Manages associative arrays (`BASH_SERVICES`, `SERVICE_STATUS`, `SERVICE_DEPENDENCIES`, `SERVICE_PIDS`) to track all registered services, their status, dependencies, and process IDs.
- **Service Lifecycle**: Provides the key functions (`service_register`, `service_start`, `service_stop`) for managing the lifecycle of each service.
- **Logging**: Offers a centralized logging system (`log_info`, `log_warn`, `log_error`) that writes to a dedicated log file (`~/.cache/bash-services/services.log`).
- **`PROMPT_COMMAND` Hook System**: Manages a centralized, safe mechanism for services to hook into the shell prompt.

### `10-config.sh`
This service provides a centralized key-value store for all configuration settings.
- It uses the `BASH_CONFIG` associative array to hold default settings.
- It provides safe accessors (`config_get`, `config_set`) for other services to retrieve configuration values.
- It can load user overrides from a `~/.bashrc.d/config.conf` file.

### `99-startup.sh`
This is the last service to be registered. Its sole purpose is to act as a coordinator that officially starts all other registered services. The main `.bashrc` file calls `service_start "startup"`, which in turn iterates through all other services and calls `service_start` on them, ensuring the entire system is initialized in the correct, dependency-aware order.

---

## 3. Service Lifecycle

The lifecycle of a service follows a clear, managed path from registration to shutdown.

1.  **Registration**: During the initial sourcing phase, each service file calls `service_register "my_service" "init_func" "cleanup_func" "type"`. This adds the service's metadata to the `BASH_SERVICES` array in `00-core.sh` but does not execute any of its logic yet.

2.  **Startup**: After all services are registered, the main `.bashrc` calls `service_start "startup"`. The startup coordinator then iterates through all registered services and calls `service_start` for each one. The `service_start` function is idempotent and dependency-aware:
    - It checks if a service is already running.
    - It recursively starts any declared dependencies first before starting the requested service.
    - It executes the service's registered `init_func`.

3.  **Shutdown**: The `00-core.sh` script sets a trap: `trap _cleanup_services EXIT`. When the shell session ends, the `_cleanup_services` function is automatically executed. This function iterates through all running services and calls their registered `cleanup_func`, ensuring a graceful shutdown. It also sends a `TERM` signal to any services registered as daemons.

---

## 4. Key Design Patterns

Two key patterns are critical to the robustness and extensibility of the framework.

### Service Types: `utility` vs. `daemon`

The `service_register` function accepts a fourth argument specifying the service type. This distinction is crucial for correct lifecycle management.

-   **`utility` (default)**: This is for services that set up the interactive environment by defining aliases, functions, or environment variables. Their `init` function runs once in the foreground during startup and does not have a persistent process. Most services (e.g., `aliases`, `functions`, `prompt`) are of this type.

-   **`daemon`**: This is for services that need to run a persistent background process, such as the `auto_reload` service when using the `inotify` method. When a `daemon` service is started, `service_start` runs its `init` function in the background (`&`) and stores its Process ID (PID) in the `SERVICE_PIDS` array. During shutdown, the `_cleanup_services` function uses this PID to send a `TERM` signal, ensuring the background process is terminated correctly.

### `PROMPT_COMMAND` Hook System

Directly manipulating the `PROMPT_COMMAND` variable from multiple scripts is brittle and prone to conflicts. This architecture solves the problem with a centralized hook system provided by `00-core.sh`.

-   `PROMPT_COMMAND` is set **once** to a single master function: `_run_prompt_hooks`.
-   Services that need to execute logic before the prompt is drawn (e.g., `python_venv`, `prompt`) do not touch `PROMPT_COMMAND`. Instead, they call `register_prompt_hook "my_hook_function"` during their initialization.
-   The `_run_prompt_hooks` function simply iterates through an array of registered hook functions and executes them in order.
-   This decouples the services, prevents conflicts, and makes the prompt execution logic clear and manageable.

---

## 5. Walkthrough: Adding a New Service

Adding a new feature is a straightforward process. Here is how to create a simple service that prints "Hello, World!" upon startup.

1.  **Create the Service File**:
    Create a new file in `~/.bashrc.d/`, for example, `91-hello.sh`. The number prefix helps control the loading order.

2.  **Write the Service Logic**:
    Add the following content to `91-hello.sh`:

    ```bash
    #!/bin/bash
    # ==================================
    # Hello World Service
    # ==================================

    # Only run in interactive shells
    [[ $- != *i* ]] && return

    # Check for core service dependency
    if ! declare -f service_register >/dev/null; then
        return 1
    fi

    # Define the initialization function
    hello_service_init() {
        echo "Hello, World! The time is $(date)."
        log_info "Hello service has run."
    }

    # Define the cleanup function
    hello_service_cleanup() {
        log_info "Hello service is cleaning up."
    }

    # Register the service with the core system
    service_register "hello" \
        "hello_service_init" \
        "hello_service_cleanup" \
        "utility"
    ```

3.  **Open a New Terminal**:
    The new service will be automatically sourced, registered, and started. Upon opening a new terminal, you will see "Hello, World!..." printed to your screen, and the log file will contain the corresponding info messages.

