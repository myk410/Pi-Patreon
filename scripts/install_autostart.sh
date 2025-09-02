#!/usr/bin/env bash
set -euo pipefail

# Install autostart entry for launcher.py

PI_HOME="${PI_HOME:-/home/pi}"
AUTOSTART_DIR="$PI_HOME/.config/autostart"
DESKTOP_FILE="$AUTOSTART_DIR/launcher.desktop"

mkdir -p "$AUTOSTART_DIR"

cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Type=Application
Name=Patreon Launcher
Exec=python3 $PI_HOME/patreon-tv-box/app/launcher.py
X-GNOME-Autostart-enabled=true
EOF

echo "Created $DESKTOP_FILE"
