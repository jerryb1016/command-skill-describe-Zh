#!/bin/bash
# Install script for OpenCode Skills ZH

INSTALL_DIR="$HOME/.config/opencode/skills/describe-zh"

mkdir -p "$INSTALL_DIR"
cp -r . "$INSTALL_DIR/"

echo "Installed describe-zh to $INSTALL_DIR"