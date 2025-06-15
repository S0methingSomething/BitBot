/*
 * BitEdit - MonetizationVars Decryptor (Node.js version)
 * This script is for manual use or reference. It is not run by the bot.
 * Original logic credits go to yntha (https://github.com/yntha/bitlife-edit).
 * Licensed under GPLv3.
 */

import fs from 'fs';
import path from 'path';

// --- Constants ---
const DEFAULT_CIPHER_KEY = "com.wtfapps.apollo16";
const B64_NET_BOOLEAN_TRUE_STANDARD = "AAEAAAD/////AQAAAAAAAAAEAQAAAA5TeXN0ZW0uQm9vbGVhbgEAAAAHbV92YWx1ZQABAQs=";
const B64_NET_BOOLEAN_TRUE_VARIANT  = "AAEAAAD/////AQAAAAAAAAAEAQAAAA5TeXN0ZW0uQm9vbGVhbgEAAAAHbV92YWx1ZQABAAs=";
const B64_NET_BOOLEAN_FALSE_STANDARD= "AAEAAAD/////AQAAAAAAAAAEAQAAAA5TeXN0ZW0uQm9vbGVhbgEAAAAHbV92YWx1ZQABAAw=";
const USER_SERIALIZED_INT32_PREFIX = new Uint8Array([0, 1, 0, 0, 0, 255, 255, 255, 255, 1, 0, 0, 0, 0, 0, 0, 0, 4, 1, 0, 0, 0, 12, 83, 121, 115, 116, 101, 109, 46, 73, 110, 116, 51, 50, 1, 0, 0, 0, 7, 109, 95, 118, 97, 108, 117, 101, 0, 8]);
const USER_SERIALIZED_INT32_SUFFIX = new Uint8Array([11]);
const USER_SERIALIZED_INT32_TOTAL_LENGTH = USER_SERIALIZED_INT32_PREFIX.length + 4 + USER_SERIALIZED_INT32_SUFFIX.length;

// --- Obfuscation Map ---
const obfCharMap = {0x61:0x7a,0x62:0x6d,0x63:0x79,0x64:0x6c,0x65:0x78,0x66:0x6b,0x67:0x77,0x68:0x6a,0x69:0x76,0x6a:0x69,0x6b:0x75,0x6c:0x68,0x6d:0x74,0x6e:0x67,0x6f:0x73,0x70:0x66,0x71:0x72,0x72:0x65,0x73:0x71,0x74:0x64,0x75:0x70,0x76:0x63,0x77:0x6f,0x78:0x62,0x79:0x6e,0x7a:0x61};

// --- Utility Functions ---
function arraysEqual(a, b) { if (!a || !b || a.length !== b.length) return false; for (let i = 0; i < a.length; i++) { if (a[i] !== b[i]) return false; } return true; }
function getObfuscatedKey(key) {let oKey = ""; for (const char of key.toLowerCase()) { const c = char.charCodeAt(0); oKey += String.fromCharCode(obfCharMap[c] || c); } return oKey;}
function base64ToUtf8String(b64) { return Buffer.from(b64, 'base64').toString('utf8'); }
function base64DecodeAndXOR(b64, key) { let dec; try { dec = base64ToUtf8String(b64); } catch (e) { throw e; } let x = ""; for (let i=0; i<dec.length; i++) {x += String.fromCharCode(dec.charCodeAt(i) ^ key.charCodeAt(i % key.length));} return x; }
function decryptInt(base64String) { try { const bytes = Buffer.from(base64String, 'base64'); if (bytes.length !== USER_SERIALIZED_INT32_TOTAL_LENGTH) return null; const prefixBytesFromFile = bytes.slice(0, USER_SERIALIZED_INT32_PREFIX.length); const suffixByteFromFile = bytes[bytes.length - 1]; if (!arraysEqual(prefixBytesFromFile, USER_SERIALIZED_INT32_PREFIX) || suffixByteFromFile !== USER_SERIALIZED_INT32_SUFFIX[0]) return null; return bytes.readInt32LE(USER_SERIALIZED_INT32_PREFIX.length); } catch (e) { return null; } }

/**
 * Main function to decrypt the MonetizationVars file.
 */
function decryptFile(inputFilePath, outputFilePath) {
    console.log(`Starting decryption of '${inputFilePath}'...`);
    if (!fs.existsSync(inputFilePath)) {
        console.error(`Error: Input file not found at '${inputFilePath}'.`);
        process.exit(1);
    }

    const fileContent = fs.readFileSync(inputFilePath, 'utf-8');
    const obfuscatedKey = getObfuscatedKey(DEFAULT_CIPHER_KEY);
    const itemMap = {};
    const lines = fileContent.split('\n').filter(line => line.trim() !== '');

    for (const line of lines) {
        const parts = line.split(/:(.+)/);
        if (parts.length < 2 || !parts[1]) continue;
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
                itemMap[decKey] = intValue !== null ? intValue : decValB64;
            }
        } catch (e) {
            console.error(`Error processing line: ${line}`, e);
            process.exit(1);
        }
    }
    fs.writeFileSync(outputFilePath, JSON.stringify(itemMap, null, 2));
    console.log(`Decryption successful. Output saved to '${outputFilePath}'.`);
}

// To run this manually: node decrypt.js <input-file> <output-file>
if (process.argv.length === 4) {
    const inputFile = process.argv[2];
    const outputFile = process.argv[3];
    decryptFile(inputFile, outputFile);
}            const decKey = base64DecodeAndXOR(encKey, obfuscatedKey);
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
