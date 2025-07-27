# src/bitbot/services/patcher.py
"""
A service for patching files using XOR-based encryption/decryption.
"""

import base64

class PatcherService:
    """
    Replicates the logic from the original process_vars.js script.
    """
    DEFAULT_CIPHER_KEY = "com.wtfapps.apollo16"
    B64_NET_BOOLEAN_TRUE = "AAEAAAD/////AQAAAAAAAAAEAQAAAA5TeXN0ZW0uQm9vbGVhbgEAAAAHbV92YWx1ZQABAQs="
    B64_NET_BOOLEAN_FALSE = "AAEAAAD/////AQAAAAAAAAAEAQAAAA5TeXN0ZW0uQm9vbGVhbgEAAAAHbV92YWx1ZQABAAw="
    OBF_CHAR_MAP = {
        0x61: 0x7a, 0x62: 0x6d, 0x63: 0x79, 0x64: 0x6c, 0x65: 0x78, 0x66: 0x6b,
        0x67: 0x77, 0x68: 0x6a, 0x69: 0x76, 0x6a: 0x69, 0x6b: 0x75, 0x6c: 0x68,
        0x6d: 0x74, 0x6e: 0x67, 0x6f: 0x73, 0x70: 0x66, 0x71: 0x72, 0x72: 0x65,
        0x73: 0x71, 0x74: 0x64, 0x75: 0x70, 0x76: 0x63, 0x77: 0x6f, 0x78: 0x62,
        0x79: 0x6e, 0x7a: 0x61
    }

    def _get_obfuscated_key(self, key: str) -> str:
        o_key = ""
        for char in key.lower():
            code = ord(char)
            o_key += chr(self.OBF_CHAR_MAP.get(code, code))
        return o_key

    def _xor_and_b64_encode(self, text: str, key: str) -> str:
        xor_result = ""
        for i, char in enumerate(text):
            xor_result += chr(ord(char) ^ ord(key[i % len(key)]))
        return base64.b64encode(xor_result.encode("latin1")).decode("utf-8")

    def _b64_decode_and_xor(self, b64: str, key: str) -> str:
        decoded = base64.b64decode(b64).decode("latin1")
        result = ""
        for i, char in enumerate(decoded):
            result += chr(ord(char) ^ ord(key[i % len(key)]))
        return result

    def decrypt(self, encrypted_content: str, obfuscated_key: str) -> dict:
        item_map = {}
        for line in encrypted_content.split('\n'):
            if not line.strip():
                continue
            parts = line.split(':', 1)
            if len(parts) != 2:
                continue
            enc_key, enc_val = parts
            dec_key = self._b64_decode_and_xor(enc_key.strip(), obfuscated_key)
            dec_val_b64 = self._b64_decode_and_xor(enc_val.strip(), obfuscated_key)

            if dec_val_b64 == self.B64_NET_BOOLEAN_TRUE:
                item_map[dec_key] = True
            elif dec_val_b64 == self.B64_NET_BOOLEAN_FALSE:
                item_map[dec_key] = False
            else:
                item_map[dec_key] = dec_val_b64
        return item_map

    def modify(self, data_object: dict) -> dict:
        for key in data_object:
            if data_object[key] is False:
                data_object[key] = True
        return data_object

    def encrypt(self, data_object: dict, obfuscated_key: str) -> str:
        output_content = ""
        for key, value in data_object.items():
            encrypted_key = self._xor_and_b64_encode(key, obfuscated_key)
            
            if value is True:
                value_to_serialize = self.B64_NET_BOOLEAN_TRUE
            elif value is False:
                value_to_serialize = self.B64_NET_BOOLEAN_FALSE
            else:
                value_to_serialize = value
            
            encrypted_value = self._xor_and_b64_encode(str(value_to_serialize), obfuscated_key)
            output_content += f"{encrypted_key}:{encrypted_value}\n"
        return output_content.strip()

    def patch_file_content(self, content: str) -> str:
        """
        Decrypts, modifies, and re-encrypts the given content.
        """
        obfuscated_key = self._get_obfuscated_key(self.DEFAULT_CIPHER_KEY)
        decrypted_data = self.decrypt(content, obfuscated_key)
        modified_data = self.modify(decrypted_data)
        re_encrypted_content = self.encrypt(modified_data, obfuscated_key)
        return re_encrypted_content
