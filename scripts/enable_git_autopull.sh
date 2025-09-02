#!/usr/bin/env bash
set -euo pipefail

# Install and enable systemd timer for automatic git pull

REPO_DIR="${REPO_DIR:-/home/myk410/Pi-Patreon}"
SERVICE_DST="/etc/systemd/system/patreon-pull.service"
TIMER_DST="/etc/systemd/system/patreon-pull.timer"

sudo sed "s#/home/myk410/Pi-Patreon#$REPO_DIR#g" systemd/patreon-pull.service | sudo tee "$SERVICE_DST" >/dev/null
sudo cp systemd/patreon-pull.timer "$TIMER_DST"

sudo systemctl daemon-reload
sudo systemctl enable --now patreon-pull.timer

echo "Git auto-pull timer enabled"
