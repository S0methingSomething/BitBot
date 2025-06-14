/*
 * BitEdit - MonetizationVars Decryptor (Node.js version)
 * This script is adapted for a Node.js environment from the BitEdit web tool.
 * Original logic credits go to yntha (https://github.com/yntha/bitlife-edit).
 * Licensed under GPLv3.
 */

const fs = require('fs');
const path = require('path');

// --- Constants ---
const DEFAULT_CIPHER_KEY = "com.wtfapps.apollo16";
const B64_NET_BOOLEAN_TRUE_STANDARD = "AAEAAAD/////AQAAAAAAAAAEAQAAAA5TeXN0ZW0uQm9vbGVhbgEAAAAHbV92YWx1ZQABAQs=";
const B64_NET_BOOLEAN_TRUE_VARIANT  = "AAEAAAD/////AQAAAAAAAAAEAQAAAA5TeXN0ZW0uQm9vbGVhbgEAAAAHbV92YWx1ZQABAAs=";
const B64_NET_BOOLEAN_FALSE_STANDARD= "AAEAAAD/////AQAAAAAAAAAEAQAAAA5TeXN0ZW0uQm9vbGVhbgEAAAAHbV92YWx1ZQABAAw=";
const USER_SERIALIZED_INT32_PREFIX = new Uint8Array([0, 1, 0, 0, 0, 255, 255, 255, 255, 1, 0, 0, 0, 0, 0, 0, 0, 4, 1, 0, 0, 0, 12, 83, 121, 115, 116, 101, 109, 46, 73, 110, 116, 51, 50, 1, 0, 0, 0, 7, 109, 95, 118, 97, 108, 117, 101, 0, 8]);
const USER_SERIALIZED_INT32_SUFFIX = new Uint8Array([11]);
const USER_INT32_VALUE_OFFSET = 48;
const USER_SERIALIZED_INT32_TOTAL_LENGTH = USER_SERIALIZED_INT32_PREFIX.length + 4 + USER_SERIALIZED_INT32_SUFFIX.length;
const INPUT_FILENAME = "MonetizationVars";
const OUTPUT_FILENAME = "decrypted.json";

// --- Obfuscation Map ---
const obfCharMap = {0x61:0x7a,0x62:0x6d,0x63:0x79,0x64:0x6c,0x65:0x78,0x66:0x6b,0x67:0x77,0x68:0x6a,0x69:0x76,0x6a:0x69,0x6b:0x75,0x6c:0x68,0x6d:0x74,0x6e:0x67,0x6f:0x73,0x70:0x66,0x71:0x72,0x72:0x65,0x73:0x71,0x74:0x64,0x75:0x70,0x76:0x63,0x77:0x6f,0x78:0x62,0x79:0x6e,0x7a:0x61};

// --- Utility Functions ---
function arraysEqual(a, b) { if (!a || !b || a.length !== b.length) return false; for (let i = 0; i < a.length; i++) { if (a[i] !== b[i]) return false; } return true; }
function getObfuscatedKey(key) {let oKey = ""; for (const char of key.toLowerCase()) { const c = char.charCodeAt(0); oKey += String.fromCharCode(obfCharMap[c] || c); } return oKey;}
function base64ToUtf8String(b64) { return Buffer.from(b64, 'base64').toString('utf8'); }
function xorAndBase64Encode(txt, key) { let x = ""; for (let i=0; i<txt.length; i++) {x += String.fromCharCode(txt.charCodeAt(i) ^ key.charCodeAt(i % key.length));} return Buffer.from(x, 'utf8').toString('base64'); }
function base64DecodeAndXOR(b64, key) { let dec; try { dec = base64ToUtf8String(b64); } catch (e) { throw e; } let x = ""; for (let i=0; i<dec.length; i++) {x += String.fromCharCode(dec.charCodeAt(i) ^ key.charCodeAt(i % key.length));} return x; }
function decryptInt(base64String) { try { const bytes = Buffer.from(base64String, 'base64'); if (bytes.length !== USER_SERIALIZED_INT32_TOTAL_LENGTH) return null; const prefixBytesFromFile = bytes.slice(0, USER_SERIALIZED_INT32_PREFIX.length); const suffixByteFromFile = bytes[bytes.length - 1]; if (!arraysEqual(prefixBytesFromFile, USER_SERIALIZED_INT32_PREFIX) || suffixByteFromFile !== USER_SERIALIZED_INT32_SUFFIX[0]) return null; return bytes.readInt32LE(USER_SERIALIZED_INT32_PREFIX.length); } catch (e) { return null; } }

/**
 * Main function to decrypt the MonetizationVars file.
 */
function decryptFile() {
    console.log(`Starting decryption of '${INPUT_FILENAME}'...`);

    const inputFilePath = path.join(__dirname, INPUT_FILENAME);
    if (!fs.existsSync(inputFilePath)) {
        console.error(`Error: Input file not found at '${inputFilePath}'.`);
        process.exit(1);
    }

    const fileContent = fs.readFileSync(inputFilePath, 'utf-8');
    const obfuscatedKey = getObfuscatedKey(DEFAULT_CIPHER_KEY);
    const itemMap = {};
    const lines = fileContent.split('\n').filter(line => line.trim() !== '');
    let lineCount = 0;

    for (const line of lines) {
        lineCount++;
        const parts = line.split(/:(.+)/);
        if (parts.length < 2 || !parts[1]) {
            console.warn(`[Line ${lineCount}] Malformed line (missing or empty value), skipping.`);
            continue;
        }

        const encKey = parts[0].trim();
        const encVal = parts[1].trim();

        try {
            const decKey = base64DecodeAndXOR(encKey, obfuscatedKey);
            const decValB64 = base64DecodeAndXOR(encVal, obfuscatedKey);

            if (decValB64 === B64_NET_BOOLEAN_TRUE_STANDARD || decValB64 === B64_NET_BOOLEAN_TRUE_VARIANT) {
                itemMap[decKey] = true;
            } else if (decValB64 === B64_NET_BOOLEAN_FALSE_STANDARD) {
                itemMap[decKey] = false;
            } else {
                const intValue = decryptInt(decValB64);
                if (intValue !== null) {
                    itemMap[decKey] = intValue;
                } else {
                    itemMap[decKey] = decValB64; // Keep as Base64 if not a known type
                }
            }
        } catch (e) {
            console.error(`[Line ${lineCount}] Error processing line: ${e.message}. Halting process.`);
            process.exit(1);
        }
    }

    const outputFilePath = path.join(__dirname, OUTPUT_FILENAME);
    fs.writeFileSync(outputFilePath, JSON.stringify(itemMap, null, 2));

    console.log(`Decryption successful. Found ${Object.keys(itemMap).length} items.`);
    console.log(`Output saved to '${OUTPUT_FILENAME}'.`);
}

// Execute the decryption
decryptFile();
