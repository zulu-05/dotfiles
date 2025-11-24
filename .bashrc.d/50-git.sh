#!/bin/bash
# ==============================================================================
# Git Integration Service
#
# Filename: 50-git.sh
# Purpose:  Provides Git aliases, custom commands, and a centralized, cached
#           status function for other services. Depends on core and config.
#
# Features:
#   - Common Git aliases
#   - Centralized, cached Git status provider (git_service_get_status)
#   - Integration with other services via dependency
# ==============================================================================

# Only run in interactive shells
[[ $- != *i* ]] && return

# Check dependencies
if ! declare -f service_register >/dev/null || ! declare -f config_get >/dev/null; then
    echo "Error: Git service requires core and config services" >&2
    return 1
fi

log_info "Loading Git service"

# ------------------------------------------------------------------------------
# SECTION 1: STATUS CACHE FOR OTHER SERVICES
# ------------------------------------------------------------------------------
declare -A GIT_STATUS_CACHE=()
declare -A GIT_STATUS_TIME=()

# Get Git status with caching. This is the definitive source for other services.
git_service_get_status() {
    local git_dir
    # Find .git directory, otherwise no point proceeding.
    if ! git_dir=$(git rev-parse --git-dir 2>/dev/null); then
        # Not a git repo, clear cache for this path and return
        unset 'GIT_STATUS_CACHE[$PWD]'
        unset 'GIT_STATUS_TIME[$PWD]'
        return 1
    fi

    local current_time
    current_time=$(date +%s)
    local cache_ttl
    cache_ttl=$(config_get git_prompt_cache_ttl 2)
    local cache_key="${git_dir}"

    # Return cached result if valid
    if [[ -v "GIT_STATUS_CACHE[$cache_key]" ]] && \
       (( current_time - ${GIT_STATUS_TIME[$cache_key]:-0} < cache_ttl )); then
        echo "${GIT_STATUS_CACHE[$cache_key]}"
        return 0
    fi

    # Get fresh status using efficient porcelain v2 format
    local status_output
    if ! status_output=$(git -C "$(dirname "$git_dir")" status --porcelain=v2 -b 2>/dev/null); then
        GIT_STATUS_CACHE["$cache_key"]="error"
        GIT_STATUS_TIME["$cache_key"]="$current_time"
        echo "error"
        return 1
    fi

    local branch="" ahead=0 behind=0 modified=0 untracked=0 stashed=0

    # Parse status output
    while IFS= read -r line; do
        case "$line" in
            '# branch.head '*)      branch="${line#* }" ;;
            '# branch.ab '*)
                # Specifically remove the known prefix to get only the numbers
                local stats_only="${line/'# branch.ab '/}"
                read -r ahead behind <<< "$stats_only"

                # Strip leading + or - signs
                ahead="${ahead#[+-]}"
                behind="${behind#[+-]}"
                # Ensure they are treated as numbers, default to 0 if empty
                ahead=$((ahead + 0))
                behind=$((behind + 0))
                ;;
            '1 '*|'2 '*)            ((modified++)) ;;
            '? '*)                  ((untracked++)) ;;
        esac
    done <<< "$status_output"

    # Get stash count (separate, cheaper operation)
    stashed=$(git -C "$(dirname "$git_dir")" stash list 2>/dev/null | wc -l)

    # Build status string
    local status_str="⎇ ${branch}"
    (( ahead > 0 )) && status_str+=" ↑${ahead}"
    (( behind > 0 )) && status_str+=" ↓${behind}"
    (( modified > 0 )) && status_str+=" ✚${modified}"
    (( untracked > 0 )) && status_str+=" …${untracked}"
    (( stashed > 0 )) && status_str+=" ≡${stashed}"

    # Update cache
    GIT_STATUS_CACHE["$cache_key"]="$status_str"
    GIT_STATUS_TIME["$cache_key"]="$current_time"
    echo "$status_str"
}

# ------------------------------------------------------------------------------
# SECTION 2: GIT ALIASES
# ------------------------------------------------------------------------------
_setup_git_aliases() {
    alias gst='git status'
    alias gco='git checkout'
    alias gbr='git branch'
    alias gpl='git pull'
    alias gps='git push'
    alias gl="git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"
    alias gd='git diff'
    alias gdc='git diff --cached'
    alias ga='git add'
    alias gaa='git add -A'
    alias gap='git add -p'
    alias gcm='git commit -m'
    alias gbd='git branch -d'
    alias gbD='git branch -D'
    alias gcb='git checkout -b'
    alias grv='git remote -v'
}

# ------------------------------------------------------------------------------
# SECTION 3: SERVICE INTEGRATION
# ------------------------------------------------------------------------------
git_service_init() {
    _setup_git_aliases
    log_info "Git service initialized"
}

git_service_cleanup() {
    # Remove aliases specifically defined by this service
    unalias gst gco gbr gpl gps gl gd gdc ga gaa gap gcm gbd gbD gcb grv 2>/dev/null

    # Clear caches
    GIT_STATUS_CACHE=()
    GIT_STATUS_TIME=()

    log_info "Git service stopped"
}

# ------------------------------------------------------------------------------
# SECTION 4: SERVICE REGISTRATION
# ------------------------------------------------------------------------------
service_register "git" \
    "git_service_init" \
    "git_service_cleanup" \
    "utility"

# Declare dependency on the config service for cache TTL settings
SERVICE_DEPENDENCIES["git"]="config"

# ------------------------------------------------------------------------------
# SECTION 5: NAMESPACE PROTECTION
# ------------------------------------------------------------------------------
readonly -f git_service_get_status _setup_git_aliases git_service_init git_service_cleanup
