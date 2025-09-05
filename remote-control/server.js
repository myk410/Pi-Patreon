const express = require('express');
const path = require('path');

const app = express();
const port = process.env.PORT || 3000;

// Serve static files from the public directory
app.use(express.static(path.join(__dirname, 'public')));

// Example handlers for remote control actions
app.post('/play', (req, res) => {
  console.log('Play');
  res.sendStatus(200);
});

app.post('/pause', (req, res) => {
  console.log('Pause');
  res.sendStatus(200);
});

app.post('/rewind', (req, res) => {
  console.log('Rewind');
  res.sendStatus(200);
});

app.post('/fast-forward', (req, res) => {
  console.log('Fast forward');
  res.sendStatus(200);
});

app.post('/skip-forward', (req, res) => {
  console.log('Skip forward 10s');
  res.sendStatus(200);
});

app.post('/skip-back', (req, res) => {
  console.log('Skip back 10s');
  res.sendStatus(200);
});

app.listen(port, () => {
  console.log(`Remote control server running at http://localhost:${port}`);
});
