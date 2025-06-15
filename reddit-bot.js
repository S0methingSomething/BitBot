// reddit-bot.js
// -------------
// Posts a release thread to Reddit when a higher BitLife version is detected.
// Uses Pushshift to discover the latest version already posted.

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
const PUSHSHIFT = 'https://api.pushshift.io/reddit/submission/search/';

const COMMON_HEADERS = {
  'User-Agent': REDDIT_USER_AGENT,
  Accept:       'application/json',
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

// ────────────────── Read the last post through Pushshift ──────────
async function getLatestPostedVersion() {
  console.log('Querying Pushshift for last submission …');

  const url = `${PUSHSHIFT}?author=${REDDIT_USERNAME}` +
              `&subreddit=${REDDIT_SUBREDDIT}` +
              `&size=1&sort=desc&sort_type=created_utc&fields=title`;

  const { data } = await axios.get(url, { headers: COMMON_HEADERS });

  if (!data?.data?.length) {
    console.log('No previous submission recorded in Pushshift.');
    return null;
  }

  const title = data.data[0].title;
  const m = title.match(/MonetizationVars for (\d+\.\d+\.\d+(?:[-+][\w.-]+)?)/);
  if (m && semver.valid(m[1])) {
    console.log(`Last version found via Pushshift: ${m[1]}`);
    return m[1];
  }

  console.log('No valid version pattern in last Pushshift title.');
  return null;
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

async function submitPost(client, title, text) {
  console.log(`Submitting new post: "${title}"`);

  const { data } = await client.post(
    '/api/submit',
    new URLSearchParams({
      sr: REDDIT_SUBREDDIT,
      kind: 'self',
      title,
      text,
      api_type: 'json',
    }),
  );

  const url = data?.json?.data?.things?.[0]?.data?.url;
  if (!url) {
    console.error('❌ Invalid submit response:', JSON.stringify(data, null, 2));
    throw new Error('Post creation failed.');
  }
  return url;
}

// ───────────────────────────── Main ───────────────────────────────
async function main() {
  try {
    console.log('Waiting 2 s before starting …');
    await sleep(2000);

    assertEnv();

    const newVersion = semver.clean(BITLIFE_VERSION);
    if (!newVersion) throw new Error(`Invalid version string: "${BITLIFE_VERSION}"`);

    const lastVersion = await getLatestPostedVersion();

    if (!lastVersion || semver.gt(newVersion, lastVersion)) {
      console.log(`New version (${newVersion}) > last (${lastVersion || 'none'}) – will post.`);

      const token  = await getToken();
      const client = redditClient(token);

      const postUrl = await submitPost(
        client,
        `MonetizationVars for ${newVersion}`,
        generatePostBody(),
      );

      console.log(`✅ Posted: ${postUrl}`);
      if (GITHUB_OUTPUT) fs.appendFileSync(GITHUB_OUTPUT, `post_url=${postUrl}\n`);
    } else {
      console.log(`🔸 No post: Reddit already has version ${lastVersion}.`);
    }
  } catch (err) {
    console.error('❌ BitBot failed.');
    if (err.response) {
      console.error(`API ${err.response.status}: ${err.response.statusText}`);
    } else {
      console.error(err.message);
    }
    process.exit(1);
  }
}

main();
