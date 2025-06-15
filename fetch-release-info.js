import axios from 'axios';

const GITHUB_API_URL = "https://api.github.com/repos/S0methingSomething/BitEdit/releases/tags/Latest";

export async function fetchAndSaveReleaseInfo() {
    console.log("Fetching latest release information from GitHub API...");
    
    const { data: releaseData } = await axios.get(GITHUB_API_URL);
    const releaseBody = releaseData.body || "";

    const versionRegex = /(?:for BitLife\s*v?|compatible with BitLife\s*v?|BitLife version\s*v?)(\d+\.\d+(?:\.\d+)?)/i;
    const match = releaseBody.match(versionRegex);

    if (!match || !match[1]) {
        throw new Error("Could not parse BitLife version from release description.");
    }
    const bitlifeVersion = match[1];
    
    const asset = releaseData.assets.find(asset => asset.name === "MonetizationVars");
    if (!asset) {
        throw new Error("Could not find 'MonetizationVars' asset in the release.");
    }
    const downloadUrl = asset.browser_download_url;

    const releaseInfo = {
        BITLIFE_VERSION: bitlifeVersion,
        DOWNLOAD_URL: downloadUrl,
    };
    
    console.log("Successfully fetched release info:", releaseInfo);
    return releaseInfo;
}
