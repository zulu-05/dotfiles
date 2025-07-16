#!/bin/bash
# ==============================================================================
# Prompt Generation Service
#
# Filename: 70-prompt.sh
# Purpose:  Provides a highly optimized, cache-enabled prompt generation system
#           with git integration. Depends on core, config, and git services.
#
# Features:
#   - Caching with TTL expiration for performance
#   - Consumes Git status from the Git service
#   - Visual indicators for venv, git status, and user/host/path
#   - Integrates with the core prompt hook system
# ==============================================================================

# Only run in interactive shells
[[ $- != *i* ]] && return

# Check if core and config services are loaded
if ! declare -f service_register >/dev/null || ! declare -f config_get >/dev/null; then
    echo "Error: Prompt service requires core and config services" >&2
    return 1
fi

log_info "Loading prompt service"

# ------------------------------------------------------------------------------
# SECTION 1: CACHE DECLARATIONS
# ------------------------------------------------------------------------------
declare -A PROMPT_CACHE=()      # Cache for full prompt strings: [key]=prompt_string
declare -A PROMPT_CACHE_TIME=() # Timestamps for prompt cache: [key]=timestamp

# ------------------------------------------------------------------------------
# SECTION 2: COLOR CONFIGURATION
# ------------------------------------------------------------------------------
# Define color codes with fallbacks
_prompt_color() {
    local color_name="$1"
    case "$color_name" in
        venv)       echo "\[\033[1;35m\]" ;; # Magenta
        user)       echo "\[\033[1;32m\]" ;; # Green
        host)       echo "\[\033[1;36m\]" ;; # Cyan
        path)       echo "\[\033[1;34m\]" ;; # Blue
        git_clean)  echo "\[\033[1;32m\]" ;; # Green
        git_dirty)  echo "\[\033[1;33m\]" ;; # Yellow
        git_error)  echo "\[\033[1;31m\]" ;; # Red
        prompt)     echo "\[\033[1;37m\]" ;; # White
        reset)      echo "\[\033[0m\]"   ;;
        *)          echo "" ;;
    esac
}

# ------------------------------------------------------------------------------
# SECTION 3: PROMPT COMPONENTS
# ------------------------------------------------------------------------------
_venv_component() {
    [[ -n "$VIRTUAL_ENV" ]] || return
    local venv_name
    venv_name=$(basename "$VIRTUAL_ENV")
    echo -n "$(_prompt_color venv)[$venv_name]$(_prompt_color reset) "
}

_user_host_component() {
    echo -n "$(_prompt_color user)\u$(_prompt_color reset)@$(_prompt_color host)\h$(_prompt_color reset)"
}

_path_component() {
    echo -n "$(_prompt_color path)\w$(_prompt_color reset)"
}

_git_component() {
    # Ensure git service function is available before calling
    declare -F git_service_get_status >/dev/null || return

    # Get git status from the git service
    local git_status
    git_status=$(git_service_get_status)
    [[ -z "$git_status" ]] && return

    # Apply color based on status
    local git_color
    if [[ "$git_status" == "error" ]]; then
        git_color=$(_prompt_color git_error)
    elif [[ "$git_status" =~ (✚|…) ]]; then # Dirty if modified or untracked
        git_color=$(_prompt_color git_dirty)
    else
        git_color=$(_prompt_color git_clean)
    fi

    echo -n " ${git_color}${git_status}${reset}"
}

# ------------------------------------------------------------------------------
# SECTION 4: PROMPT GENERATION ENGINE
# ------------------------------------------------------------------------------
_generate_prompt() {
    local line1=""
    line1+="$(_venv_component)"
    line1+="$(_user_host_component)"
    line1+=":$(_path_component)"
    line1+="$(_git_component)"

    local line2="$(_prompt_color prompt)\\\$$(_prompt_color reset) "

    # Set final PS1
    PS1="\n${line1}\n${line2}"
}

# Optimized prompt generation with caching
_set_prompt() {
    local cache_ttl
    cache_ttl=$(config_get prompt_cache_ttl 2)
    # Generate cache key based on state that affects the prompt
    local cache_key="${PWD}:${VIRTUAL_ENV}"

    # Check cache validity
    if [[ -v "PROMPT_CACHE[$cache_key]" ]] && \
       (( $(date +%s) - ${PROMPT_CACHE_TIME[$cache_key]:-0} < cache_ttl )); then
        PS1="${PROMPT_CACHE[$cache_key]}"
        return
    fi

    # Generate new prompt
    _generate_prompt

    # Update cache with fresh timestamp
    PROMPT_CACHE["$cache_key"]="$PS1"
    PROMPT_CACHE_TIME["$cache_key"]=$(date +%s)
}

# ------------------------------------------------------------------------------
# SECTION 5: SERVICE INTEGRATION
# ------------------------------------------------------------------------------
prompt_service_init() {
    # Hook into the core prompt command system
    register_prompt_hook "_set_prompt"
    log_info "Prompt service initialized"
}

prompt_service_cleanup() {
    # Remove from the core prompt command system
    unregister_prompt_hook "_set_prompt"

    # Clear caches
    PROMPT_CACHE=()
    PROMPT_CACHE_TIME=()

    log_info "Prompt service stopped"
}

# ------------------------------------------------------------------------------
# SECTION 6: SERVICE REGISTRATION
# ------------------------------------------------------------------------------
service_register "prompt" \
    "prompt_service_init" \
    "prompt_service_cleanup" \
    "utility"

# Add dependencies on config (for TTLs) and git (for status)
SERVICE_DEPENDENCIES["prompt"]="config git"

# ------------------------------------------------------------------------------
# SECTION 7: NAMESPACE PROTECTION
# ------------------------------------------------------------------------------
readonly -f _prompt_color _venv_component _user_host_component _path_component
readonly -f _git_component _generate_prompt _set_prompt
