#!/bin/bash
# Wrapper to run the Patreon launcher with environment variables

# Force fullscreen (like F11) by default
export PATRON_FULLSCREEN=1

# Optional: how long to wait for network before giving up
export NETWORK_TIMEOUT=60

# Path to your launcher.py
SCRIPT_DIR="/home/myk410/Pi-Patreon/app"

cd "$SCRIPT_DIR" || exit 1

# Run the launcher
/usr/bin/python3 launcher.py
