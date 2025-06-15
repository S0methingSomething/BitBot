import 'dotenv/config';
import express from 'express';
import { runFullBotProcess } from './run-bot.js';

const PORT = process.env.PORT || 3000;

// This file is the entrypoint for LOCAL and REPLIT deployments.
// It checks if it's in a server environment and acts accordingly.

if (process.env.REPL_ID) {
    // --- SERVER MODE (for Replit) ---
    const app = express();
    
    app.get('/', async (req, res) => {
        console.log(`[${new Date().toISOString()}] Replit server received a ping. Starting bot...`);
        // Respond immediately to the UptimeRobot ping
        res.status(202).send('Accepted: Bot process started in the background.');
        
        // Run the main logic without waiting for it to finish
        runFullBotProcess().catch(err => {
            console.error("Background bot run failed:", err.message);
        });
    });

    app.listen(PORT, () => {
        console.log(`Replit server listening on port ${PORT}. Ready for pings.`);
    });

} else {
    // --- LOCAL MODE (for Termux/PC) ---
    console.log("No server environment detected. Running script once locally.");
    runFullBotProcess().catch(err => {
        console.error("Local run failed.");
        process.exit(1);
    });
}
