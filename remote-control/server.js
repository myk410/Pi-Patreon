// /home/myk410/Pi-Patreon/remote-control/server.js
const express = require("express");
const path = require("path");
const { exec } = require("child_process");

const app = express();
const PORT = process.env.PORT || 3000;
const HOST = process.env.HOST || "0.0.0.0"; // listen on all interfaces

// Serve the static control page from the public directory
app.use(express.static(path.join(__dirname, "public")));

// Default environment for xdotool when launched outside a desktop session.
// Using DISPLAY=:0 targets the primary X server on Raspberry Pi OS.
const X_ENV = {
  DISPLAY: process.env.DISPLAY || ":0",
  XAUTHORITY: process.env.XAUTHORITY || "/home/pi/.Xauthority",
};

// Locate the first visible Chromium window. Chromium on Raspberry Pi may
// expose different WM_CLASS values (e.g. "chromium", "Chromium", or
// "chromium-browser"). We try a few known variants and use the first result.
function findChromiumWindow(cb) {
  const classes = ["chromium", "Chromium", "chromium-browser"];
  const tryNext = (i) => {
    if (i >= classes.length) return cb(new Error("Chromium window not found"));
    const cmd = `xdotool search --onlyvisible --class ${classes[i]} | head -n 1`;
    exec(cmd, { env: { ...process.env, ...X_ENV } }, (err, stdout) => {
      const id = stdout && stdout.trim();
      if (!err && id) {
        cb(null, id);
      } else {
        tryNext(i + 1);
      }
    });
  };
  tryNext(0);
}

// Helper to send keystrokes to Chromium using xdotool
function key(key, res) {
  findChromiumWindow((winErr, id) => {
    if (winErr) {
      console.error("xdotool search error:", winErr.message);
      return res.status(500).json({ ok: false, error: winErr.message });
    }
    const cmd = `xdotool key --window ${id} ${key}`;
    exec(cmd, { env: { ...process.env, ...X_ENV } }, (err, stdout, stderr) => {
      if (err) {
        console.error("xdotool error:", err.message || err, stderr);
        return res.status(500).json({
          ok: false,
          error: err.message || String(err),
        });
      }
      res.json({ ok: true });
    });
  });
}

// Control endpoints
// Control endpoints map simple button presses to YouTube-style shortcuts.
// Many embedded Patreon videos use the same key bindings.
app.post("/play",         (_, res) => key("k", res));
app.post("/pause",        (_, res) => key("k", res));
app.post("/play-pause",   (_, res) => key("k", res));
app.post("/rewind",       (_, res) => key("Left", res)); // 5 seconds back
app.post("/fast-forward", (_, res) => key("Right", res)); // 5 seconds forward
app.post("/skip-back",    (_, res) => key("j", res)); // 10 seconds back
app.post("/skip-forward", (_, res) => key("l", res)); // 10 seconds forward
app.post("/toggle-fullscreen", (_, res) => key("f", res));

// Start server
app.listen(PORT, HOST, () => {
  console.log(`Remote control server running at http://${HOST}:${PORT}`);
});
