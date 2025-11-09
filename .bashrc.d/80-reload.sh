#!/bin/bash
# ==============================================================================
# Auto-Reload Service
#
# Filename: 80-reload.sh
# Purpose:  Provides automatic reloading of configuration changes using either
#           a timestamp-based check or an inotify-based background daemon.
#
# Features:
#   - Timestamp-based method via prompt hook (low overhead)
#   - Inotify-based daemon method (immediate detection)
#   - Recursion prevention during reload
# ==============================================================================

# Only run in interactive shells
[[ $- != *i* ]] && return

# Check if core and config services are loaded
if ! declare -f service_register >/dev/null || ! declare -f config_get >/dev/null; then
    echo "Error: Auto-reload service requires core and config services" >&2
    return 1
fi

log_info "Loading auto_reload service"

# ------------------------------------------------------------------------------
# SECTION 1: CORE RELOAD FUNCTIONALITY
# ------------------------------------------------------------------------------
# Global variable to prevent recursive reloads
export _RELOAD_IN_PROGRESS=false

# Primary reload mechanism
safe_reload() {
    if [[ "$_RELOAD_IN_PROGRESS" == "true" ]]; then
        log_warn "Recursive reload attempt prevented"
        return 1
    fi

    _RELOAD_IN_PROGRESS=true
    log_info "Configuration has changed. Reloading shell..."
    
    # Execute the reload. `source` is crucial here.
    source ~/.bashrc
    
    # Unset the guard after reloading is complete
    _RELOAD_IN_PROGRESS=false
}

# ------------------------------------------------------------------------------
# SECTION 2: CHANGE DETECTION METHODS
# ------------------------------------------------------------------------------
# Low-overhead method that checks file modification times via prompt hook
auto_reload_check_timestamp() {
    local config_dir
    config_dir=$(config_get config_dir "$HOME/.bashrc.d")
    local cache_dir
    cache_dir=$(config_get cache_dir "$HOME/.cache/bash-services")
    local ts_cache_file="${cache_dir}/config-timestamps"
    local reload_needed=false

    # Ensure cache directory exists
    mkdir -p "$cache_dir"

    # Check if cache file exists or if the main .bashrc is newer
    if [[ ! -f "$ts_cache_file" ]] || [[ ~/.bashrc -nt "$ts_cache_file" ]]; then
        reload_needed=true
    else
        # Check if any config file is newer than the cache file
        while IFS= read -r -d $'\0' file; do
            if [[ "$file" -nt "$ts_cache_file" ]]; then
                reload_needed=true
                break
            fi
        done < <(find "$config_dir" -type f \( -name '*.sh' -o -name '*.conf' \) -print0)
    fi

    # Trigger reload if needed and update the timestamp cache
    if [[ "$reload_needed" == "true" ]]; then
        touch "$ts_cache_file"
        safe_reload
    fi
}

# Checks for a trigger file created by the inotify daemon
auto_reload_check_trigger() {
    local trigger_file
    trigger_file="$(config_get cache_dir "$HOME/.cache/bash-services")/reload-trigger"
    
    if [[ -f "$trigger_file" ]]; then
        rm -f "$trigger_file"
        safe_reload
    fi
}

# ------------------------------------------------------------------------------
# SECTION 3: INOTIFY DAEMON STARTUP
# ------------------------------------------------------------------------------
# This function is run in the background by the core 'service_start'
_auto_reload_start_daemon() {
    if ! command -v inotifywait >/dev/null; then
        log_warn "inotifywait not found. Auto-reload will not use inotify method."
        return 1
    fi
    
    local config_dir
    config_dir=$(config_get config_dir "$HOME/.bashrc.d")
    local trigger_file
    trigger_file="$(config_get cache_dir "$HOME/.cache/bash-services")/reload-trigger"

    # The daemon's main loop
    while true; do
        # Watch relevant config files for changes and wait quietly.
        inotifywait -qq -e close_write,moved_to,create,delete \
            ~/.bashrc "$config_dir"
        
        # Create a trigger file for the prompt hook to discover.
        # This is necessary because a background process cannot 'source' for the parent shell.
        touch "$trigger_file"
    done
}

# ------------------------------------------------------------------------------
# SECTION 4: SERVICE MANAGEMENT
# ------------------------------------------------------------------------------
auto_reload_init() {
    local method
    method=$(config_get reload_method "timestamp")
    log_info "Initializing auto-reload service with method: $method"

    case "$method" in
        "inotify")
            register_prompt_hook "auto_reload_check_trigger"
            exec _auto_reload_start_daemon
            ;;
        "timestamp")
            register_prompt_hook "auto_reload_check_timestamp"
            ;;
        *) # Default to timestamp for safety
            log_warn "Unknown reload_method '$method'. Defaulting to 'timestamp'."
            register_prompt_hook "auto_reload_check_timestamp"
            ;;
    esac
}

auto_reload_cleanup() {
    # Unregister all possible hooks this service might have set
    unregister_prompt_hook "auto_reload_check_timestamp"
    unregister_prompt_hook "auto_reload_check_trigger"
    log_info "Auto-reload service stopped"
}

# Determine the service type dynamically based on the configuration.
# This is crucial because only the 'inotify' method runs a true daemon.
# The 'timestamp' method is a simple utility that sets up a prompt hook.
reload_method_for_type_check=$(config_get reload_method "timestamp")
service_type="utility" # Default to utility
if [[ "$reload_method_for_type_check" == "inotify" ]]; then
    service_type="daemon"
fi

log_debug "Registering auto_reload service as type: $service_type"
service_register "auto_reload" \
    "auto_reload_init" \
    "auto_reload_cleanup" \
    "$service_type"

SERVICE_DEPENDENCIES["auto_reload"]="config"

# ------------------------------------------------------------------------------
# SECTION 5: NAMESPACE PROTECTION
# ------------------------------------------------------------------------------
readonly -f safe_reload auto_reload_check_timestamp auto_reload_check_trigger
readonly -f _auto_reload_start_daemon auto_reload_init auto_reload_cleanup
