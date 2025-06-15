import axios from 'axios';
import semver from 'semver';
import fs from 'fs';

// --- Configuration & Constants ---
const {
    REDDIT_CLIENT_ID,
    REDDIT_CLIENT_SECRET,
    REDDIT_USERNAME,
    REDDIT_PASSWORD, // We need the password for this grant type
    REDDIT_USER_AGENT,
    REDDIT_SUBREDDIT,
    BITLIFE_VERSION,
    DOWNLOAD_URL,
    GITHUB_OUTPUT, 
} = process.env;

const TOKEN_URL = 'https://www.reddit.com/api/v1/access_token';
const API_BASE = 'https://oauth.reddit.com';

// (Helper functions like assertEnv, generatePostBody, etc. remain the same)
function assertEnv() {
    const required = { REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USERNAME, REDDIT_PASSWORD, REDDIT_USER_AGENT, REDDIT_SUBREDDIT, BITLIFE_VERSION, DOWNLOAD_URL };
    const missing = Object.keys(required).filter(key => !required[key]);
    if (missing.length > 0) throw new Error(`Missing required environment variables: ${missing.join(', ')}`);
    console.log("Environment configuration validated successfully.");
}
function generatePostBody() {
    return `This is an automated post by [BitBot](https://github.com/S0methingSomething/BitBot).\n\n` +
           `**Download link:** [MonetizationVars](${DOWNLOAD_URL})\n\n` +
           `**Homepage:** [https://github.com/S0methingSomething/BitBot](https://github.com/S0methingSomething/BitBot)\n\n` +
           `This is created by [u/C1oudyLol](https://www.reddit.com/user/C1oudyLol/).\n\n` +
           `**Current status (based on comments):** Working`;
}

/**
 * Gets a Reddit API token using the password grant type.
 */
async function getToken() {
    console.log("Requesting API token using password grant type...");
    const body = new URLSearchParams({
        grant_type: 'password',
        username: REDDIT_USERNAME,
        password: REDDIT_PASSWORD,
    });
    const auth = Buffer.from(`${REDDIT_CLIENT_ID}:${REDDIT_CLIENT_SECRET}`).toString('base64');
    const { data } = await axios.post(TOKEN_URL, body, {
        headers: { Authorization: `Basic ${auth}`, 'User-Agent': REDDIT_USER_AGENT }
    });
    return data.access_token;
}

// (The rest of the script remains the same)
function createRedditClient(token) {
    return axios.create({
        baseURL: API_BASE,
        headers: { Authorization: `Bearer ${token}`, 'User-Agent': REDDIT_USER_AGENT }
    });
}
async function getLatestPostedVersion(client) {
    console.log(`Searching for last post by u/${REDDIT_USERNAME} in r/${REDDIT_SUBREDDIT}...`);
    const { data } = await client.get(`/r/${REDDIT_SUBREDDIT}/search.json`, {
        params: { q: `author:${REDDIT_USERNAME}`, sort: 'new', restrict_sr: 1, limit: 5 }
    });
    const versionRegex = /MonetizationVars for (\d+\.\d+\.\d+.*)/;
    for (const post of data.data.children) {
        const match = post.data.title.match(versionRegex);
        if (match && match[1] && semver.valid(match[1])) {
            console.log(`Found last valid version: ${match[1]}`);
            return match[1];
        }
    }
    console.log("No previous valid post found.");
    return null;
}
async function postRelease(client, title, text) {
    console.log(`Submitting new post: "${title}"`);
    const { data } = await client.post('/api/submit', new URLSearchParams({
        sr: REDDIT_SUBREDDIT,
        kind: 'self',
        title,
        text,
        api_type: 'json'
    }));
    const postData = data?.json?.data?.things?.[0]?.data;
    if (postData && postData.url) {
        return postData.url;
    }
    console.error("❌ Post submission response was invalid.");
    console.error("Full API Response:", JSON.stringify(data, null, 2));
    throw new Error("Post creation verification failed: Invalid API response from Reddit.");
}
async function main() {
    try {
        assertEnv();
        const token = await getToken();
        const redditClient = createRedditClient(token);
        const newVersion = semver.clean(BITLIFE_VERSION);
        if (!newVersion) throw new Error(`Invalid version format from release: "${BITLIFE_VERSION}"`);
        const lastPostedVersion = await getLatestPostedVersion(redditClient);
        if (!lastPostedVersion || semver.gt(newVersion, lastPostedVersion)) {
            console.log(`New version (${newVersion}) is higher than last posted version (${lastPostedVersion || 'None'}). Posting...`);
            const postTitle = `MonetizationVars for ${newVersion}`;
            const postBody = generatePostBody();
            const newPostUrl = await postRelease(redditClient, postTitle, postBody);
            if (newPostUrl && GITHUB_OUTPUT) {
                console.log(`Communicating new post URL back to the workflow: ${newPostUrl}`);
                fs.appendFileSync(GITHUB_OUTPUT, `post_url=${newPostUrl}\n`);
            } else {
                 console.log("Not in a GitHub Actions environment, skipping output.");
            }
        } else {
            console.log(`🔸 No post needed. The latest version on Reddit (${lastPostedVersion}) is current.`);
        }
    } catch (error) {
        console.error("❌ BitBot failed to run.");
        if (error.response) {
            console.error(`API Error: ${error.response.status} ${error.response.statusText}`, error.response.data);
        } else {
            console.error(error.message);
        }
        process.exit(1);
    }
}
main();
