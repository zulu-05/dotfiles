# ==============================================================================
# ~/.bashrc: Main Shell Configuration Loader
#
# This file serves as the master loader for an interactive Bash session.
# It sources core services and then delegates all functionality to modular
# scripts located in ~/.bashrc.d/
# ==============================================================================

# --- Sourcing Guard ---
# If this file has already been sourced, just stop.
# This prevents errors when a login shell sources .profile, which then sources .bashrc.
if [ -n "$BASHRC_SOURCED" ]; then
    return
fi
BASHRC_SOURCED=1

# --- Interactive Shell Guard ---
# Do not run the rest of this file for non-interactive shells
case "$-" in
    *i*) ;;
      *) return;;
esac

# --- Standard History Settings ---
HISTCONTROL=ignoreboth
shopt -s histappend
HISTSIZE=1000
HISTFILESIZE=2000

# --- Core Shell Configuration ---
# Check window size after each command
shopt -s checkwinsize

# Make less more powerful
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# --- Load Modular Services ---
# Source all .sh files from the .bashrc.d directory to register services.
# The subshell (...) isolates the 'file' variable during the loop.
if [ -d "$HOME/.bashrc.d" ]; then
    shopt -s nullglob
    for file in "$HOME/.bashrc.d/"*.sh; do
        if [ -f "$file" ] && [ -r "$file" ]; then
            # Source the file, capturing errors.
            if ! . "$file"; then
                echo "Warning: Failed to load $file" >&2
            fi
        fi
    done
fi
# Unset the loop variable from the parent shell's scope for cleanliness. [cite: 102]
unset file

# --- Initialize All Services ---
# Kick off the entire service architecture by starting the 'startup' coordinator.
# This single command handles dependency resolution and initialization for all services.
if declare -f service_start >/dev/null; then
    service_start "startup"
fi
