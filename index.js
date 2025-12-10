const express = require("express");
const axios = require("axios");

const app = express();
app.use(express.json());

const VERIFY_TOKEN = process.env.VERIFY_TOKEN || "YOUR_VERIFY_TOKEN";
const MAKE_WEBHOOK_URL = process.env.MAKE_WEBHOOK_URL || "https://hook.eu2.make.com/m47yrjmw2h0f4w8do4am6sgr6kzccmyy";

app.get("/webhook", (req, res) => {
  const mode = req.query["hub.mode"];
  const token = req.query["hub.verify_token"];
  const challenge = req.query["hub.challenge"];

  if (mode && token === VERIFY_TOKEN) {
    res.status(200).send(challenge);
  } else {
    res.sendStatus(403);
  }
});

app.post("/webhook", async (req, res) => {
  const data = req.body;
  console.log("Received payload:", data);

  try {
    await axios.post(MAKE_WEBHOOK_URL, data);
  } catch (err) {
    console.error("Error sending to Make.com:", err);
  }

  res.status(200).send("EVENT_RECEIVED");
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Webhook server running on port ${PORT}`);
});
