# -*- coding: utf-8 -*-
"""
BitBot Core Processor: Decrypts, Modifies, and Re-encrypts a target asset file.
This script is a Python port of the original Node.js version, designed to handle
a simple XOR-encrypted, base64-encoded key-value file format, where it sets
all boolean `false` values to `true`.
"""
import sys
import base64

# --- Constants ---
DEFAULT_CIPHER_KEY = "com.wtfapps.apollo16"
B64_NET_BOOLEAN_TRUE = "AAEAAAD/////AQAAAAAAAAAEAQAAAA5TeXN0ZW0uQm9vbGVhbgEAAAAHbV92YWx1ZQABAQs="
B64_NET_BOOLEAN_FALSE = "AAEAAAD/////AQAAAAAAAAAEAQAAAA5TeXN0ZW0uQm9vbGVhbgEAAAAHbV92YWx1ZQABAAw="
OBF_CHAR_MAP = {0x61:0x7a,0x62:0x6d,0x63:0x79,0x64:0x6c,0x65:0x78,0x66:0x6b,0x67:0x77,0x68:0x6a,0x69:0x76,0x6a:0x69,0x6b:0x75,0x6c:0x68,0x6d:0x74,0x6e:0x67,0x6f:0x73,0x70:0x66,0x71:0x72,0x72:0x65,0x73:0x71,0x74:0x64,0x75:0x70,0x76:0x63,0x77:0x6f,0x78:0x62,0x79:0x6e,0x7a:0x61}

def get_obfuscated_key(key: str) -> str:
    """Applies a simple character substitution obfuscation to the cipher key."""
    o_key = ""
    for char in key.lower():
        code = ord(char)
        o_key += chr(OBF_CHAR_MAP.get(code, code))
    return o_key

def xor_and_b64_encode(text: str, key: str) -> str:
    """Performs an XOR operation and then Base64 encodes the result."""
    key_bytes = key.encode('latin-1')
    text_bytes = text.encode('latin-1')
    xor_result = bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(text_bytes)])
    return base64.b64encode(xor_result).decode('utf-8')

def b64_decode_and_xor(b64: str, key: str) -> str:
    """Decodes a Base64 string and then performs an XOR operation."""
    key_bytes = key.encode('latin-1')
    decoded_bytes = base64.b64decode(b64)
    xor_result = bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(decoded_bytes)])
    return xor_result.decode('latin-1')

def decrypt(encrypted_content: str, obfuscated_key: str) -> dict:
    """Decrypts the content of the asset file into a Python dictionary."""
    item_map = {}
    for line in encrypted_content.splitlines():
        if not line.strip():
            continue
        parts = line.split(':', 1)
        if len(parts) != 2:
            continue
        enc_key, enc_val = parts
        dec_key = b64_decode_and_xor(enc_key.strip(), obfuscated_key)
        dec_val_b64 = b64_decode_and_xor(enc_val.strip(), obfuscated_key)
        
        if dec_val_b64 == B64_NET_BOOLEAN_TRUE:
            item_map[dec_key] = True
        elif dec_val_b64 == B64_NET_BOOLEAN_FALSE:
            item_map[dec_key] = False
        else:
            item_map[dec_key] = dec_val_b64
    return item_map

def modify(data_object: dict) -> dict:
    """Modifies the decrypted data object by setting all boolean false values to true."""
    print("Modifying data: Setting all boolean 'false' values to 'true'.")
    for key, value in data_object.items():
        if value is False:
            data_object[key] = True
    return data_object

def encrypt(data_object: dict, obfuscated_key: str) -> str:
    """Re-encrypts the modified data object back into the file format."""
    print("Re-encrypting data...")
    output_lines = []
    for key, value in data_object.items():
        encrypted_key = xor_and_b64_encode(key, obfuscated_key)
        
        if value is True:
            value_to_serialize = B64_NET_BOOLEAN_TRUE
        elif value is False:
            value_to_serialize = B64_NET_BOOLEAN_FALSE
        else:
            value_to_serialize = value
            
        encrypted_value = xor_and_b64_encode(value_to_serialize, obfuscated_key)
        output_lines.append(f"{encrypted_key}:{encrypted_value}")
    return "\n".join(output_lines)

def main():
    """Main function to orchestrate the file processing."""
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <input-file> <output-file>", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    print(f"Processing file: {input_file}")
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            encrypted_content = f.read()
            
        obfuscated_key = get_obfuscated_key(DEFAULT_CIPHER_KEY)
        
        decrypted_data = decrypt(encrypted_content, obfuscated_key)
        modified_data = modify(decrypted_data)
        re_encrypted_content = encrypt(modified_data, obfuscated_key)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(re_encrypted_content)
            
        print(f"Successfully processed and saved patched file to: {output_file}")

    except FileNotFoundError:
        print(f"Error: Input file not found at {input_file}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
