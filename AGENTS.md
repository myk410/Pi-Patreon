# Agents Guide

## Project Name
Patreon TV Box (Raspberry Pi 5)

## High-Level Goal
Turn a Raspberry Pi 5 into a “Patreon TV box”:
- On login, **launch Chromium in fullscreen kiosk mode to Patreon** (using a stored Google login session)
- Support Google Sign-In by reusing Chromium’s persisted profile/session
- Allow remote control of the Pi from an iPhone via **VNC**
- Keep the Pi **in sync with GitHub** using an auto-pull timer

---

## Updated UX Flow
1. Raspberry Pi boots to Desktop.
2. `launcher.py` waits for network connectivity and launches Chromium with:
   ```bash
   chromium-browser --kiosk https://www.patreon.com/home
   ```
   - Uses the existing Chromium profile so Google login persists
   - If the user is not signed in, the agent should open normal (non-kiosk) Chromium for the first login, then kiosk mode thereafter.
3. User watches Patreon content fullscreen on TV via HDMI.
4. Remote control via VNC is available from iPhone/Mac.

---

## Repository Structure
/ (root)
├─ agents.md                 # This file
├─ README.md                 # Project documentation
├─ app/
│  └─ launcher.py            # Main script: launches Chromium on boot
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

---

## Conventions
- **Branching:** `main` is always deployable; feature branches merged via PR.
- **Commits:** Use Conventional Commits style (`feat:`, `fix:`, `docs:`, etc.).
- **Shell scripts:** `bash`, with `set -euo pipefail`, include inline comments.
- **Python:** 3.11+, standard library only (`subprocess` to launch Chromium).
- **Paths:** Assume user `pi`, home `/home/pi`, but make configurable via env vars where possible.

---

## Environment Assumptions
- Raspberry Pi OS (Bookworm) **with Desktop**
- Pi 5 connected via HDMI to a TV
- Network via DHCP on the same LAN as controlling devices
- Chromium browser installed
- Git installed
- VNC server enabled (RealVNC preferred)
- Repository synced at `/home/myk410/Pi-Patreon`

---

## Tasks

### 1. Create `app/launcher.py`
- Wait for network connectivity (with a timeout)
- Launch Chromium to `https://www.patreon.com/home`
- Use kiosk mode unless `PATRON_FIRST_LOGIN=1`

### 2. Autostart `launcher.py` on login
- `scripts/install_autostart.sh`:
  - Creates `~/.config/autostart/launcher.desktop` with:
    ```ini
    [Desktop Entry]
    Type=Application
    Name=Patreon Launcher
    Exec=python3 /home/pi/patreon-tv-box/app/launcher.py
    X-GNOME-Autostart-enabled=true
    ```

### 3. Enable VNC
- `scripts/setup_vnc.sh`:
  - Runs `sudo raspi-config nonint do_vnc 0`
  - Prints IP and VNC connection info

### 4. Auto-pull from GitHub
- `systemd/patreon-pull.service`:
  - Runs `git pull --ff-only` in `/home/pi/patreon-tv-box`
- `systemd/patreon-pull.timer`:
  - Runs service every 60 seconds
- `scripts/enable_git_autopull.sh` installs and enables the timer

### 5. (Optional) Push-based deploy
- `.github/workflows/deploy.yml`:  
  - On push to `main`, rsync changes to Pi via SSH (requires repo secrets)

---

## Commands Agent May Run
```bash
sudo apt update
sudo apt install -y git python3 chromium-browser
bash scripts/install_autostart.sh
bash scripts/setup_vnc.sh
bash scripts/enable_git_autopull.sh
```
