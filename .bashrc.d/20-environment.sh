#!/bin/bash
# ==============================================================================
# Environment Configuration Service
#
# Filename: 20-environment.sh
# Purpose:  Sets global environment variables, PATH, and secret management.
#           Idempotent design safe for re-sourcing. Depends on core/config.
# ==============================================================================

[[ $- != *i* ]] && return  # Only interactive shells

if ! declare -f service_register >/dev/null; then
    echo "Error: Environment service requires core service" >&2
    return 1
fi

log_info "Loading environment service"

# ------------------------------------------------------------------------------
# PATH MANAGEMENT FUNCTIONS
# ------------------------------------------------------------------------------
__path_prepend() {
    [ -d "$1" ] && [[ ":$PATH:" != *":$1:"* ]] && PATH="$1:$PATH"
}

__path_append() {
    [ -d "$1" ] && [[ ":$PATH:" != *":$1:"* ]] && PATH="$PATH:$1"
}

# ------------------------------------------------------------------------------
# SECRET MANAGEMENT FUNCTIONS
# ------------------------------------------------------------------------------
git_token() {
    command -v pass >/dev/null && pass show github_token 2>/dev/null
}

email_pass() {
    command -v pass >/dev/null && pass show email_pass 2>/dev/null
}

# ------------------------------------------------------------------------------
# ENVIRONMENT INITIALIZATION
# ------------------------------------------------------------------------------
env_service_init() {
    # WSL GUI configuration
    if grep -qi microsoft /proc/version; then
        export DISPLAY="${DISPLAY:-:0}"
        export LIBGL_ALWAYS_INDIRECT=1
        export QT_QPA_PLATFORM=xcb
        log_debug "Configured WSL environment"
    fi

    # Core PATH configuration
    __path_prepend "$HOME/.local/bin"
    __path_append "$HOME/scripts"
    __path_append "$HOME/.vcpkg"
    
    # Ruby GEM_HOME might not be standard, handle carefully
    if command -v ruby >/dev/null; then
      export GEM_HOME="$(ruby -e 'puts Gem.user_dir')"
      __path_append "$GEM_HOME/bin"
    fi

    # Standard environment variables
    export EDITOR=nvim
    export PAGER=less
    export MANPAGER="less -X"
    export FZF_DEFAULT_OPTS="--height 40% --layout=reverse --border"

    log_info "Environment service initialized"
}

# ------------------------------------------------------------------------------
# SERVICE CLEANUP
# ------------------------------------------------------------------------------
env_service_cleanup() {
    # This cleanup is minimal as PATH and ENV changes are hard to revert safely.
    # We only unset the internal functions of this script.
    unset -f __path_prepend __path_append git_token email_pass
    log_info "Environment service stopped"
}

# ------------------------------------------------------------------------------
# SERVICE REGISTRATION
# ------------------------------------------------------------------------------
service_register "environment" \
    "env_service_init" \
    "env_service_cleanup" \
    "utility"

# ------------------------------------------------------------------------------
# NAMESPACE PROTECTION
# ------------------------------------------------------------------------------
readonly -f __path_prepend __path_append env_service_init env_service_cleanup git_token email_pass
