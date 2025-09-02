#!/usr/bin/env python3
"""Launch Chromium to Patreon for the TV box (Pi + VNC/desktop).

Defaults to fullscreen (like pressing F11) but NOT kiosk, so site UI remains.
Set PATRON_FULLSCREEN=0 to start as a normal window (maximized, positioned at 0,0).
"""

from __future__ import annotations

import os
import shutil
import subprocess
import time
import logging
from urllib.error import URLError
from urllib.request import urlopen
from typing import Optional

PATREON_URL = "https://www.patreon.com/home"
NETWORK_TIMEOUT = int(os.getenv("NETWORK_TIMEOUT", "60"))
CONNECTIVITY_CHECK_URL = "https://www.google.com"
LOG_PATH = os.path.join(os.path.dirname(__file__), "launcher.log")


def _env_bool(name: str, default: bool) -> bool:
    v = os.getenv(name)
    if v is None:
        return default
    return v.strip() in ("1", "true", "TRUE", "yes", "YES", "on", "ON")


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    handlers=[logging.FileHandler(LOG_PATH), logging.StreamHandler()],
)


def wait_for_network(timeout: int = NETWORK_TIMEOUT) -> None:
    """Block until HTTP connectivity is available or the timeout expires."""
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
    """Return path to Chromium executable."""
    for name in ("chromium", "chromium-browser"):
        path = shutil.which(name)
        if path:
            logging.info("Using browser binary: %s", path)
            return path
    raise FileNotFoundError("Chromium executable not found (install 'chromium').")


def build_cmd(browser: str, fullscreen: bool) -> list[str]:
    """Build the Chromium command."""
    cmd = [
        browser,
        "--no-first-run",
        "--no-default-browser-check",
        "--password-store=basic",
    ]
    if fullscreen:
        # F11-style fullscreen with UI available on exit
        cmd.append("--start-fullscreen")
    else:
        # Normal window; try to keep it on-screen and big
        cmd += ["--start-maximized", "--window-position=0,0"]
    cmd.append(PATREON_URL)
    return cmd


def main() -> None:
    # Only launch in a desktop/X11 session
    display = os.environ.get("DISPLAY")
    if not display:
        logging.warning("No DISPLAY; desktop session not ready. Skipping launch.")
        return
    logging.info("DISPLAY detected: %s (XDG_DESKTOP=%s)", display, os.getenv("XDG_CURRENT_DESKTOP", ""))

    wait_for_network()

    try:
        browser = find_chromium()
    except FileNotFoundError as e:
        logging.error(str(e))
        return

    fullscreen = _env_bool("PATRON_FULLSCREEN", True)  # default ON
    # Keep kiosk OFF unless you explicitly reintroduce it elsewhere
    cmd = build_cmd(browser, fullscreen)

    logging.info("Launching Chromium: %s", " ".join(cmd))
    try:
        with open(LOG_PATH, "a") as log_file:
            subprocess.Popen(cmd, stdout=log_file, stderr=log_file)
        logging.info("Chromium launched")
    except Exception:
        logging.exception("Failed to launch Chromium")


if __name__ == "__main__":
    main()
