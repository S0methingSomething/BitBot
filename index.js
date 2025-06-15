import 'dotenv/config';
import express from 'express';
import { fetchLatestReleaseInfo } from './fetch-release-info.js';
import { runRedditLogic } from './reddit-bot.js';

// Load all configuration from environment variables
const config = {
    PORT: process.env.PORT || 3000,
    REDDIT_CLIENT_ID: process.env.REDDIT_CLIENT_ID,
    REDDIT_CLIENT_SECRET: process.env.REDDIT_CLIENT_SECRET,
    REDDIT_USERNAME: process.env.REDDIT_USERNAME,
    REDDIT_PASSWORD: process.env.REDDIT_PASSWORD,
    REDDIT_SUBREDDIT: process.env.REDDIT_SUBREDDIT,
    REDDIT_USER_AGENT: process.env.REDDIT_USER_AGENT || `bot:BitBot/3.0 (by u/${process.env.REDDIT_USERNAME})`,
};

// This is the core task the bot performs
async function runFullBotProcess() {
    console.log("--- Starting Full Bot Process ---");
    const releaseInfo = await fetchLatestReleaseInfo();
    const result = await runRedditLogic(config, releaseInfo);
    return result;
}

// Check if this is being run in a server environment like Replit or Vercel
// VERCEL_URL is a system-provided environment variable on Vercel
// REPL_ID is a system-provided environment variable on Replit
if (process.env.VERCEL || process.env.REPL_ID) {
    // --- SERVER MODE (for Vercel/Replit) ---
    const app = express();
    
    // The main endpoint for cron jobs or pings
    app.get('/', async (req, res) => {
        console.log(`[${new Date().toISOString()}] Server received a request. Starting bot...`);
        try {
            const result = await runFullBotProcess();
            res.status(200).send(`Bot run finished. Result: ${result}`);
        } catch (error) {
            console.error(`[${new Date().toISOString()}] Bot run failed:`, error.message);
            res.status(500).send(`Bot run failed: ${error.message}`);
        }
    });
    
    // For Vercel, we export the app instance.
    // For Replit, it needs to listen on a port.
    if (process.env.REPL_ID) {
        app.listen(config.PORT, () => {
            console.log(`Server listening on port ${config.PORT}...`);
        });
    }

    // For Vercel, the file needs to export the express app
    // Note: If deploying to Vercel, rename this file to /api/index.js
    export default app;

} else {
    // --- LOCAL MODE (for Termux/PC) ---
    console.log("No server environment detected. Running script once locally.");
    runFullBotProcess().catch(err => {
        console.error("Local run failed.");
        process.exit(1);
    });
}
