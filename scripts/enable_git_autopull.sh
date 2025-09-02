#!/usr/bin/env bash
set -euo pipefail

# Install and enable systemd timer for automatic git pull

REPO_DIR="${REPO_DIR:-/home/pi/patreon-tv-box}"
SERVICE_DST="/etc/systemd/system/patreon-pull.service"
TIMER_DST="/etc/systemd/system/patreon-pull.timer"

sudo sed "s#/home/pi/patreon-tv-box#$REPO_DIR#g" systemd/patreon-pull.service | sudo tee "$SERVICE_DST" >/dev/null
sudo cp systemd/patreon-pull.timer "$TIMER_DST"

sudo systemctl daemon-reload
sudo systemctl enable --now patreon-pull.timer

echo "Git auto-pull timer enabled"
