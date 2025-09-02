# Agents Guide

## Project Name
Patreon TV Box (Raspberry Pi 5)

## High-Level Goal
Turn a Raspberry Pi 5 into a “Patreon TV box”:
- On login, **show a small popup with the Pi’s IP address first**
- When the user clicks the **Close / Open Patreon** button, **launch Chromium in fullscreen kiosk mode to Patreon** (using a stored Google login session)
- Support Google Sign-In by reusing Chromium’s persisted profile/session
- Allow remote control of the Pi from an iPhone via **VNC**
- Keep the Pi **in sync with GitHub** using an auto-pull timer

---

## Updated UX Flow
1. Raspberry Pi boots to Desktop.
2. **Popup window appears** (always on top) showing:
   - LAN IP address (auto-detected)
   - A disabled “Open Patreon” button until the IP is found
3. Once IP is available, **button becomes active**.
4. Clicking the button:
   - Closes the popup
   - Launches Chromium with:
     ```bash
     chromium-browser --kiosk https://www.patreon.com/home
     ```
     - Uses the existing Chromium profile so Google login persists
   - If the user is not signed in, the agent should open normal (non-kiosk) Chromium for the first login, then kiosk mode thereafter.
5. User watches Patreon content fullscreen on TV via HDMI.
6. Remote control via VNC is available from iPhone/Mac.

---

## Repository Structure
/ (root)
├─ agents.md                 # This file
├─ README.md                 # Project documentation
├─ app/
│  └─ launcher.py            # Main script: popup first → launches Chromium on button press
├─ scripts/
│  ├─ install_autostart.sh   # Installs single autostart entry for launcher.py
│  ├─ setup_vnc.sh           # Enables/configures VNC
│  ├─ enable_git_autopull.sh # Sets up systemd timer for git pull
├─ systemd/
│  ├─ patreon-pull.service
│  └─ patreon-pull.timer
└─ .github/
└─ workflows/
└─ deploy.yml          # Optional push-based deploy over SSH
