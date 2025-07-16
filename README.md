# Modular Bash Services

This repository contains a powerful, modular, and service-oriented bash environment. It replaces a single, monolithic `.bashrc` file with a collection of independent "services" that are easy to manage, configure, and extend.

***

## ✨ Features

* **Fast, Two-Line Prompt**: A clean and informative prompt shows your virtual environment, Git status, user, host, and current path.
* **Intelligent Git Integration**:
    * Provides a rich set of common Git aliases (`gst`, `gco`, `gl`, etc.).
    * Displays a detailed Git status in the prompt, including branch, ahead/behind count, modified files, untracked files, and stashed items.
* **Automatic Python Venv Management**:
    * Automatically detects and activates a `.venv` in your project's directory tree.
    * Automatically deactivates the virtual environment when you navigate away.
    * Includes a simple `venv-create` command to quickly set up a new environment.
* **Live Configuration Reloading**: Automatically reloads your shell's configuration when you save changes to any of the service files, using either an efficient `inotify` daemon or a timestamp-based check.
* **Helpful Utilities**:
    * A collection of useful aliases for navigation (`ll`, `..`, `...`) and system operations (`update`, `psg`).
    * Powerful shell functions like `extract` for any archive type and `mkcd` to create and enter a directory in one step.
* **Centralized Configuration**: All settings are managed in one place with sensible defaults, which you can easily override.

***

## 🚀 Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/dotfiles.git](https://github.com/your-username/dotfiles.git) ~/dotfiles
    ```
2.  **Run the installer:**
    The installer script will back up any existing configuration files and create symbolic links to the files in this repository.
    ```bash
    cd ~/dotfiles
    ./install.sh
    ```
3.  **Restart your shell:**
    Open a new terminal or run `source ~/.bashrc` to activate the new environment.

***

## 🔧 Configuration

You can easily customize the behavior of the services without modifying the core files.

1.  **Create an override file**:
    ```bash
    touch ~/.bashrc.d/config.conf
    ```
2.  **Add your settings**:
    Open `~/.bashrc.d/config.conf` and add any values you want to change. For example:

    ```ini
    # Disable venv auto-activation
    venv_auto_activate=false

    # Use the inotify method for faster reloads
    reload_method=inotify

    # Set the cache Time-To-Live (TTL) for the git prompt to 5 seconds
    git_prompt_cache_ttl=5
    ```

You can find a full list of default settings in `.bashrc.d/10-config.sh`.

***

## 🧩 Adding a New Service

Creating a new service is simple. Here's how to add a "hello world" service:

1.  **Create the file**: `touch ~/.bashrc.d/91-hello.sh`
2.  **Add the content**:

    ```bash
    #!/bin/bash
    # My "Hello World" Service

    # Initialization function
    hello_init() {
        echo "Hello from your new service!"
    }

    # Cleanup function (optional)
    hello_cleanup() {
        echo "Goodbye from the hello service."
    }

    # Register the service with the core system
    service_register "hello" "hello_init" "hello_cleanup" "utility"
    ```
3.  **Reload your shell**, and you will see "Hello from your new service!" printed on startup.
