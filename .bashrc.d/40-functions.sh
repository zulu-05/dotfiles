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

# ------------------------------------------------------------------------------
# SERVICE INTEGRATION
# ------------------------------------------------------------------------------
functions_service_init() {
    log_info "Functions service initialized"
}

functions_service_cleanup() {
    unset -f mkcd dus extract
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
readonly -f mkcd dus extract
