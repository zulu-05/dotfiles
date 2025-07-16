#!/bin/bash
# ==============================================================================
# Configuration Management Service
#
# Filename: 10-config.sh
# Purpose:  Provides centralized configuration management with validation.
#           Must be sourced after 00-core.sh for logging functionality.
#
# Features:
#   - Centralized configuration store with defaults
#   - Type and value validation
#   - Safe access methods with fallback defaults
#   - Environment variable integration
# ==============================================================================

# Only run in interactive shells
[[ $- != *i* ]] && return

# Check if core service is loaded
if ! declare -f log_info >/dev/null; then
    echo "Error: Configuration service requires core service (00-core.sh)" >&2
    return 1
fi

log_info "Loading configuration service"

# ------------------------------------------------------------------------------
# SECTION 1: CONFIGURATION STORE
# ------------------------------------------------------------------------------
declare -A BASH_CONFIG=(
    # System settings
    [log_level]="INFO"                   # DEBUG, INFO, WARN, ERROR
    [log_file]="$HOME/.cache/bash-config.log"

    # Feature toggles
    [auto_reload]="true"                 # true|false
    [venv_auto_activate]="true"          # true|false
    [git_prompt]="true"                  # true|false

    # Performance settings
    [reload_check_interval]="1"          # seconds
    [reload_method]="timestamp"          # timestamp or inotify
    [venv_cache_ttl]="10"                # seconds
    [prompt_cache_ttl]="2"               # seconds
    [git_prompt_cache_ttl]="2"           # seconds
    [service_timeout]="5"                # seconds
    [max_path_depth]="10"                # maximum directory depth

    # Paths
    [config_dir]="$HOME/.bashrc.d"
    [cache_dir]="$HOME/.cache/bash-services"
)

# ------------------------------------------------------------------------------
# SECTION 2: CONFIGURATION ACCESS METHODS
# ------------------------------------------------------------------------------
# Retrieve a configuration value with optional default fallback
config_get() {
    local key="$1"
    local default="${2:-}"

    # Check if key exists in configuration
    if [[ -v "BASH_CONFIG[$key]" ]]; then
        echo "${BASH_CONFIG[$key]}"
        return 0
    fi

    # Check environment variables as fallback
    local env_var="BASH_${key^^}"
    if [[ -v "$env_var" ]]; then
        echo "${!env_var}"
        return 0
    fi

    # Return default if provided
    [[ -n "$default" ]] && echo "$default"
    return 1
}

# Set configuration value (with validation)
config_set() {
    local key="$1"
    local value="$2"

    # Validate before setting
    if config_validate_key "$key" "$value"; then
        BASH_CONFIG["$key"]="$value"
        log_debug "Set config: $key=$value"
        return 0
    else
        log_error "Invalid value for $key: $value"
        return 1
    fi
}

# ------------------------------------------------------------------------------
# SECTION 3: CONFIGURATION VALIDATION
# ------------------------------------------------------------------------------
config_validate_key() {
    local key="$1"
    local value="$2"

    case "$key" in
        log_level)
            [[ "$value" =~ ^(DEBUG|INFO|WARN|ERROR)$ ]] || return 1
            ;;
        auto_reload|venv_auto_activate|git_prompt)
            [[ "$value" =~ ^(true|false)$ ]] || return 1
            ;;
        reload_method)
            [[ "$value" =~ ^(timestamp|inotify)$ ]] || return 1
            ;;
        reload_check_interval|venv_cache_ttl|prompt_cache_ttl|git_prompt_cache_ttl|service_timeout|max_path_depth)
            [[ "$value" =~ ^[0-9]+$ ]] && (( value >= 0 )) || return 1
            ;;
        log_file|config_dir|cache_dir)
            [[ -n "$value" ]] || return 1
            ;;
        *)
            log_warn "Unknown configuration key: $key"
            # Allow setting of unknown keys, but warn
            return 0
            ;;
    esac
    return 0
}

# Validate entire configuration
config_validate_all() {
    local valid=true
    for key in "${!BASH_CONFIG[@]}"; do
        if ! config_validate_key "$key" "${BASH_CONFIG[$key]}"; then
            log_error "Invalid configuration: $key=${BASH_CONFIG[$key]}"
            valid=false
        fi
    done
    [[ "$valid" == "true" ]]
}

# Load user configuration if it exists
config_load_user() {
    local config_file="$HOME/.bashrc.d/config.conf"
    if [[ -f "$config_file" ]]; then
        log_info "Loading user configuration from $config_file"
        while IFS='=' read -r key value; do
            # Skip comments and empty lines
            [[ "$key" =~ ^[[:space:]]*# ]] && continue
            [[ -z "$key" ]] && continue

            # Trim whitespace
            key=$(echo "$key" | xargs)
            value=$(echo "$value" | xargs)

            if [[ -n "$key" ]]; then
                config_set "$key" "$value"
            fi
        done < "$config_file"
    fi
}

# ------------------------------------------------------------------------------
# SECTION 4: SERVICE INTEGRATION
# ------------------------------------------------------------------------------
_config_service_init() {
    # Apply defaults first
    BASH_LOG_LEVEL=$(config_get log_level "INFO")
    BASH_LOG_FILE=$(config_get log_file "$HOME/.cache/bash-config.log")
    mkdir -p "$(dirname "$(config_get log_file)")"
    mkdir -p "$(config_get cache_dir)"

    # Load user overrides
    config_load_user

    # Re-apply potentially overridden values
    BASH_LOG_LEVEL=$(config_get log_level "INFO")
    BASH_LOG_FILE=$(config_get log_file "$HOME/.cache/bash-config.log")

    if ! config_validate_all; then
        log_error "Configuration validation failed. Some services may not work as expected."
        return 1
    fi
    log_info "Configuration service initialized"
    return 0
}

_config_service_cleanup() {
    log_info "Configuration service stopped"
}

# Register this service as a 'utility'
service_register "config" \
    "_config_service_init" \
    "_config_service_cleanup" \
    "utility"

# ------------------------------------------------------------------------------
# SECTION 5: NAMESPACE PROTECTION
# ------------------------------------------------------------------------------
readonly -f config_get config_set config_validate_key config_validate_all config_load_user
readonly -f _config_service_init _config_service_cleanup
