import { fetchLatestReleaseInfo } from './fetch-release-info.js';
import { runRedditLogic } from './reddit-bot.js';
import { getProxyList } from './proxy-manager.js';

const MAX_RETRIES = 5; // Try up to 5 different proxies before giving up.

export async function runFullBotProcess() {
    console.log("--- Starting Full Bot Process ---");
    const config = {
        REDDIT_CLIENT_ID: process.env.REDDIT_CLIENT_ID,
        REDDIT_CLIENT_SECRET: process.env.REDDIT_CLIENT_SECRET,
        REDDIT_USERNAME: process.env.REDDIT_USERNAME,
        REDDIT_PASSWORD: process.env.REDDIT_PASSWORD,
        REDDIT_SUBREDDIT: process.env.REDDIT_SUBREDDIT,
        REDDIT_USER_AGENT: process.env.REDDIT_USER_AGENT || `bot:BitBot/4.0 (by u/${process.env.REDDIT_USERNAME})`,
    };

    const proxies = await getProxyList();
    const attempts = [...proxies, null]; // Add a direct connection attempt as the final fallback

    for (let i = 0; i < MAX_RETRIES && i < attempts.length; i++) {
        const proxy = attempts[i];
        try {
            console.log(`\n--- ATTEMPT ${i + 1}/${MAX_RETRIES} ---`);
            if (proxy) {
                console.log(`Using proxy: ${proxy}`);
            } else {
                console.log("Attempting direct connection (no proxy).");
            }
            
            const releaseInfo = await fetchLatestReleaseInfo(proxy);
            const result = await runRedditLogic(config, releaseInfo, proxy);
            
            console.log("--- BOT RUN SUCCEEDED ---");
            return result;
        
        } catch (error) {
            console.error(`Attempt ${i + 1} failed: ${error.message}`);
            if (i === MAX_RETRIES - 1) {
                console.error("All proxy attempts failed. The bot could not complete its task.");
                throw error;
            }
        }
    }
}
