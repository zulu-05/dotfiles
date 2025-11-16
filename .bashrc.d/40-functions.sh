#!/bin/bash
# ==============================================================================
# Utility Functions Service
#
# Filename: 40-functions.sh
# Purpose:  Defines reusable shell utilities. Safe for re-sourcing.
#           Depends on core service.
# ==============================================================================

[[ $- != *i* ]] && return

if ! declare -f service_register >/dev/null; then
    echo "Error: Functions service requires core service" >&2
    return 1
fi

log_info "Loading functions service"

# ------------------------------------------------------------------------------
# FUNCTION DEFINITIONS
# ------------------------------------------------------------------------------
mkcd() {
    [ -z "$1" ] && echo "Usage: mkcd <dir>" >&2 && return 1
    mkdir -p "$@" && cd -- "${@: -1}" || return 1
}

# More robust 'dus' that handles files with spaces
dus() {
    du -sh -- * | sort -rh | head -n "${1:-10}"
}

extract() {
    local file
    for file in "$@"; do
        if [ ! -f "$file" ]; then
            echo "extract: '$file' is not a valid file" >&2
            continue
        fi
        case "$file" in
            *.tar.gz|*.tgz)   tar -xzvf "$file" ;;
            *.tar.bz2|*.tbz2) tar -xjvf "$file" ;;
            *.tar.xz|*.txz)   tar -xJvf "$file" ;;
            *.zip)            unzip "$file" ;;
            *.rar)            unrar x "$file" ;;
            *.gz)             gunzip "$file" ;;
            *.bz2)            bunzip2 "$file" ;;
            *.7z)             7z x "$file" ;;
            *)                echo "extract: unsupported format for '$file'" >&2 ;;
        esac
    done
}

# Searches for a pattern in a directory using Neovim and Telescope.
# Usage: zap <pattern> [directory] [-r]
#     - <pattern>: The text or regex pattern to search for.
#     - [directory]: Optional. The directory to search in. Defaults to the current directory.
#     - [-r]: Optional. Accepted for convenience; search is recursive by default.
zap() {
    local pattern=""
    local directory="."
    # The -r flag is parsed but doesn't change behaviour, as ripgrep is recursive by default.
    # This makes the command feel more familiar to users of grep.

    # Robust argument parsing loop.
    while (( "$#" )); do
        case "$1" in
            -r)
                # This flag is simply consumed.
                shift
                ;;
            -*) # Handle unknown flags
                echo "Error: Unknown flag $1" >&2
                echo "Usage: zap <pattern> [directory] [-r]" >&2
                return 1
                ;;
            *)
                if [[ -z "$pattern" ]]; then
                    pattern="$1"
                else
                    directory="$1"
                fi
                shift
                ;;
        esac
    done

    # Ensure a search pattern was provided.
    if [[ -z "$pattern" ]]; then
        echo "Usage: zap <pattern> [directory] [-r]" >&2
        return 1
    fi

    # Construct and execute the Neovim command.
    # This launches nvim and immediately runs Telescope's live_grep.
    nvim --cmd "lua require('telescope.builtin').live_grep({ search_dirs = {'${directory}'}, default_text = '${pattern}' })"
}

# Initialises a git repo, adds all files, and makes the initial commit.
gstart() {
    # Check if git command is available first.
    if ! command -v git &> /dev/null; then
        echo "Error: git command not found. Please install Git." >&2
        return 1
    fi

    # Check if we are not in a git repository at all.
    # If not, this is the simplest case: do everything.
    if ! git rev-parse --is-inside-work-tree &> /dev/null; then
        echo "--> Not a Git repository. Initializing, adding all files, and committing..."
        git init && git add . && git commit -m "Initial commit"
        return $?
    fi

    # If we are here, we are inside a git repository.
    # Now, check if there are any commits. If so, our work is done.
    if git rev-parse --verify HEAD &> /dev/null; then
        echo "Info: This repository already has commits. No action taken."
        return 0
    fi

    # If we are here, we are in a repo with NO commits.
    # The final step is to check if files are already staged.
    # `git diff --cached --quiet` exits with 1 if there are staged changes.
    if ! git diff --cached --quiet; then
        echo "--> Repository is initialized and files are staged. Committing..."
        git commit -m "Initial commit"
        return $?
    else
        echo "--> Repository is initialized, but no files are staged. Adding all and committing..."
        git add . && git commit -m "Initial commit"
        return $?
    fi
}

# Changes the current directory to the root of the current Git repository
# Usage: cdgr
cdgr() {
    # Check if the Git command is available first.
    if ! command -v git &> /dev/null; then
        echo "Error: Git command not found. Please install Git." >&2
        return 1
    fi

    # Use the reliable 'rev-parse' command to find the top-level directory.
    local git_root
    git_root=$(git rev-parse --show-toplevel 2>/dev/null)

    # Check if the command succeeded. If not, we are not in a Git repository.
    if [[ -z "$git_root" ]]; then
        echo "Error: Not inside a Git repository." >&2
        return 1
    fi

    # Change to the Git root directory.
    cd "$git_root" || return 1
}

# Provides an intelligent, filtered 'tree -a' view of the current directory.
# It hides auto-generated files, caches, and dependency directories.
# Usage: lsa [directory]
lsa() {
    # First, ensure the 'tree' command is available.
    if ! command -v tree &> /dev/null; then
        echo "Error: 'tree' command not found. Please install it." >&2
        echo "On Debian/Ubuntu: sudo apt install tree" >&2
        return 1
    fi

    # Define the exclusion pattern. This is the core of the function's intelligence.
    # Hides the version control internals, virtual environments, caches, and other noise.
    local exclude_pattern=".git|.venv|__pycache__|packer_compiled.lua|node_modules|target|.DS_Store"

    # Execute tree with the '-a' flag (to see dotfiles) and our ignore pattern.
    # All arguments passed to 'lsa' (like a directory path) are forwarded to 'tree'.
    tree -a -I "$exclude_pattern" "$@"
}

# ------------------------------------------------------------------------------
# SERVICE INTEGRATION
# ------------------------------------------------------------------------------
functions_service_init() {
    log_info "Functions service initialized"
}

functions_service_cleanup() {
    unset -f mkcd dus extract zap gstart cdgr lsa
    log_info "Functions service stopped"
}

# ------------------------------------------------------------------------------
# SERVICE REGISTRATION
# ------------------------------------------------------------------------------
service_register "functions" \
    "functions_service_init" \
    "functions_service_cleanup" \
    "utility"

# ------------------------------------------------------------------------------
# NAMESPACE PROTECTION
# ------------------------------------------------------------------------------
readonly -f mkcd dus extract zap gstart cdgr lsa
