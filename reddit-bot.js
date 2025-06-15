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

// Keywords to determine post status from comments
const WORKING_KEYWORDS = ['working', 'works', 'no issues', 'thank you', 'thanks', 'perfect'];
const NOT_WORKING_KEYWORDS = ['not working', "doesn't work", 'broken', 'crashes', 'crash', 'error', 'issue'];


// --- Helper Functions ---

/** Validates that all required environment variables are set. */
function assertEnv() {
    const required = { REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USERNAME, REDDIT_USER_AGENT, REDDIT_SUBREDDIT, BITLIFE_VERSION, DOWNLOAD_URL };
    const missing = Object.keys(required).filter(key => !required[key]);
    if (missing.length > 0) throw new Error(`Missing required environment variables: ${missing.join(', ')}`);
    console.log("Environment configuration validated successfully.");
}

/**
 * Generates the post body text with a given status.
 * @param {string} status - The calculated status ('Working', 'Not Working', etc.)
 * @returns {string} The full markdown text for the post body.
 */
function generatePostBody(status) {
    return `This is an automated post by [BitBot](https://github.com/S0methingSomething/BitBot).\n\n` +
           `**Download link:** [MonetizationVars](${DOWNLOAD_URL})\n\n` +
           `**Homepage:** [https://github.com/S0methingSomething/BitBot](https://github.com/S0methingSomething/BitBot)\n\n` +
           `This is created by [u/C1oudyLol](https://www.reddit.com/user/C1oudyLol/).\n\n` +
           `**Current status (based on comments):** ${status}`;
}


// --- Reddit API Interaction ---

/** Gets a Reddit API token using secure client_credentials grant type. */
async function getToken() {
    console.log("Requesting API token using client credentials...");
    const body = new URLSearchParams({ grant_type: 'client_credentials' });
    const auth = Buffer.from(`${REDDIT_CLIENT_ID}:${REDDIT_CLIENT_SECRET}`).toString('base64');
    const { data } = await axios.post(TOKEN_URL, body, {
        headers: { Authorization: `Basic ${auth}`, 'User-Agent': REDDIT_USER_AGENT }
    });
    return data.access_token;
}

/** Creates a pre-configured Axios instance for making authenticated API calls. */
function createRedditClient(token) {
    return axios.create({
        baseURL: API_BASE,
        headers: { Authorization: `Bearer ${token}`, 'User-Agent': REDDIT_USER_AGENT }
    });
}

/** Searches for an existing post by the bot for the current version. */
async function searchForExistingPost(client, title) {
    console.log(`Searching for post with title: "${title}"`);
    const { data } = await client.get(`/r/${REDDIT_SUBREDDIT}/search.json`, {
        params: { q: `title:"${title}" author:${REDDIT_USERNAME} self:yes`, restrict_sr: 'on', sort: 'new' }
    });
    if (data.data.children.length > 0) {
        console.log(`Found existing post: ${data.data.children[0].data.name}`);
        return data.data.children[0].data; // Return the full post object
    }
    console.log("No existing post found for this version.");
    return null;
}

/** Fetches top-level comments from a given post. */
async function getComments(client, postId) {
    console.log(`Fetching comments for post ID: ${postId}`);
    const { data } = await client.get(`/r/${REDDIT_SUBREDDIT}/comments/${postId.replace('t3_', '')}.json`, {
        params: { limit: 100, depth: 1 }
    });
    return data[1].data.children.map(c => c.data);
}

/** Analyzes comments to determine the working status. */
function analyzeComments(comments) {
    if (comments.length === 0) return "Gathering data...";
    let workingCount = 0;
    let notWorkingCount = 0;
    for (const comment of comments) {
        const body = (comment.body || "").toLowerCase();
        if (NOT_WORKING_KEYWORDS.some(keyword => body.includes(keyword))) {
            notWorkingCount++;
        } else if (WORKING_KEYWORDS.some(keyword => body.includes(keyword))) {
            workingCount++;
        }
    }
    console.log(`Comment analysis complete: ${workingCount} positive, ${notWorkingCount} negative.`);
    if (notWorkingCount > 0) return "Not Working";
    if (workingCount > 0) return "Working";
    return "Gathering data..."; // Default if no keywords are found
}

/** Edits an existing post with a new body. */
async function editPost(client, postId, newText) {
    console.log(`Editing post ${postId} with new status...`);
    await client.post('/api/editusertext', new URLSearchParams({ api_type: 'json', thing_id: postId, text: newText }));
    console.log("Post edited successfully.");
}

/** Creates a new post and verifies its creation. */
async function postRelease(client, title, text) {
    console.log(`Submitting new post: "${title}"`);
    const { data } = await client.post('/api/submit', new URLSearchParams({
        sr: REDDIT_SUBREDDIT,
        kind: 'self',
        title,
        text,
        api_type: 'json'
    }));

    // --- VERIFICATION STEP ---
    // Check if the response has the expected structure for a successful post.
    const postData = data?.json?.data?.things?.[0]?.data;
    if (postData && postData.url) {
        console.log(`✅ Post successfully created!`);
        console.log(`✅ Verification successful. Post URL: ${postData.url}`);
        return; // Success!
    }

    // If we reach here, verification failed.
    console.error("❌ Post submission seemed to succeed, but the response was invalid.");
    console.error("Full API Response:", JSON.stringify(data, null, 2));
    throw new Error("Post creation verification failed: Invalid API response from Reddit.");
}

// --- Main Execution Logic ---
async function main() {
    try {
        assertEnv();
        const token = await getToken();
        const redditClient = createRedditClient(token);
        const newVersion = semver.clean(BITLIFE_VERSION);
        if (!newVersion) throw new Error(`Invalid version format from release: "${BITLIFE_VERSION}"`);
        
        const postTitle = `MonetizationVars for ${newVersion}`;
        const existingPost = await searchForExistingPost(redditClient, postTitle);

        if (existingPost) {
            console.log("Post for this version already exists. Checking for status updates...");
            const comments = await getComments(redditClient, existingPost.name);
            const newStatus = analyzeComments(comments);
            const currentStatusMatch = existingPost.selftext.match(/\*\*Current status \(based on comments\):\*\* (.*)/);
            const currentStatus = currentStatusMatch ? currentStatusMatch[1] : "";

            if (newStatus !== currentStatus) {
                const newBody = generatePostBody(newStatus);
                await editPost(redditClient, existingPost.name, newBody);
            } else {
                console.log("Status has not changed. No edit needed.");
            }
        } else {
            console.log("No post found for this version. Creating a new one...");
            const initialBody = generatePostBody("Gathering data...");
            await postRelease(redditClient, postTitle, initialBody);
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
