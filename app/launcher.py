#!/usr/bin/env python3
"""Tkinter launcher for Patreon TV box."""

from __future__ import annotations

import os
import socket
import subprocess
import time
import tkinter as tk
from typing import Optional


POLL_INTERVAL_MS = 1000  # How often to poll for IP address
NETWORK_WAIT_SECONDS = 15  # Max seconds to wait for network on startup
PATREON_URL = "https://www.patreon.com/home"


def get_ip_address() -> Optional[str]:
    """Return the Wi-Fi (wlan0) IP address or fall back to LAN.

    The function prefers the Wi-Fi interface but will return the
    default route's address if Wi-Fi is unavailable. ``None`` is
    returned when no network address can be determined.
    """
    try:
        output = subprocess.check_output(
            ["ip", "-4", "-o", "addr", "show", "wlan0"], text=True
        ).strip()
        if output:
            return output.split()[3].split("/")[0]
    except (subprocess.CalledProcessError, OSError, IndexError):
        print("ip command failed or wlan0 unavailable")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # Connect to an external host; we don't actually send data
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except OSError:
        return None


def wait_for_network() -> None:
    """Delay startup until a network address is available or timeout."""
    for _ in range(NETWORK_WAIT_SECONDS):
        if get_ip_address():
            return
        time.sleep(1)


def open_patreon(root: tk.Tk) -> None:
    """Close the popup and launch Chromium."""
    root.destroy()

    kiosk = os.getenv("PATRON_FIRST_LOGIN", "0") != "1"
    cmd = ["chromium-browser"]
    if kiosk:
        cmd.append("--kiosk")
    cmd.append(PATREON_URL)
    subprocess.Popen(cmd)


def main() -> None:
    wait_for_network()
    root = tk.Tk()
    root.title("Patreon Launcher")
    root.attributes("-topmost", True)

    ip_var = tk.StringVar(value="Detecting IP...")

    label = tk.Label(root, textvariable=ip_var, font=("Arial", 14))
    label.pack(padx=20, pady=10)

    button = tk.Button(root, text="Open Patreon", state=tk.DISABLED,
                       command=lambda: open_patreon(root))
    button.pack(pady=10)

    def poll_ip() -> None:
        ip = get_ip_address()
        if ip:
            ip_var.set(f"IP: {ip}")
            button.config(state=tk.NORMAL)
        else:
            ip_var.set("No network")
            button.config(state=tk.DISABLED)
        root.after(POLL_INTERVAL_MS, poll_ip)

    root.after(0, poll_ip)
    root.mainloop()


if __name__ == "__main__":
    main()
