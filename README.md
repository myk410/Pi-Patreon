# Patreon TV Box (Raspberry Pi 5)

Turn your Raspberry Pi 5 into a Patreon TV box.

**Features:**
- On login, Chromium automatically launches to Patreon (fullscreen by default).
- Supports Google Sign-In by keeping Chromium’s profile intact between sessions.
- Remote control the Pi from iPhone or Mac via VNC.
- Auto-sync with this GitHub repo using a systemd timer.

---

## How It Works
1. Pi boots to Desktop.
2. `launcher.py` waits for network connectivity and then launches Chromium to `https://www.patreon.com/home`.
   - `PATRON_FULLSCREEN` (default `1`) controls fullscreen; set to `0` for a normal window.
   - `PATRON_KIOSK=1` launches in kiosk mode.
   - Adjust `NETWORK_TIMEOUT` (seconds) if your connection takes longer to come up.
3. Videos play on your TV via HDMI.
4. If the Git auto-pull timer is enabled, changes to this repo will appear on the Pi within 60 seconds.

---

## Requirements
- Raspberry Pi OS (Bookworm) with Desktop
- Raspberry Pi 5 with HDMI to TV
- Network connection
- Git
- Python 3.11+
- Chromium browser

---

## Installation
1. Install dependencies:
   ```bash
   sudo apt update
   sudo apt install -y git python3 chromium-browser
   ```
2. Set up autostart, VNC and git auto-pull:
   ```bash
   bash scripts/install_autostart.sh
   bash scripts/setup_vnc.sh
   bash scripts/enable_git_autopull.sh
   ```
