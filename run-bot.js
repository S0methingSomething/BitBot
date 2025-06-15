import { fetchLatestReleaseInfo } from './fetch-release-info.js';
import { runRedditLogic } from './reddit-bot.js';

// This is the shared, core logic that both index.js and api/run.js will call.
export async function runFullBotProcess() {
    console.log("--- Starting Full Bot Process ---");
    const config = {
        REDDIT_CLIENT_ID: process.env.REDDIT_CLIENT_ID,
        REDDIT_CLIENT_SECRET: process.env.REDDIT_CLIENT_SECRET,
        REDDIT_USERNAME: process.env.REDDIT_USERNAME,
        REDDIT_PASSWORD: process.env.REDDIT_PASSWORD,
        REDDIT_SUBREDDIT: process.env.REDDIT_SUBREDDIT,
        REDDIT_USER_AGENT: process.env.REDDIT_USER_AGENT || `bot:BitBot/3.0 (by u/${process.env.REDDIT_USERNAME})`,
    };
    const releaseInfo = await fetchLatestReleaseInfo();
    const result = await runRedditLogic(config, releaseInfo);
    return result;
}
