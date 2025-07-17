#!/bin/bash
# ==============================================================================
# Dotfiles Installer
#
# This script creates symlinks from the home directory to the files in this
# repository. It also backs up any existing dotfiles.
# ==============================================================================

set -e # Exit immediately if a command exits with a non-zero status.

# Variables
DOTFILES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="$HOME"
BACKUP_DIR="$TARGET_DIR/.dotfiles_backup_$(date +%Y%m%d_%H%M%S)"

# Files and directories to link
# Format: "repo_path:target_path"
LINKS=(
    "profile:.profile"
    "bashrc:.bashrc"
    ".bashrc.d:.bashrc.d"
    "config/nvim:.config/nvim"jk
)

# --- Main Logic ---
echo "🚀 Starting dotfiles installation..."
mkdir -p "$BACKUP_DIR"
echo "Backups will be stored in: $BACKUP_DIR"

for link_pair in "${LINKS[@]}"; do
    IFS=":" read -r source_file target_file <<< "$link_pair"

    SOURCE_PATH="$DOTFILES_DIR/$source_file"
    TARGET_PATH="$TARGET_DIR/$target_file"

    # If the target exists, is not a link, or points elsewhere, back it up
    if [ -e "$TARGET_PATH" ] && [ ! -L "$TARGET_PATH" ]; then
        echo "  -> Backing up existing $TARGET_PATH to $BACKUP_DIR"
        mv "$TARGET_PATH" "$BACKUP_DIR/"
    elif [ -L "$TARGET_PATH" ] && [ "$(readlink "$TARGET_PATH")" != "$SOURCE_PATH" ]; then
        echo "  -> Removing incorrect symlink at $TARGET_PATH"
        rm "$TARGET_PATH"
    fi

    # Create the symlink if it doesn't exist
    if [ ! -e "$TARGET_PATH" ]; then
        echo "  -> Linking $SOURCE_PATH to $TARGET_PATH"
        ln -s "$SOURCE_PATH" "$TARGET_PATH"
    else
        echo "  -> Link for $target_file already correct. Skipping."
    fi
done

echo "✅ Installation complete! Please restart your shell or run 'source ~/.bashrc'."
