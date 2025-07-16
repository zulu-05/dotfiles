#!/bin/bash
# ==============================================================================
# Python Virtual Environment Service
#
# Filename: 60-python.sh
# Purpose:  Manages Python virtual environments with caching and auto-activation
#           using the service-oriented architecture. Depends on core and config.
#
# Features:
#   - Cached venv detection with TTL and depth limit
#   - Automatic activation/deactivation via prompt hook
#   - Safe venv creation with validation
#   - Service lifecycle integration
# ==============================================================================

# Only run in interactive shells
[[ $- != *i* ]] && return

# Check dependencies
if ! declare -f service_register >/dev/null || ! declare -f config_get >/dev/null; then
    echo "Error: Python venv service requires core and config services" >&2
    return 1
fi

log_info "Loading python_venv service"

# ------------------------------------------------------------------------------
# SECTION 1: VENV DISCOVERY AND CACHING
# ------------------------------------------------------------------------------
declare -A VENV_CACHE=()      # Cache: [dir_path]=venv_path
declare -A VENV_CACHE_TIME=() # Cache: [dir_path]=timestamp

# Find venv with caching and depth limit
find_venv_cached() {
    local dir="$1"
    local current_time
    current_time=$(date +%s)
    local cache_ttl
    cache_ttl=$(config_get venv_cache_ttl 10)

    # Check cache validity
    if [[ -v "VENV_CACHE[$dir]" ]] && \
       (( current_time - ${VENV_CACHE_TIME[$dir]:-0} < cache_ttl )); then
        echo "${VENV_CACHE[$dir]}"
        return 0
    fi

    # Cache miss - search filesystem up to a max depth
    local venv_path=""
    local search_dir="$dir"
    local max_depth
    max_depth=$(config_get max_path_depth 10)
    local current_depth=0

    while [[ "$search_dir" != "/" && "$search_dir" != "" && $current_depth -lt $max_depth ]]; do
        if [[ -d "$search_dir/.venv" ]]; then
            venv_path="$search_dir/.venv"
            break
        fi
        search_dir="$(dirname "$search_dir")"
        ((current_depth++))
    done

    # Update cache
    VENV_CACHE["$dir"]="$venv_path"
    VENV_CACHE_TIME["$dir"]="$current_time"

    echo "$venv_path"
}

# ------------------------------------------------------------------------------
# SECTION 2: AUTO-ACTIVATION ENGINE
# ------------------------------------------------------------------------------
__auto_activate_venv() {
    # Guard against running if feature is disabled
    [[ $(config_get venv_auto_activate "true") != "true" ]] && return

    local venv_path
    venv_path=$(find_venv_cached "$PWD")

    # If the found path is the same as the active one, do nothing.
    [[ "$venv_path" == "$VIRTUAL_ENV" ]] && return

    # Deactivate if we are in a new directory without a venv, but one is active.
    if [[ -n "$VIRTUAL_ENV" && -z "$venv_path" ]]; then
        log_debug "Deactivating Python venv: $(basename "$VIRTUAL_ENV")"
        deactivate
    fi

    # Activate new venv if found and not already active
    if [[ -n "$venv_path" && "$venv_path" != "$VIRTUAL_ENV" ]]; then
        # Deactivate previous venv if there is one
        if [[ -n "$VIRTUAL_ENV" ]]; then
            log_debug "Deactivating current venv before switching"
            deactivate
        fi
        if [[ -f "$venv_path/bin/activate" ]]; then
            log_debug "Activating Python venv: $venv_path"
            source "$venv_path/bin/activate"
        fi
    fi
}

# ------------------------------------------------------------------------------
# SECTION 3: VENV CREATION & MANAGEMENT
# ------------------------------------------------------------------------------
create_py_venv() {
    # Validate Python installation
    if ! command -v python3 &>/dev/null; then
        log_error "Python3 not found in PATH. Cannot create virtual environment."
        return 1
    fi

    # Check if a venv already exists
    if [[ -d ".venv" ]]; then
        read -p "A virtual environment '.venv' already exists. Overwrite? (y/N): " response
        [[ ! "${response,,}" =~ ^(y|yes)$ ]] && return 1
        log_info "Removing existing .venv directory."
        rm -rf .venv
    fi

    local env_name="${1:-$(basename "$PWD")}"
    log_info "Creating Python venv '.venv' with prompt '$env_name'"

    if python3 -m venv --prompt "$env_name" .venv; then
        # Invalidate cache for current directory to force re-detection
        unset 'VENV_CACHE[$PWD]'
        # Activate the new environment
        source .venv/bin/activate
        log_info "Virtual environment created and activated."
        return 0
    else
        log_error "Failed to create virtual environment."
        return 1
    fi
}

# ------------------------------------------------------------------------------
# SECTION 4: SERVICE INTEGRATION
# ------------------------------------------------------------------------------
python_venv_init() {
    # Hook into the core prompt command system
    register_prompt_hook "__auto_activate_venv"
    alias venv-create='create_py_venv'
    log_info "Python venv service initialized"
}

python_venv_cleanup() {
    # Remove from the core prompt command system
    unregister_prompt_hook "__auto_activate_venv"
    unalias venv-create 2>/dev/null

    # Clear cache
    VENV_CACHE=()
    VENV_CACHE_TIME=()
    log_info "Python venv service stopped"
}

# ------------------------------------------------------------------------------
# SECTION 5: SERVICE REGISTRATION
# ------------------------------------------------------------------------------
service_register "python_venv" \
    "python_venv_init" \
    "python_venv_cleanup" \
    "utility"

SERVICE_DEPENDENCIES["python_venv"]="config"

# ------------------------------------------------------------------------------
# SECTION 6: NAMESPACE PROTECTION
# ------------------------------------------------------------------------------
readonly -f find_venv_cached __auto_activate_venv create_py_venv
readonly -f python_venv_init python_venv_cleanup
