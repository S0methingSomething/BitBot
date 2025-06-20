// BitBot Core Processor: Decrypts, Modifies, and Re-encrypts MonetizationVars
const fs = require('fs');
const path = require('path');

// --- Constants ---
const DEFAULT_CIPHER_KEY = "com.wtfapps.apollo16";
const B64_NET_BOOLEAN_TRUE = "AAEAAAD/////AQAAAAAAAAAEAQAAAA5TeXN0ZW0uQm9vbGVhbgEAAAAHbV92YWx1ZQABAQs=";
const B64_NET_BOOLEAN_FALSE = "AAEAAAD/////AQAAAAAAAAAEAQAAAA5TeXN0ZW0uQm9vbGVhbgEAAAAHbV92YWx1ZQABAAw=";
const obfCharMap = {0x61:0x7a,0x62:0x6d,0x63:0x79,0x64:0x6c,0x65:0x78,0x66:0x6b,0x67:0x77,0x68:0x6a,0x69:0x76,0x6a:0x69,0x6b:0x75,0x6c:0x68,0x6d:0x74,0x6e:0x67,0x6f:0x73,0x70:0x66,0x71:0x72,0x72:0x65,0x73:0x71,0x74:0x64,0x75:0x70,0x76:0x63,0x77:0x6f,0x78:0x62,0x79:0x6e,0x7a:0x61};

// --- Utility Functions ---
const getObfuscatedKey = (key) => {
    let oKey = "";
    for (const char of key.toLowerCase()) {
        const code = char.charCodeAt(0);
        oKey += obfCharMap.hasOwnProperty(code)
            ? String.fromCharCode(obfCharMap[code])
            : char;
    }
    return oKey;
};
const xorAndB64Encode = (text, key) => {
    let xorResult = "";
    for (let i = 0; i < text.length; i++) {
        xorResult += String.fromCharCode(text.charCodeAt(i) ^ key.charCodeAt(i % key.length));
    }
    return Buffer.from(xorResult, 'latin1').toString('base64');
};
const b64DecodeAndXor = (b64, key) => {
    const decoded = Buffer.from(b64, 'base64').toString('latin1');
    let result = "";
    for (let i = 0; i < decoded.length; i++) {
        result += String.fromCharCode(decoded.charCodeAt(i) ^ key.charCodeAt(i % key.length));
    }
    return result;
};

// --- Core Processing Functions ---
function decrypt(encryptedContent, obfuscatedKey) {
    const itemMap = {};
    for (const line of encryptedContent.split('\n').filter(l => l.trim())) {
        const [encKey, encVal] = line.split(/:(.+)/);
        if (!encKey || !encVal) continue;
        const decKey = b64DecodeAndXor(encKey.trim(), obfuscatedKey);
        const decValB64 = b64DecodeAndXor(encVal.trim(), obfuscatedKey);
        if (decValB64 === B64_NET_BOOLEAN_TRUE) itemMap[decKey] = true;
        else if (decValB64 === B64_NET_BOOLEAN_FALSE) itemMap[decKey] = false;
        else itemMap[decKey] = decValB64;
    }
    return itemMap;
}

function modify(dataObject) {
    console.log("Modifying data: Setting all boolean 'false' values to 'true'.");
    for (const key in dataObject) {
        if (dataObject[key] === false) {
            dataObject[key] = true;
        }
    }
    return dataObject;
}

function encrypt(dataObject, obfuscatedKey) {
    console.log("Re-encrypting data...");
    let outputContent = "";
    for (const key in dataObject) {
        const value = dataObject[key];
        const encryptedKey = xorAndB64Encode(key, obfuscatedKey);
        let valueToSerialize;
        if (value === true) {
            valueToSerialize = B64_NET_BOOLEAN_TRUE;
        } else if (value === false) {
            valueToSerialize = B64_NET_BOOLEAN_FALSE;
        } else {
            valueToSerialize = value;
        }
        const encryptedValue = xorAndB64Encode(valueToSerialize, obfuscatedKey);
        outputContent += `${encryptedKey}:${encryptedValue}\n`;
    }
    return outputContent.trim();
}

function main() {
    const inputFile = process.argv[2];
    const outputFile = process.argv[3];
    if (!inputFile || !outputFile) {
        console.error("Usage: node process_vars.js <input-file> <output-file>");
        process.exit(1);
    }
    console.log(`Processing file: ${inputFile}`);
    const obfuscatedKey = getObfuscatedKey(DEFAULT_CIPHER_KEY);
    const encryptedContent = fs.readFileSync(inputFile, 'utf-8');
    const decryptedData = decrypt(encryptedContent, obfuscatedKey);
    const modifiedData = modify(decryptedData);
    const reEncryptedContent = encrypt(modifiedData, obfuscatedKey);
    fs.writeFileSync(outputFile, reEncryptedContent);
    console.log(`Successfully processed and saved patched file to: ${outputFile}`);
}

main();
