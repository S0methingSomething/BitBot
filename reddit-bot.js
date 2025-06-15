import axios from 'axios';
import semver from 'semver';
import 'dotenv/config'; // Loads credentials from .env file or Replit Secrets
import { fetchAndSaveReleaseInfo } from './fetch-release-info.js';

// This file is now a module and exports its main function.

// ───────────────────────── Configuration ──────────────────────────
const {
  REDDIT_CLIENT_ID,
  REDDIT_CLIENT_SECRET,
  REDDIT_USERNAME,
  REDDIT_PASSWORD,
  REDDIT_USER_AGENT = `WebApp:BitBot-C1oudyLol:v3.0 (Replit)`,
  REDDIT_SUBREDDIT,
} = process.env;

const TOKEN_URL = 'https://www.reddit.com/api/v1/access_token';
const API_BASE  = 'https://oauth.reddit.com';

const COMMON_HEADERS = {
  'User-Agent': REDDIT_USER_AGENT,
  Accept:       'application/json',
};

// ────────────────────────── Utilities ─────────────────────────────
function assertEnv() {
  const required = {
    REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USERNAME,
    REDDIT_PASSWORD,  REDDIT_SUBREDDIT,
  };
  const missing = Object.entries(required)
    .filter(([, v]) => !v)
    .map(([k]) => k);
  if (missing.length) throw new Error(`Missing Replit Secrets: ${missing.join(', ')}`);

  console.log('Environment configuration validated.');
  console.log(`Using User-Agent: ${REDDIT_USER_AGENT}`);
}

function generatePostBody(downloadUrl) {
  return (
    `This is an automated post by [BitBot](https://github.com/S0methingSomething/BitBot).\n\n` +
    `**Download link:** [MonetizationVars](${downloadUrl})\n\n` +
    `**Homepage:** [https://github.com/S0methingSomething/BitBot](https://github.com/S0methingSomething/BitBot)\n\n` +
    `Created by [u/C1oudyLol](https://www.reddit.com/user/C1oudyLol/).\n\n` +
    `**Current status (based on comments):** Working`
  );
}

// ───────────────────── Reddit authenticated helpers ───────────────
async function getToken() {
  console.log('Requesting API token …');
  const auth = Buffer.from(`${REDDIT_CLIENT_ID}:${REDDIT_CLIENT_SECRET}`).toString('base64');
  const body = new URLSearchParams({
    grant_type: 'password',
    username:   REDDIT_USERNAME,
    password:   REDDIT_PASSWORD,
    scope:      'identity read submit',
  });
  const { data } = await axios.post(TOKEN_URL, body, {
    headers: { ...COMMON_HEADERS, Authorization: `Basic ${auth}` },
  });
  return data.access_token;
}

function redditClient(token) {
  return axios.create({
    baseURL: API_BASE,
    headers: { ...COMMON_HEADERS, Authorization: `Bearer ${token}` },
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

async function submitPost(client, title, text) {
  console.log(`Submitting new post: "${title}"`);
  const { data } = await client.post(
    '/api/submit',
    new URLSearchParams({ sr: REDDIT_SUBREDDIT, kind: 'self', title, text, api_type: 'json' })
  );
  const url = data?.json?.data?.things?.[0]?.data?.url;
  if (!url) {
    console.error('❌ Invalid submit response:', JSON.stringify(data, null, 2));
    throw new Error('Post creation failed.');
  }
  return url;
}

// ───────────────────────────── Main Logic (Exported) ───────────────
export async function runBotLogic() {
  try {
    assertEnv();
    
    // Step 1: Fetch the latest release info from GitHub
    const releaseInfo = await fetchAndSaveReleaseInfo();
    const newVersion = semver.clean(releaseInfo.BITLIFE_VERSION);
    if (!newVersion) throw new Error(`Invalid version string: "${releaseInfo.BITLIFE_VERSION}"`);

    // Step 2: Authenticate and check Reddit
    const token  = await getToken();
    const client = redditClient(token);
    const lastVersion = await getLatestPostedVersion(client);

    // Step 3: Compare and post if necessary
    if (!lastVersion || semver.gt(newVersion, lastVersion)) {
      console.log(`New version (${newVersion}) > last (${lastVersion || 'none'}) – will post.`);
      
      const postUrl = await submitPost(
        client,
        `MonetizationVars for ${newVersion}`,
        generatePostBody(releaseInfo.DOWNLOAD_URL),
      );
      
      console.log(`✅ Posted: ${postUrl}`);
    } else {
      console.log(`🔸 No post needed: Reddit already has version ${lastVersion}.`);
    }
  } catch (err) {
    console.error('❌ BitBot failed.');
    if (err.response) {
      console.error(`API ${err.response.status}: ${err.response.statusText}`);
    } else {
      console.error(err.message);
    }
    // Don't exit process, just throw error for server to handle
    throw err;
  }
}
