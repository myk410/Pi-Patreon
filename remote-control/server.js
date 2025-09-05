cat > /home/myk410/Pi-Patreon/remote-control/server.js <<'EOF'
const express = require("express");
const path = require("path");
const { execFile } = require("child_process");

const app = express();
const PORT = process.env.PORT || 3000;
const HOST = process.env.HOST || "0.0.0.0"; // listen on LAN

app.use(express.static(path.join(__dirname, "public")));

function pc(args, res) {
  execFile("playerctl", ["--player=%any", ...args], (err, stdout, stderr) => {
    if (err) {
      console.error("playerctl error:", err.message || err, stderr);
      return res.status(500).json({ ok:false, error: err.message || String(err) });
    }
    res.json({ ok:true, out: stdout.trim() });
  });
}

app.post("/play",        (_, res) => pc(["play"], res));
app.post("/pause",       (_, res) => pc(["pause"], res));
app.post("/play-pause",  (_, res) => pc(["play-pause"], res));
app.post("/rewind",      (_, res) => pc(["position", "10-", "--"], res));
app.post("/fast-forward",(_, res) => pc(["position", "10+", "--"], res));
app.post("/skip-back",   (_, res) => pc(["position", "10-", "--"], res));
app.post("/skip-forward",(_, res) => pc(["position", "10+", "--"], res));

app.get("/players", (_, res) => {
  execFile("playerctl", ["-l"], (err, stdout, stderr) => {
    if (err) {
      console.error("playerctl -l error:", err.message || err, stderr);
      return res.json({ players: [] });
    }
    res.json({ players: stdout.trim().split("\n").filter(Boolean) });
  });
});

app.listen(PORT, HOST, () => {
  console.log(`Remote control server running at http://${HOST}:${PORT}`);
});
EOF
