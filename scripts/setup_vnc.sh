#!/usr/bin/env bash
set -euo pipefail

# Enable VNC and show connection info

sudo raspi-config nonint do_vnc 0

IP=$(hostname -I | awk '{print $1}')
echo "VNC enabled. Connect using ${IP}:5901"
