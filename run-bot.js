import { fetchLatestReleaseInfo } from './fetch-release-info.js';
import { runRedditLogic }        from './reddit-bot.js';
import { getProxyList }          from './proxy-manager.js';

const MAX_RETRIES       = 1;                               // number of proxy attempts
const GITHUB_DIRECT_IP  = process.env.GITHUB_DIRECT_IP;    // e.g. "140.82.113.6"

export async function runFullBotProcess () {
  console.log('--- Starting Full Bot Process ---');

  const config = {
    REDDIT_CLIENT_ID     : process.env.REDDIT_CLIENT_ID,
    REDDIT_CLIENT_SECRET : process.env.REDDIT_CLIENT_SECRET,
    REDDIT_USERNAME      : process.env.REDDIT_USERNAME,
    REDDIT_PASSWORD      : process.env.REDDIT_PASSWORD,
    REDDIT_SUBREDDIT     : process.env.REDDIT_SUBREDDIT,
    REDDIT_USER_AGENT    : process.env.REDDIT_USER_AGENT ||
                           `node:BitBot/4.0 (by u/${process.env.REDDIT_USERNAME})`,
  };

  /*  ────────────────────────────────────────────────────────────
      Build the attempt list:
      1. First element  -> direct call (GitHub IP if provided)
      2. Next elements -> up to MAX_RETRIES proxy URLs
  */
  const proxies   = await getProxyList();
  const attempts  = [null, ...proxies.slice(0, MAX_RETRIES)];

  for (let i = 0; i < attempts.length; i++) {
    const proxy = attempts[i];

    try {
      console.log(`\n--- ATTEMPT ${i + 1}/${attempts.length} ---`);

      if (proxy) {
        console.log(`Using proxy: ${proxy}`);
      } else if (GITHUB_DIRECT_IP) {
        console.log(`Attempting direct connection via GitHub IP: ${GITHUB_DIRECT_IP}`);
      } else {
        console.log('Attempting direct connection (standard DNS).');
      }

      /*  If you supplied GITHUB_DIRECT_IP we pass it to
          fetchLatestReleaseInfo so that it can hit the IP address
          while still sending Host: api.github.com  */
      const releaseInfo = await fetchLatestReleaseInfo(proxy, GITHUB_DIRECT_IP);
      const result      = await runRedditLogic(config, releaseInfo, proxy);

      console.log('--- BOT RUN SUCCEEDED ---');
      return result;

    } catch (error) {
      console.error(`Attempt ${i + 1} failed: ${error.message}`);

      // after we've exhausted the proxies we give up
      if (i === attempts.length - 1) {
        console.error('All attempts failed. The bot could not complete its task.');
        throw error;
      }
    }
  }
}
