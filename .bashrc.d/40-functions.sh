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

# ------------------------------------------------------------------------------
# SERVICE INTEGRATION
# ------------------------------------------------------------------------------
functions_service_init() {
    log_info "Functions service initialized"
}

functions_service_cleanup() {
    unset -f mkcd dus extract gstart
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
readonly -f mkcd dus extract gstart
