# Unified Development Environment

This repository contains a complete, version-controlled development environment. It goes beyond a typical shell setup, integrating a modular, service-oriented bash framework with a modern Neovim configuration and a suite of custom command-line tools.

***

## ✨ Features

* **Modular Bash Services**: Replaces a monolithic `.bashrc` with independent services for aliases, functions, environment variables, and more, making the setup easy to manage and extend.
* **Integrated Neovim Experience**:
    * A complete, modern Neovim configuration managed by `packer.nvim` is included and installed automatically.
    * Comes pre-configured with the popular `gruvbox` theme.
    * Features the powerful `telescope.nvim` fuzzy finder for lightning-fast file navigation and text searching.
* **Custom Command-Line Tools**:
    * A professional-grade command-line tool suite located in the `bin/` directory.
    * Built upon a robust, tested, and modular Python library (`git_tools`) for maximum stability and maintainability.
    * Includes the `zap <pattern> [dir]` command, a "search and edit" power-tool that seamlessly integrates the shell with Neovim's interactive search.
    * Provides a full suite of Git management scripts to create, delete, rename, and manage GitHub repositories directly from the command line.
* **Intelligent Shell Prompt**: A clean and informative two-line prompt that shows your Python virtual environment, detailed Git status, user, host, and current path.
* **Automatic Venv and Live Reload**: Includes services for automatically activating Python virtual environments and for live-reloading your entire shell configuration whenever you save a change.

***

## 📋 Requirements

Before installation, please ensure you have the following external dependencies installed:

* **Neovim (v0.9+):** A recent version is required for the included Lua plugins to function correctly.
* **`ripgrep` (`rg`):** A fast command-line search tool used by Telescope for its live grep feature.
* **Python 3 & Pip:** Required to run the custom tools.
* **Git:** For version control and interacting with GitHub.

***

## 🚀 Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/dotfiles.git](https://github.com/your-username/dotfiles.git) ~/dotfiles
    ```
2.  **Install Python Dependencies:**
    The custom tools require a few Python packages. Install them using the provided `requirements.txt` file.
    ```bash
    pip install -r ~/dotfiles/bin/requirements.txt
    ```
    *(For developers looking to contribute, also install the development dependencies: `pip install -r ~/dotfiles/bin/requirements-dev.txt`)*

3.  **Run the installer:**
    The installer script will back up any existing configuration files and create symbolic links to the components in this repository.
    ```bash
    cd ~/dotfiles
    ./install.sh
    ```
4.  **Restart your shell:**
    Open a new terminal. The first time you run Neovim, it will automatically install its plugins via Packer.

***

## 🔧 Configuration

You can easily customize the behavior of the bash services without modifying the core files.

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
    ```
You can find a full list of default settings in `.bashrc.d/10-config.sh`.
```
