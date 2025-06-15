import axios from 'axios';

const PROXY_API_URL = 'https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=text';

export async function getProxyList() {
    console.log("Fetching proxy list from ProxyScrape API...");
    try {
        const { data } = await axios.get(PROXY_API_URL);
        const proxies = data.split('\r\n').filter(p => p.startsWith('http://'));
        
        if (proxies.length === 0) {
            console.warn("ProxyScrape returned no HTTP proxies.");
            return [];
        }

        for (let i = proxies.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [proxies[i], proxies[j]] = [proxies[j], proxies[i]];
        }
        
        console.log(`Found and shuffled ${proxies.length} HTTP proxies.`);
        return proxies;
    } catch (error) {
        console.error("Could not fetch proxy list:", error.message);
        return [];
    }
}
