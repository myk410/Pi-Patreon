// /home/myk410/Pi-Patreon/remote-control/server.js
const express = require("express");
const path = require("path");
const { exec } = require("child_process");

const app = express();
const PORT = process.env.PORT || 3000;
const HOST = process.env.HOST || "0.0.0.0"; // listen on all interfaces

// Serve the static control page from the public directory
app.use(express.static(path.join(__dirname, "public")));

// Helper to send keystrokes to Chromium using xdotool
function key(key, res) {
  const cmd = `xdotool key --window $(xdotool search --onlyvisible --class chromium | head -n 1) ${key}`;
  exec(cmd, (err, stdout, stderr) => {
    if (err) {
      console.error("xdotool error:", err.message || err, stderr);
      return res.status(500).json({
        ok: false,
        error: err.message || String(err)
      });
    }
    res.json({ ok: true });
  });
}

// Control endpoints
app.post("/play",         (_, res) => key("space", res));
app.post("/pause",        (_, res) => key("space", res));
app.post("/play-pause",   (_, res) => key("space", res));
app.post("/rewind",       (_, res) => key("Left", res));
app.post("/fast-forward", (_, res) => key("Right", res));
app.post("/skip-back",    (_, res) => key("Shift+Left", res));
app.post("/skip-forward", (_, res) => key("Shift+Right", res));
app.post("/toggle-fullscreen", (_, res) => key("f", res));

// Start server
app.listen(PORT, HOST, () => {
  console.log(`Remote control server running at http://${HOST}:${PORT}`);
});
