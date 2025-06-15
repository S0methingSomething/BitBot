// reddit-bot.js
// -------------
// Posts a release thread to Reddit when a higher BitLife version is detected.

import axios from 'axios';
import semver from 'semver';
import fs from 'fs';

// ───────────────────────── Configuration ──────────────────────────
const {
  REDDIT_CLIENT_ID,
  REDDIT_CLIENT_SECRET,
  REDDIT_USERNAME,
  REDDIT_PASSWORD,
  REDDIT_USER_AGENT = `script:BitBot/2.0 (by u/${process.env.REDDIT_USERNAME})`,
  REDDIT_SUBREDDIT,
  BITLIFE_VERSION,
  DOWNLOAD_URL,
  GITHUB_OUTPUT,
} = process.env;

const TOKEN_URL = 'https://www.reddit.com/api/v1/access_token';
const API_BASE  = 'https://oauth.reddit.com';

const DEFAULT_HEADERS = {
  'User-Agent' : REDDIT_USER_AGENT,
  'Accept'     : 'application/json',
};

// ────────────────────────── Utilities ─────────────────────────────
function assertEnv() {
  const required = {
    REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USERNAME,
    REDDIT_PASSWORD,  REDDIT_SUBREDDIT,
    BITLIFE_VERSION,  DOWNLOAD_URL,
  };

  const missing = Object.entries(required)
                        .filter(([, v]) => !v)
                        .map(([k]) => k);

  if (missing.length) throw new Error(`Missing env vars: ${missing.join(', ')}`);
  console.log('Environment configuration validated.');
  console.log(`Using User-Agent: ${REDDIT_USER_AGENT}`);
}

function generatePostBody() {
  return (
    `This is an automated post by [BitBot](https://github.com/S0methingSomething/BitBot).\n\n` +
    `**Download link:** [MonetizationVars](${DOWNLOAD_URL})\n\n` +
    `**Homepage:** [https://github.com/S0methingSomething/BitBot](https://github.com/S0methingSomething/BitBot)\n\n` +
    `Created by [u/C1oudyLol](https://www.reddit.com/user/C1oudyLol/).\n\n` +
    `**Current status (based on comments):** Working`
  );
}

const sleep = ms => new Promise(r => setTimeout(r, ms));

// ─────────────────────── Reddit API helpers ───────────────────────
async function getToken() {
  console.log('Requesting API token …');

  const body = new URLSearchParams({
    grant_type : 'password',
    username   : REDDIT_USERNAME,
    password   : REDDIT_PASSWORD,
    scope      : 'identity read submit',
  });

  const auth = Buffer.from(`${REDDIT_CLIENT_ID}:${REDDIT_CLIENT_SECRET}`).toString('base64');

  const { data } = await axios.post(TOKEN_URL, body, {
    headers: { ...DEFAULT_HEADERS, Authorization: `Basic ${auth}` },
  });

  return data.access_token;
}

function createRedditClient(token) {
  return axios.create({
    baseURL : API_BASE,
    headers : { ...DEFAULT_HEADERS, Authorization: `Bearer ${token}` },
  });
}

// Looks at the authorised user's own submissions instead of the subreddit feed
async function getLatestPostedVersion(client) {
  console.log(`Scanning u/${REDDIT_USERNAME} submitted posts …`);

  const { data } = await client.get(
    `/user/${REDDIT_USERNAME}/submitted.json`,
    { params: { limit: 100, raw_json: 1 } },
  );

  const versionRegex = /MonetizationVars for (\d+\.\d+\.\d+(?:[-+][\w.-]+)?)/;

  for (const post of data.data.children) {
    const p = post.data;

    // Only consider posts in the target subreddit
    if (p.subreddit !== REDDIT_SUBREDDIT) continue;

    const match = p.title.match(versionRegex);
    if (match && semver.valid(match[1])) {
      console.log(`Found last valid version: ${match[1]}`);
      return match[1];
    }
  }
  console.log('No previous valid post found.');
  return null;
}

async function postRelease(client, title, text) {
  console.log(`Submitting new post: "${title}"`);

  const { data } = await client.post(
    '/api/submit',
    new URLSearchParams({
      sr       : REDDIT_SUBREDDIT,
      kind     : 'self',
      title,
      text,
      api_type : 'json',
    }),
  );

  const postData = data?.json?.data?.things?.[0]?.data;
  if (postData?.url) return postData.url;

  console.error('❌ Invalid post submission response.');
  console.error(JSON.stringify(data, null, 2));
  throw new Error('Post creation failed.');
}

// ─────────────────────────── Main flow ────────────────────────────
async function main() {
  try {
    console.log('Waiting 2 s before starting …');
    await sleep(2000);

    assertEnv();

    const token        = await getToken();
    const redditClient = createRedditClient(token);

    const newVersion = semver.clean(BITLIFE_VERSION);
    if (!newVersion) throw new Error(`Invalid version: "${BITLIFE_VERSION}"`);

    const lastVersion = await getLatestPostedVersion(redditClient);

    if (!lastVersion || semver.gt(newVersion, lastVersion)) {
      console.log(`Posting new version ${newVersion} (prev = ${lastVersion || 'none'}) …`);

      const postUrl = await postRelease(
        redditClient,
        `MonetizationVars for ${newVersion}`,
        generatePostBody(),
      );

      if (postUrl && GITHUB_OUTPUT) {
        console.log(`Writing post URL to workflow: ${postUrl}`);
        fs.appendFileSync(GITHUB_OUTPUT, `post_url=${postUrl}\n`);
      }
    } else {
      console.log(`🔸 No post: Reddit already has version ${lastVersion}.`);
    }
  } catch (err) {
    console.error('❌ BitBot failed.');
    if (err.response) {
      console.error(`API Error: ${err.response.status} ${err.response.statusText}`);
    } else {
      console.error(err.message);
    }
    process.exit(1);
  }
}

main();
