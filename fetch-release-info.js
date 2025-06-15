import axios from 'axios';
import fs from 'fs';

const GITHUB_API_URL = "https://api.github.com/repos/S0methingSomething/BitEdit/releases/tags/Latest";

/**
 * Fetches the latest release data from the GitHub API.
 * Parses the release body to find the BitLife version and the download URL for the 'MonetizationVars' asset.
 * Writes the found data to a file named 'release-info.json'.
 */
async function fetchAndSaveReleaseInfo() {
    console.log("Fetching latest release information from GitHub API...");

    try {
        const { data: releaseData } = await axios.get(GITHUB_API_URL);
        const releaseBody = releaseData.body || "";

        // This regex is the same robust one from the index.html file.
        const versionRegex = /(?:for BitLife\s*v?|compatible with BitLife\s*v?|BitLife version\s*v?)(\d+\.\d+(?:\.\d+)?)/i;
        const match = releaseBody.match(versionRegex);

        if (!match || !match[1]) {
            throw new Error("Could not parse BitLife version from release description.");
        }
        const bitlifeVersion = match[1];
        console.log(`Successfully parsed BitLife Version: ${bitlifeVersion}`);

        const asset = releaseData.assets.find(asset => asset.name === "MonetizationVars");
        if (!asset) {
            throw new Error("Could not find 'MonetizationVars' asset in the release.");
        }
        const downloadUrl = asset.browser_download_url;
        console.log(`Found download URL: ${downloadUrl}`);

        const output = {
            BITLIFE_VERSION: bitlifeVersion,
            DOWNLOAD_URL: downloadUrl,
        };

        // Write the data to a file that the workflow can easily read.
        fs.writeFileSync('release-info.json', JSON.stringify(output, null, 2));
        console.log("Release information saved to release-info.json");

    } catch (error) {
        console.error("❌ Failed to fetch or parse release info:", error.message);
        process.exit(1); // Exit with failure code
    }
}

fetchAndSaveReleaseInfo();
