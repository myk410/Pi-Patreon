#!/usr/bin/env python3
"""Simplified launcher for the Patreon TV box.

This script waits briefly for network connectivity and then launches
Chromium to Patreon.  The previous Tkinter popup and IP display have
been removed because the device now uses a static IP address.
"""

from __future__ import annotations

import os
import socket
import subprocess
import time


NETWORK_WAIT_SECONDS = 15
PATREON_URL = "https://www.patreon.com/home"


def wait_for_network() -> None:
    """Block until basic network connectivity is available or timeout."""
    for _ in range(NETWORK_WAIT_SECONDS):
        try:
            with socket.create_connection(("8.8.8.8", 80), timeout=1):
                return
        except OSError:
            time.sleep(1)


def main() -> None:
    wait_for_network()

    kiosk = os.getenv("PATRON_FIRST_LOGIN", "0") != "1"
    cmd = ["chromium-browser"]
    if kiosk:
        cmd.append("--kiosk")
    cmd.append(PATREON_URL)

    subprocess.Popen(cmd)


if __name__ == "__main__":
    main()

