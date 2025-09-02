#!/usr/bin/env python3
"""Launch Chromium to Patreon for the TV box (Pi + VNC/desktop)."""

from __future__ import annotations

import os
import shutil
import subprocess
import time
import logging
from urllib.error import URLError
from urllib.request import urlopen

PATREON_URL = "https://www.patreon.com/home"
NETWORK_TIMEOUT = int(os.getenv("NETWORK_TIMEOUT", "60"))
CONNECTIVITY_CHECK_URL = "https://www.google.com"
LOG_PATH = os.path.join(os.path.dirname(__file__), "launcher.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    handlers=[logging.FileHandler(LOG_PATH), logging.StreamHandler()],
)

def wait_for_network(timeout: int = NETWORK_TIMEOUT) -> None:
    end = time.time() + timeout
    while time.time() < end:
        try:
            urlopen(CONNECTIVITY_CHECK_URL, timeout=5)
            logging.info("Network connectivity established")
            return
        except URLError:
            logging.info("Waiting for network...")
            time.sleep(1)
    logging.warning("Network not available after %s seconds", timeout)

def find_chromium() -> str:
    for name in ("chromium", "chromium-browser"):
        path = shutil.which(name)
        if path:
            logging.info("Using browser binary: %s", path)
            return path
    raise FileNotFoundError("Chromium executable not found (install 'chromium').")


def nudge_window() -> None:
    """Move Chromium to (0,0) and maximize if tools available."""
    if not shutil.which("xdotool") or not shutil.which("wmctrl"):
        logging.info("xdotool or wmctrl not available; skipping window adjustment")
        return

    end = time.time() + 5
    window_id: str | None = None
    while time.time() < end:
        try:
            result = subprocess.run(
                ["xdotool", "search", "--onlyvisible", "--class", "Chromium"],
                capture_output=True,
                text=True,
                check=False,
            )
            ids = [line.strip() for line in result.stdout.splitlines() if line.strip()]
            if ids:
                window_id = ids[0]
                break
        except Exception:
            break
        time.sleep(0.5)

    if not window_id:
        logging.info("Chromium window not found for adjustment")
        return

    subprocess.run(["wmctrl", "-ir", window_id, "-e", "0,0,0,-1,-1"], check=False)
    subprocess.run(
        ["wmctrl", "-ir", window_id, "-b", "add,maximized_horz,maximized_vert"],
        check=False,
    )

def main() -> None:
    # Don’t try to open a GUI unless we’re in a desktop session
    if not os.environ.get("DISPLAY"):
        logging.warning("No DISPLAY; desktop session not ready. Skipping launch.")
        return

    wait_for_network()

    browser = find_chromium()
    kiosk = os.getenv("PATRON_KIOSK") == "1"
    fullscreen = os.getenv("PATRON_FULLSCREEN", "1") == "1"

    cmd = [
        browser,
        "--no-first-run",
        "--no-default-browser-check",
        "--password-store=basic",
    ]
    if kiosk:
        cmd.append("--kiosk")
    else:
        if fullscreen:
            cmd.append("--start-fullscreen")
        else:
            cmd.extend(["--start-maximized", "--window-position=0,0"])
    cmd.append(PATREON_URL)

    logging.info("Launching Chromium: %s", " ".join(cmd))
    try:
        with open(LOG_PATH, "a") as log_file:
            subprocess.Popen(cmd, stdout=log_file, stderr=log_file)
        logging.info("Chromium launched")
    except Exception:
        logging.exception("Failed to launch Chromium")

    if not kiosk and not fullscreen:
        nudge_window()

if __name__ == "__main__":
    main()
