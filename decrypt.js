// BitEdit Decryption Logic Re-implementation in Node.js
const fs = require('fs');
const path = require('path');

// --- Constants ---
const DEFAULT_CIPHER_KEY = "com.wtfapps.apollo16";
const B64_NET_BOOLEAN_TRUE_STANDARD = "AAEAAAD/////AQAAAAAAAAAEAQAAAA5TeXN0ZW0uQm9vbGVhbgEAAAAHbV92YWx1ZQABAQs=";
const B64_NET_BOOLEAN_TRUE_VARIANT  = "AAEAAAD/////AQAAAAAAAAAEAQAAAA5TeXN0ZW0uQm9vbGVhbgEAAAAHbV92YWx1ZQABAAs=";
const B64_NET_BOOLEAN_FALSE_STANDARD= "AAEAAAD/////AQAAAAAAAAAEAQAAAA5TeXN0ZW0uQm9vbGVhbgEAAAAHbV92YWx1ZQABAAw=";
const USER_SERIALIZED_INT32_PREFIX = Buffer.from([0, 1, 0, 0, 0, 255, 255, 255, 255, 1, 0, 0, 0, 0, 0, 0, 0, 4, 1, 0, 0, 0, 12, 83, 121, 115, 116, 101, 109, 46, 73, 110, 116, 51, 50, 1, 0, 0, 0, 7, 109, 95, 118, 97, 108, 117, 101, 0, 8]);
const USER_SERIALIZED_INT32_SUFFIX = Buffer.from([11]);
const obfCharMap = {0x61:0x7a,0x62:0x6d,0x63:0x79,0x64:0x6c,0x65:0x78,0x66:0x6b,0x67:0x77,0x68:0x6a,0x69:0x76,0x6a:0x69,0x6b:0x75,0x6c:0x68,0x6d:0x74,0x6e:0x67,0x6f:0x73,0x70:0x66,0x71:0x72,0x72:0x65,0x73:0x71,0x74:0x64,0x75:0x70,0x76:0x63,0x77:0x6f,0x78:0x62,0x79:0x6e,0x7a:0x61};

// --- Utility Functions ---
function getObfuscatedKey(key) {
    let oKey = "";
    for (const char of key.toLowerCase()) oKey += String.fromCharCode(obfCharMap[char.charCodeAt(0)] || char.charCodeAt(0));
    return oKey;
}
function base64DecodeAndXOR(b64, key) {
    const decoded = Buffer.from(b64, 'base64');
    const result = Buffer.alloc(decoded.length);
    for (let i = 0; i < decoded.length; i++) result[i] = decoded[i] ^ key.charCodeAt(i % key.length);
    return result.toString('utf-8');
}
function decryptInt(base64String) {
    try {
        const bytes = Buffer.from(base64String, 'base64');
        if (bytes.length !== 55 || Buffer.compare(bytes.slice(0, 49), USER_SERIALIZED_INT32_PREFIX) !== 0 || Buffer.compare(bytes.slice(54), USER_SERIALIZED_INT32_SUFFIX) !== 0) return null;
        return bytes.readInt32LE(49);
    } catch { return null; }
}
async function decryptFile(filePath) {
    console.log(`Starting decryption for: ${filePath}`);
    const fileContent = fs.readFileSync(filePath, 'utf-8');
    const obfuscatedKey = getObfuscatedKey(DEFAULT_CIPHER_KEY);
    const itemMap = {};
    for (const line of fileContent.split('\n').filter(l => l.trim())) {
        const [encKey, encVal] = line.split(/:(.+)/);
        if (!encKey || !encVal) continue;
        const decKey = base64DecodeAndXOR(encKey.trim(), obfuscatedKey);
        const decValB64 = base64DecodeAndXOR(encVal.trim(), obfuscatedKey);
        if (decValB64 === B64_NET_BOOLEAN_TRUE_STANDARD || decValB64 === B64_NET_BOOLEAN_TRUE_VARIANT) itemMap[decKey] = true;
        else if (decValB64 === B64_NET_BOOLEAN_FALSE_STANDARD) itemMap[decKey] = false;
        else itemMap[decKey] = decryptInt(decValB64) ?? decValB64;
    }
    const outputJson = JSON.stringify(itemMap, null, 2);
    const outputFilePath = path.join(path.dirname(filePath), `${path.basename(filePath, path.extname(filePath))}_decrypted.json`);
    fs.writeFileSync(outputFilePath, outputJson);
    console.log(`Decryption complete. Output: ${outputFilePath}`);
}
if (require.main === module) decryptFile(process.argv[2]);
