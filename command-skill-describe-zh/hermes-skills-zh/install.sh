#!/bin/bash
# Install script for Hermes Skills ZH

INSTALL_DIR="$HOME/.hermes/skills/describe-zh"

mkdir -p "$INSTALL_DIR"

# Copy all files
cp -r . "$INSTALL_DIR/"

echo "Installed describe-zh to $INSTALL_DIR"
echo "Restart Hermes to use the skill."
