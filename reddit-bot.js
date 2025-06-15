import axios from 'axios';
import semver from 'semver';

const TOKEN_URL = 'https://www.reddit.com/api/v1/access_token';
const API_BASE  = 'https://oauth.reddit.com';

// This function now contains the entire sequence of Reddit operations.
export async function runRedditLogic(config, releaseInfo) {
  console.log("--- Starting Reddit Bot Logic ---");
  assertConfig(config);

  const newVersion = semver.clean(releaseInfo.BITLIFE_VERSION);
  if (!newVersion) throw new Error(`Invalid version string from GitHub: "${releaseInfo.BITLIFE_VERSION}"`);

  const token = await getRedditToken(config);
  const client = createRedditClient(token, config.REDDIT_USER_AGENT);
  const lastVersion = await getLatestPostedVersion(client, config);

  if (!lastVersion || semver.gt(newVersion, lastVersion)) {
    console.log(`New version (${newVersion}) > last (${lastVersion || 'none'}). Posting...`);
    const postUrl = await submitPost(
      client,
      config,
      `MonetizationVars for ${newVersion}`,
      generatePostBody(releaseInfo.DOWNLOAD_URL, config.REDDIT_USERNAME)
    );
    const successMessage = `✅ Successfully posted new release: ${postUrl}`;
    console.log(successMessage);
    return successMessage;
  } else {
    const message = `🔸 No post needed: Reddit version (${lastVersion}) is current.`;
    console.log(message);
    return message;
  }
}

// --- Helper Functions ---
function assertConfig(config) {
    const required = [
        'REDDIT_CLIENT_ID', 'REDDIT_CLIENT_SECRET', 'REDDIT_USERNAME', 
        'REDDIT_PASSWORD', 'REDDIT_SUBREDDIT', 'REDDIT_USER_AGENT'
    ];
    const missing = required.filter(key => !config[key]);
    if (missing.length > 0) {
        throw new Error(`Missing required configuration: ${missing.join(', ')}`);
    }
    console.log('Reddit bot configuration validated.');
}

function generatePostBody(downloadUrl, username) {
  return (
    `This is an automated post by [BitBot](https://github.com/S0methingSomething/BitBot).\n\n` +
    `**Download link:** [MonetizationVars](${downloadUrl})\n\n` +
    `**Homepage:** [https://github.com/S0methingSomething/BitBot](https://github.com/S0methingSomething/BitBot)\n\n` +
    `Created by [u/${username}](https://www.reddit.com/user/${username}/).\n\n` +
    `**Current status (based on comments):** Working`
  );
}

async function getRedditToken(config) {
  console.log('Requesting Reddit API token...');
  const auth = Buffer.from(`${config.REDDIT_CLIENT_ID}:${config.REDDIT_CLIENT_SECRET}`).toString('base64');
  const body = new URLSearchParams({
    grant_type: 'password',
    username:   config.REDDIT_USERNAME,
    password:   config.REDDIT_PASSWORD,
    scope:      'identity read submit',
  });
  const { data } = await axios.post(TOKEN_URL, body, {
    headers: { 'User-Agent': config.REDDIT_USER_AGENT, Authorization: `Basic ${auth}` },
  });
  return data.access_token;
}

function createRedditClient(token, userAgent) {
  return axios.create({
    baseURL: API_BASE,
    headers: { 'User-Agent': userAgent, Authorization: `Bearer ${token}` },
  });
}

async function getLatestPostedVersion(client, config) {
    console.log(`Searching for last post by u/${config.REDDIT_USERNAME} in r/${config.REDDIT_SUBREDDIT}...`);
    const { data } = await client.get(`/r/${config.REDDIT_SUBREDDIT}/search.json`, {
        params: { q: `author:${config.REDDIT_USERNAME}`, sort: 'new', restrict_sr: 1, limit: 5 }
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

async function submitPost(client, config, title, text) {
  console.log(`Submitting new post: "${title}"`);
  const { data } = await client.post(
    '/api/submit',
    new URLSearchParams({ sr: config.REDDIT_SUBREDDIT, kind: 'self', title, text, api_type: 'json' })
  );
  const url = data?.json?.data?.things?.[0]?.data?.url;
  if (!url) {
    console.error('❌ Invalid submit response:', JSON.stringify(data, null, 2));
    throw new Error('Post creation failed due to invalid API response.');
  }
  return url;
}
