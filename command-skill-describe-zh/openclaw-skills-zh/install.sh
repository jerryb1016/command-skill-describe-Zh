#!/bin/bash
# Install script for OpenClaw Skills ZH

INSTALL_DIR="skills/describe-zh"

mkdir -p "$INSTALL_DIR"
cp -r . "$INSTALL_DIR/"

echo "Installed describe-zh to $INSTALL_DIR"