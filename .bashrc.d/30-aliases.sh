#!/bin/bash
# ==============================================================================
# Aliases Service
#
# Filename: 30-aliases.sh
# Purpose:  Defines common aliases for system navigation and operations.
#           Safe for re-sourcing. Depends on core service.
# ==============================================================================

[[ $- != *i* ]] && return

if ! declare -f service_register >/dev/null; then
    echo "Error: Aliases service requires core service" >&2
    return 1
fi

log_info "Loading aliases service"

# ------------------------------------------------------------------------------
# ALIAS INITIALIZATION
# ------------------------------------------------------------------------------
aliases_service_init() {
    # Configuration editing
    alias bashrc='nvim ~/.bashrc'
    alias bashd='nvim ~/.bashrc.d/'
    alias init_lua='nvim ~/.config/nvim/init.lua'
    alias reload='source ~/.bashrc && echo "Configuration reloaded"'

    # Safety features
    alias rm='rm -i'
    alias cp='cp -i'
    alias mv='mv -i'
    alias ln='ln -i'

    # Navigation
    alias ls='ls --color=auto --group-directories-first'
    alias la='ls -a'
    alias ll='ls -alFh'
    alias l='ls -CF'
    alias dus='du -sh * | sort -rh'
    alias tree='tree -C'
    alias ..='cd ..'
    alias ...='cd ../..'
    alias ....='cd ../../..'

    # System operations
    alias update='sudo apt update && sudo apt upgrade -y'
    alias psg='ps aux | grep -v grep | grep -i'
    alias df='df -h'
    alias free='free -h'
    alias ipa='ip -c a'
    alias myip='curl -s ifconfig.me; echo'

    # WSL-specific
    if grep -qi microsoft /proc/version; then
        alias explorer='explorer.exe .'
        alias winpath='wslpath -w'
    fi

    log_info "Aliases service initialized"
}

# ------------------------------------------------------------------------------
# SERVICE CLEANUP
# ------------------------------------------------------------------------------
aliases_service_cleanup() {
    # Specifically unalias only the aliases defined by this service for safety.
    unalias bashrc bashd vimrc reload \
            rm cp mv ln \
            ls la ll l dus tree \
            .. ... .... \
            update psg df free ipa myip \
            explorer winpath 2>/dev/null
    log_info "Aliases service stopped"
}

# ------------------------------------------------------------------------------
# SERVICE REGISTRATION
# ------------------------------------------------------------------------------
service_register "aliases" \
    "aliases_service_init" \
    "aliases_service_cleanup" \
    "utility"

# ------------------------------------------------------------------------------
# NAMESPACE PROTECTION
# ------------------------------------------------------------------------------
readonly -f aliases_service_init aliases_service_cleanup
