#!/usr/bin/env python3
"""Tkinter launcher for Patreon TV box."""

from __future__ import annotations

import os
import socket
import subprocess
import tkinter as tk
from typing import Optional


POLL_INTERVAL_MS = 1000  # How often to poll for IP address
PATREON_URL = "https://www.patreon.com/home"


def get_ip_address() -> Optional[str]:
    """Return the LAN IP address or ``None`` if not available."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # Connect to an external host; we don't actually send data
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except OSError:
        return None


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

    poll_ip()
    root.mainloop()


if __name__ == "__main__":
    main()
