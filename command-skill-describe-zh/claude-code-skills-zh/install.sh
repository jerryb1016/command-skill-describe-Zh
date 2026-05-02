#!/bin/bash
# Install script for Claude Code Skills ZH

INSTALL_DIR="$HOME/.claude/skills/describe-zh"

mkdir -p "$INSTALL_DIR"

# Copy all files
cp -r . "$INSTALL_DIR/"

echo "Installed describe-zh to $INSTALL_DIR"
echo "Restart Claude Code to use the skill."