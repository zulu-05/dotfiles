#!/bin/bash
# ==============================================================================
# Core Infrastructure & Logging Service
#
# Filename: 00-core.sh
# Purpose:  Provides core infrastructure for service management, error handling,
#           logging, and prompt command hooks. This must be sourced first.
#
# Features:
#   - Service registry with distinct daemon/utility types
#   - Centralized logging with configurable levels
#   - Centralized PROMPT_COMMAND hook system
#   - Signal handling for graceful shutdown
#   - Namespace protection for internal functions
# ==============================================================================

# Only run in interactive shells
[[ $- != *i* ]] && return

# ------------------------------------------------------------------------------
# SECTION 1: SERVICE REGISTRY & HOOKS
# ------------------------------------------------------------------------------
declare -A BASH_SERVICES=()         # Registry: [name]="init_func cleanup_func type"
declare -A SERVICE_PIDS=()          # PIDs for 'daemon' services: [name]=pid
declare -A SERVICE_STATUS=()        # Status: [name]="running|stopped|error"
declare -A SERVICE_DEPENDENCIES=()  # Dependencies: [name]="dep1 dep2"
declare -a BASH_PROMPT_HOOKS=()     # Functions to run in PROMPT_COMMAND

# ------------------------------------------------------------------------------
# SECTION 2: LOGGING SYSTEM
# ------------------------------------------------------------------------------
BASH_LOG_DIR="${HOME}/.cache/bash-services"
mkdir -p "${BASH_LOG_DIR}"
BASH_LOG_FILE="${BASH_LOG_DIR}/services.log"
BASH_LOG_LEVEL="${BASH_LOG_LEVEL:-INFO}" # Default, can be overridden by config service

log_error() {
    echo "[ERROR] $(date '+%Y-%m-%d %H:%M:%S') $*" >&2
    echo "[ERROR] $(date '+%Y-%m-%d %H:%M:%S') $*" >> "${BASH_LOG_FILE}"
}

log_warn() {
    echo "[WARN]  $(date '+%Y-%m-%d %H:%M:%S') $*" >&2
    echo "[WARN]  $(date '+%Y-%m-%d %H:%M:%S') $*" >> "${BASH_LOG_FILE}"
}

log_info() {
    if [[ "$BASH_LOG_LEVEL" =~ ^(INFO|DEBUG)$ ]]; then
        echo "[INFO]  $(date '+%Y-%m-%d %H:%M:%S') $*" >> "${BASH_LOG_FILE}"
    fi
}

log_debug() {
    if [[ "$BASH_LOG_LEVEL" == "DEBUG" ]]; then
        echo "[DEBUG] $(date '+%Y-%m-%d %H:%M:%S') $*" >> "${BASH_LOG_FILE}"
    fi
}

# ------------------------------------------------------------------------------
# SECTION 3: PROMPT COMMAND HOOK SYSTEM
# ------------------------------------------------------------------------------
# Registers a function to be executed by PROMPT_COMMAND
register_prompt_hook() {
    local hook_func="$1"
    # Avoid adding duplicates
    for hook in "${BASH_PROMPT_HOOKS[@]}"; do
        [[ "$hook" == "$hook_func" ]] && return 0
    done
    BASH_PROMPT_HOOKS+=("$hook_func")
}

# Unregisters a function from PROMPT_COMMAND
unregister_prompt_hook() {
    local hook_func="$1"
    local new_hooks=()
    for hook in "${BASH_PROMPT_HOOKS[@]}"; do
        [[ "$hook" != "$hook_func" ]] && new_hooks+=("$hook")
    done
    BASH_PROMPT_HOOKS=("${new_hooks[@]}")
}

# Master function called by PROMPT_COMMAND to execute all registered hooks
_run_prompt_hooks() {
    for hook in "${BASH_PROMPT_HOOKS[@]}"; do
        # Ensure function exists before calling
        declare -F "$hook" > /dev/null && "$hook"
    done
}

# Set PROMPT_COMMAND to use the hook system exclusively
PROMPT_COMMAND="_run_prompt_hooks"

# ------------------------------------------------------------------------------
# SECTION 4: SERVICE LIFECYCLE MANAGEMENT
# ------------------------------------------------------------------------------
# [cite_start]Register a service with its type (utility or daemon) [cite: 99]
service_register() {
    local service_name="$1"
    local init_func="${2:-}"
    local cleanup_func="${3:-}"
    local service_type="${4:-utility}" # Default to 'utility'

    BASH_SERVICES["$service_name"]="$init_func $cleanup_func $service_type"
    SERVICE_STATUS["$service_name"]="registered"
    log_info "Registered service: $service_name (type: $service_type)"
}

# Start a service and its dependencies
service_start() {
    local service_name="$1"

    # Check if service is registered
    if [[ -z "${BASH_SERVICES[$service_name]}" ]]; then
        log_warn "Attempted to start unregistered service: $service_name"
        return 1
    fi

    # Check if already running
    if [[ "${SERVICE_STATUS[$service_name]}" == "running" ]]; then
        return 0
    fi

    # Start dependencies first
    for dep in ${SERVICE_DEPENDENCIES[$service_name]}; do
        if ! service_is_running "$dep"; then
            service_start "$dep" || return 1
        fi
    done

    # Extract service details
    local service_info=(${BASH_SERVICES[$service_name]})
    local init_func="${service_info[0]}"
    local service_type="${service_info[2]}"

    if declare -F "$init_func" > /dev/null; then
        log_info "Starting service: $service_name"
        local start_success=false

        if [[ "$service_type" == "daemon" ]]; then
            # [cite_start]Run daemon in background and track its PID [cite: 58, 83]
            "$init_func" &
            SERVICE_PIDS["$service_name"]=$!
            # Give it a moment to fail
            sleep 0.1
            if kill -0 ${SERVICE_PIDS[$service_name]} 2>/dev/null; then
                log_debug "Started daemon $service_name (PID: ${SERVICE_PIDS[$service_name]})"
                start_success=true
            fi
        else
            # Run utility service in the foreground
            if "$init_func"; then
                start_success=true
            fi
        fi

        if "$start_success"; then
            SERVICE_STATUS["$service_name"]="running"
            return 0
        else
            SERVICE_STATUS["$service_name"]="error"
            log_error "Failed to start service: $service_name"
            # Unset PID if daemon start failed
            [[ "$service_type" == "daemon" ]] && unset 'SERVICE_PIDS[$service_name]'
            return 1
        fi
    else
        log_warn "No init function for service: $service_name"
        SERVICE_STATUS["$service_name"]="stopped"
        return 1
    fi
}

# Stop a service and clean up resources
service_stop() {
    local service_name="$1"

    if [[ "${SERVICE_STATUS[$service_name]}" != "running" ]]; then
        return 0
    fi

    # Extract service details
    local service_info=(${BASH_SERVICES[$service_name]})
    local cleanup_func="${service_info[1]}"
    local service_type="${service_info[2]}"

    # Kill daemon process if it exists
    if [[ "$service_type" == "daemon" && -n "${SERVICE_PIDS[$service_name]}" ]]; then
        if kill -0 "${SERVICE_PIDS[$service_name]}" 2>/dev/null; then
            log_debug "Sending TERM signal to $service_name (PID: ${SERVICE_PIDS[$service_name]})"
            kill -TERM "${SERVICE_PIDS[$service_name]}" 2>/dev/null
        fi
        unset 'SERVICE_PIDS[$service_name]'
    fi

    # Run cleanup function
    if declare -F "$cleanup_func" > /dev/null; then
        log_info "Stopping service: $service_name"
        if "$cleanup_func"; then
            SERVICE_STATUS["$service_name"]="stopped"
            return 0
        else
            log_error "Failed to clean up service: $service_name"
            return 1
        fi
    else
        SERVICE_STATUS["$service_name"]="stopped"
        return 0
    fi
}

# Check if a service is running
service_is_running() {
    local service_name="$1"
    [[ "${SERVICE_STATUS[$service_name]}" == "running" ]]
}

# ------------------------------------------------------------------------------
# SECTION 5: SIGNAL HANDLING AND CLEANUP
# ------------------------------------------------------------------------------
_cleanup_services() {
    log_info "Shutting down bash services..."
    local service_names
    # Get a list of registered services to iterate over
    service_names=(${!BASH_SERVICES[@]})

    # Stop services (reverse order is not strictly necessary but good practice)
    for ((i=${#service_names[@]}-1; i>=0; i--)); do
        service_stop "${service_names[i]}"
    done

    log_info "Cleanup completed"
}

# Setup signal traps for graceful shutdown
trap _cleanup_services EXIT

# ------------------------------------------------------------------------------
# SECTION 6: NAMESPACE PROTECTION
# ------------------------------------------------------------------------------
readonly -f log_error log_warn log_info log_debug
readonly -f register_prompt_hook unregister_prompt_hook _run_prompt_hooks
readonly -f service_register service_start service_stop service_is_running
readonly -f _cleanup_services
