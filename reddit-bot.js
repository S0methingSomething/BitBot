import axios from 'axios';
import semver from 'semver';

// --- Configuration & Constants ---
const {
    REDDIT_CLIENT_ID,
    REDDIT_CLIENT_SECRET,
    REDDIT_USERNAME,
    REDDIT_USER_AGENT,
    REDDIT_SUBREDDIT,
    BITLIFE_VERSION,
    DOWNLOAD_URL,
} = process.env;

const TOKEN_URL = 'https://www.reddit.com/api/v1/access_token';
const API_BASE = 'https://oauth.reddit.com';

// --- Helper Functions ---

/** Validates that all required environment variables are set. */
function assertEnv() {
    const required = { REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USERNAME, REDDIT_USER_AGENT, REDDIT_SUBREDDIT, BITLIFE_VERSION, DOWNLOAD_URL };
    const missing = Object.keys(required).filter(key => !required[key]);
    if (missing.length > 0) {
        throw new Error(`Missing required environment variables: ${missing.join(', ')}`);
    }
    console.log("Environment configuration validated successfully.");
}

/** Generates the post body text. */
function generatePostBody() {
    return `This is an automated post by [BitBot](https://github.com/S0methingSomething/BitBot).\n\n` +
           `**Download link:** [MonetizationVars](${DOWNLOAD_URL})\n\n` +
           `**Homepage:** [https://github.com/S0methingSomething/BitBot](https://github.com/S0methingSomething/BitBot)\n\n` +
           `This is created by [u/C1oudyLol](https://www.reddit.com/user/C1oudyLol/).\n\n` +
           `**Current status (based on comments):** Working`;
}

// --- Reddit API Interaction ---

/**
 * Gets a Reddit API token using secure client_credentials grant type.
 * @returns {Promise<string>} The access token.
 */
async function getToken() {
    console.log("Requesting API token using client credentials...");
    const body = new URLSearchParams({ grant_type: 'client_credentials' });
    const auth = Buffer.from(`${REDDIT_CLIENT_ID}:${REDDIT_CLIENT_SECRET}`).toString('base64');
    const { data } = await axios.post(TOKEN_URL, body, {
        headers: { Authorization: `Basic ${auth}`, 'User-Agent': REDDIT_USER_AGENT }
    });
    return data.access_token;
}

/**
 * Creates a pre-configured Axios instance for making authenticated API calls.
 * @param {string} token - The OAuth access token.
 * @returns {axios.AxiosInstance} A configured Axios instance.
 */
function createRedditClient(token) {
    return axios.create({
        baseURL: API_BASE,
        headers: { Authorization: `Bearer ${token}`, 'User-Agent': REDDIT_USER_AGENT }
    });
}

/**
 * Finds the version number from the latest post made by the bot.
 * @param {axios.AxiosInstance} client - The authenticated Axios client.
 * @returns {Promise<string|null>} The latest version string or null if no post is found.
 */
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

/**
 * Submits a new release post to the specified subreddit.
 * @param {axios.AxiosInstance} client - The authenticated Axios client.
 * @param {string} version - The version to be posted.
 */
async function postRelease(client, version) {
    const title = `MonetizationVars for ${version}`;
    const text = generatePostBody();
    console.log(`Submitting new post: "${title}"`);

    await client.post('/api/submit', new URLSearchParams({
        sr: REDDIT_SUBREDDIT,
        kind: 'self',
        title: title,
        text: text,
        api_type: 'json'
    }));
}

// --- Main Execution ---

try {
    assertEnv();
    const token = await getToken();
    const redditClient = createRedditClient(token);
    const lastPostedVersion = await getLatestPostedVersion(redditClient);
    const newVersion = semver.clean(BITLIFE_VERSION); // Clean the version string

    if (!newVersion) {
        throw new Error(`Invalid version format from GitHub release: "${BITLIFE_VERSION}"`);
    }

    if (!lastPostedVersion || semver.gt(newVersion, lastPostedVersion)) {
        await postRelease(redditClient, newVersion);
        console.log(`✅ Successfully posted new release for version ${newVersion}.`);
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
