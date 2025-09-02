#!/usr/bin/env python3
"""Launch Chromium to Patreon for the TV box.

The script waits for basic network connectivity and then opens Chromium to
the Patreon homepage.  Kiosk mode is used by default so the browser fills the
screen, but setting ``PATRON_FIRST_LOGIN=1`` disables kiosk mode to make the
initial Google sign-in easier.
"""

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
_CONNECTIVITY_CHECK_URL = "https://www.google.com"  # Any reliable site works

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
)


def wait_for_network(timeout: int = NETWORK_TIMEOUT) -> None:
    """Block until HTTP connectivity is available or the timeout expires."""
    end = time.time() + timeout
    while time.time() < end:
        try:
            urlopen(_CONNECTIVITY_CHECK_URL, timeout=5)
            logging.info("Network connectivity established")
            return
        except URLError:
            logging.info("Waiting for network...")
            time.sleep(1)
    logging.warning("Network not available after %s seconds", timeout)


def _find_chromium() -> str:
    """Return the first available Chromium executable."""
    for name in ("chromium", "chromium-browser"):
        path = shutil.which(name)
        if path:
            return path
    raise FileNotFoundError("Chromium executable not found")


def main() -> None:
    wait_for_network()

    cmd = [_find_chromium()]
    if os.getenv("PATRON_FIRST_LOGIN", "0") != "1":
        cmd.append("--kiosk")
    cmd.append(PATREON_URL)

    logging.info("Launching Chromium: %s", " ".join(cmd))
    try:
        subprocess.Popen(cmd)
        logging.info("Chromium launched")
    except Exception:  # pragma: no cover - log unexpected launch failures
        logging.exception("Failed to launch Chromium")


if __name__ == "__main__":
    main()

