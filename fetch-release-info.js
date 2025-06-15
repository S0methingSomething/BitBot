import axios from 'axios';

const GITHUB_API_URL = "https://api.github.com/repos/S0methingSomething/BitEdit/releases/tags/Latest";

export async function fetchLatestReleaseInfo() {
  console.log("Fetching latest release info from GitHub...");
  const { data: releaseData } = await axios.get(GITHUB_API_URL);
  const releaseBody = releaseData.body || "";

  const versionRegex = /(?:for BitLife\s*v?|compatible with BitLife\s*v?|BitLife version\s*v?)(\d+\.\d+(\.\d+)?)/i;
  const match = releaseBody.match(versionRegex);
  if (!match || !match[1]) {
    throw new Error("Could not parse version from GitHub release description.");
  }

  const asset = releaseData.assets.find(asset => asset.name === "MonetizationVars");
  if (!asset) {
    throw new Error("Could not find 'MonetizationVars' asset in the release.");
  }

  const releaseInfo = {
    BITLIFE_VERSION: match[1],
    DOWNLOAD_URL: asset.browser_download_url,
  };

  console.log("Successfully fetched release info:", releaseInfo);
  return releaseInfo;
}
