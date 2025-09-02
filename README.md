# Patreon TV Box (Raspberry Pi 5)

Turn your Raspberry Pi 5 into a Patreon TV box.

**Features:**
- On login, a popup shows your Pi’s LAN IP and an **Open Patreon** button.
- Clicking the button closes the popup and launches Chromium in fullscreen kiosk mode to Patreon.
- Supports Google Sign-In by keeping Chromium’s profile intact between sessions.
- Remote control the Pi from iPhone or Mac via VNC.
- Auto-sync with this GitHub repo using a systemd timer.

---

## How It Works
1. Pi boots to Desktop.
2. Tkinter popup (`launcher.py`) appears, showing the IP address.
3. The **Open Patreon** button is disabled until a valid IP is detected.
4. Clicking the button:
   - Closes the popup
   - Launches Chromium in kiosk mode to `https://www.patreon.com/home`
5. Videos play fullscreen on your TV via HDMI.
6. If the Git auto-pull timer is enabled, changes to this repo will appear on the Pi within 60 seconds.

---

## Requirements
- Raspberry Pi OS (Bookworm) with Desktop
- Raspberry Pi 5 with HDMI to TV
- Network connection
- Git
- Python 3.11+ with Tkinter
- Chromium browser

---

## Installation
1. Install dependencies:
   ```bash
   sudo apt update
   sudo apt install -y git python3-tk chromium-browser
   ```
2. Set up autostart, VNC and git auto-pull:
   ```bash
   bash scripts/install_autostart.sh
   bash scripts/setup_vnc.sh
   bash scripts/enable_git_autopull.sh
   ```
