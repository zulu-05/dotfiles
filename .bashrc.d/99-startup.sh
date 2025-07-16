#!/bin/bash
# ==============================================================================
# Service Startup Coordinator
#
# Filename: 99-startup.sh
# Purpose:  Initializes all registered services in dependency order.
#           This script is intended to be the last one sourced.
# ==============================================================================

# Only run in interactive shells
[[ $- != *i* ]] && return

if ! declare -f service_register >/dev/null; then
    echo "Error: Startup service requires core service (00-core.sh)" >&2
    return 1
fi

log_info "Loading startup coordinator"

# ------------------------------------------------------------------------------
# SERVICE INITIALIZATION
# ------------------------------------------------------------------------------
# This function iterates through and starts all registered services.
startup_service_init() {
    log_info "Coordinator starting all registered services..."
    local service
    
    # Start all services. Dependency resolution is handled by service_start.
    for service in "${!BASH_SERVICES[@]}"; do
        # Avoid starting self, which would cause an infinite loop.
        if [[ "$service" != "startup" ]]; then
            service_start "$service"
        fi
    done
    
    log_info "All services have been initialized by the coordinator."
}

# ------------------------------------------------------------------------------
# SERVICE REGISTRATION
# ------------------------------------------------------------------------------
# Register the coordinator itself as a utility service.
# The main .bashrc will call 'service_start startup' to kick everything off.
service_register "startup" \
    "startup_service_init" \
    "" \
    "utility"

# ------------------------------------------------------------------------------
# NAMESPACE PROTECTION
# ------------------------------------------------------------------------------
readonly -f startup_service_init
