/*
 * Reddit Bot for BitBot
 * This script authenticates with the Reddit API and posts a comment.
 * It requires environment variables for credentials.
 */

const fs = require('fs');
const path = require('path');
const axios = require('axios');

// --- Configuration ---
const {
    REDDIT_CLIENT_ID,
    REDDIT_CLIENT_SECRET,
    REDDIT_USERNAME,
    REDDIT_PASSWORD,
    REDDIT_USER_AGENT,
    REDDIT_POST_ID
} = process.env;

const DECRYPTED_FILE_PATH = path.join(__dirname, 'decrypted.json');
const OAUTH_URL = 'https://www.reddit.com/api/v1/access_token';
const API_URL_BASE = 'https://oauth.reddit.com';

/**
 * Validates that all required environment variables are set.
 */
function validateConfig() {
    const requiredVars = {
        REDDIT_CLIENT_ID,
        REDDIT_CLIENT_SECRET,
        REDDIT_USERNAME,
        REDDIT_PASSWORD,
        REDDIT_USER_AGENT,
        REDDIT_POST_ID
    };
    const missingVars = Object.keys(requiredVars).filter(key => !requiredVars[key]);
    if (missingVars.length > 0) {
        throw new Error(`Missing required environment variables: ${missingVars.join(', ')}. Please configure them as GitHub secrets.`);
    }
    console.log("Configuration validated successfully.");
}

/**
 * Authenticates with the Reddit API to get an OAuth token.
 * @returns {Promise<string>} The access token.
 */
async function getAccessToken() {
    console.log("Attempting to get Reddit API access token...");
    try {
        const authString = Buffer.from(`${REDDIT_CLIENT_ID}:${REDDIT_CLIENT_SECRET}`).toString('base64');

        const response = await axios.post(OAUTH_URL, new URLSearchParams({
            grant_type: 'password',
            username: REDDIT_USERNAME,
            password: REDDIT_PASSWORD,
        }), {
            headers: {
                'Authorization': `Basic ${authString}`,
                'User-Agent': REDDIT_USER_AGENT,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        });

        console.log("Successfully obtained access token.");
        return response.data.access_token;
    } catch (error) {
        console.error("Error getting access token:", error.response ? error.response.data : error.message);
        throw new Error("Failed to authenticate with Reddit API.");
    }
}

/**
 * Posts a comment to the specified Reddit post.
 * @param {string} token - The OAuth access token.
 * @param {string} commentText - The text of the comment to post.
 */
async function postComment(token, commentText) {
    const thingId = REDDIT_POST_ID.startsWith('t3_') ? REDDIT_POST_ID : `t3_${REDDIT_POST_ID}`;
    console.log(`Posting comment to Reddit post ID: ${thingId}`);

    try {
        const response = await axios.post(`${API_URL_BASE}/api/comment`, new URLSearchParams({
            api_type: 'json',
            text: commentText,
            thing_id: thingId,
        }), {
            headers: {
                'Authorization': `Bearer ${token}`,
                'User-Agent': REDDIT_USER_AGENT,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        });

        if (response.data.json.errors.length > 0) {
            throw new Error(`Reddit API returned errors: ${JSON.stringify(response.data.json.errors)}`);
        }

        console.log("Successfully posted comment to Reddit.");
        console.log("Comment URL:", response.data.json.data.things[0].data.permalink);

    } catch (error) {
        console.error("Error posting comment:", error.response ? error.response.data : error.message);
        throw new Error("Failed to post comment to Reddit.");
    }
}

/**
 * Main function to run the bot.
 */
async function main() {
    try {
        validateConfig();

        // Check if the decrypted file exists
        if (!fs.existsSync(DECRYPTED_FILE_PATH)) {
            throw new Error(`Decrypted file not found at '${DECRYPTED_FILE_PATH}'. Halting bot.`);
        }

        // Read the decrypted data to report the number of items
        const decryptedData = JSON.parse(fs.readFileSync(DECRYPTED_FILE_PATH, 'utf-8'));
        const itemCount = Object.keys(decryptedData).length;

        // Construct the comment
        const timestamp = new Date().toUTCString();
        const comment = `🤖 **BitBot Status Update** 🤖\n\n` +
                        `* **Status:** Decryption Successful\n` +
                        `* **Items Found:** ${itemCount}\n` +
                        `* **Timestamp:** ${timestamp}\n\n` +
                        `--- \n` +
                        `*This is an automated message.*`;

        // Get token and post comment
        const token = await getAccessToken();
        await postComment(token, comment);

    } catch (error) {
        console.error(`BitBot failed: ${error.message}`);
        process.exit(1); // Exit with an error code to fail the GitHub Action
    }
}

// Run the main function
main();
