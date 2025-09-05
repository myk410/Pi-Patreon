# Remote Control Server

Serves a simple web page that issues media control commands by sending
keystrokes to Chromium via `xdotool`.

## Usage

```bash
npm install
npm start
```

Open a browser to `http://<host>:3000` to use the remote control interface.

Requires [`xdotool`](https://github.com/jordansissel/xdotool) to be installed:

```bash
sudo apt install -y xdotool
```
