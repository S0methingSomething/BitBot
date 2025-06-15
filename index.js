import express from 'express';
import { runBotLogic } from './reddit-bot.js';

const app = express();
const port = 3000;

// This is the main endpoint that UptimeRobot will ping.
app.get('/', async (req, res) => {
  console.log(`[${new Date().toISOString()}] Received a ping. Starting bot logic...`);
  
  // Respond to the ping immediately so it doesn't time out.
  res.status(202).send('Accepted: Bot logic is now running in the background.');

  // Run the actual bot logic asynchronously.
  try {
    await runBotLogic();
    console.log(`[${new Date().toISOString()}] Bot logic finished successfully.`);
  } catch (error) {
    console.error(`[${new Date().toISOString()}] An error occurred during bot execution:`, error.message);
  }
});

app.listen(port, () => {
  console.log(`Bot server listening on port ${port}...`);
});
