"""Service for patching the asset file."""

import base64


class FilePatcherService:
    """Handles the core logic of decrypting, modifying, and re-encrypting
    the target asset file.
    """

    _DEFAULT_CIPHER_KEY = "com.wtfapps.apollo16"
    _B64_NET_BOOLEAN_TRUE = "AAEAAAD/////AQAAAAAAAAAEAQAAAA5TeXN0ZW0uQm9vbGVhbgEAAAAHbV92YWx1ZQABAQs="
    _B64_NET_BOOLEAN_FALSE = "AAEAAAD/////AQAAAAAAAAAEAQAAAA5TeXN0ZW0uQm9vbGVhbgEAAAAHbV92YWx1ZQABAAw="
    _OBF_CHAR_MAP = {
        0x61: 0x7A,
        0x62: 0x6D,
        0x63: 0x79,
        0x64: 0x6C,
        0x65: 0x78,
        0x66: 0x6B,
        0x67: 0x77,
        0x68: 0x6A,
        0x69: 0x76,
        0x6A: 0x69,
        0x6B: 0x75,
        0x6C: 0x68,
        0x6D: 0x74,
        0x6E: 0x67,
        0x6F: 0x73,
        0x70: 0x66,
        0x71: 0x72,
        0x72: 0x65,
        0x73: 0x71,
        0x74: 0x64,
        0x75: 0x70,
        0x76: 0x63,
        0x77: 0x6F,
        0x78: 0x62,
        0x79: 0x6E,
        0x7A: 0x61,
    }

    def patch_file_content(self, content: str) -> str:
        """Takes the string content of an asset file, patches it, and returns
        the new content.
        """
        obfuscated_key = self._get_obfuscated_key(self._DEFAULT_CIPHER_KEY)
        decrypted_data = self._decrypt(content, obfuscated_key)
        modified_data = self._modify(decrypted_data)
        return self._encrypt(modified_data, obfuscated_key)

    def _get_obfuscated_key(self, key: str) -> str:
        """Applies a simple character substitution obfuscation."""
        return "".join(chr(self._OBF_CHAR_MAP.get(ord(char), ord(char))) for char in key.lower())

    def _xor_and_b64_encode(self, text: str, key: str) -> str:
        """Performs an XOR operation and then Base64 encodes the result."""
        key_bytes = key.encode("latin-1")
        text_bytes = text.encode("latin-1")
        xor_result = bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(text_bytes)])
        return base64.b64encode(xor_result).decode("utf-8")

    def _b64_decode_and_xor(self, b64: str, key: str) -> str:
        """Decodes a Base64 string and then performs an XOR operation."""
        key_bytes = key.encode("latin-1")
        decoded_bytes = base64.b64decode(b64)
        xor_result = bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(decoded_bytes)])
        return xor_result.decode("latin-1")

    def _decrypt(self, encrypted_content: str, obfuscated_key: str) -> dict[str, bool | str]:
        """Decrypts the content of the asset file into a Python dictionary."""
        item_map: dict[str, bool | str] = {}
        for line in encrypted_content.splitlines():
            if not line.strip() or ":" not in line:
                continue
            enc_key, enc_val = line.split(":", 1)
            dec_key = self._b64_decode_and_xor(enc_key.strip(), obfuscated_key)
            dec_val_b64 = self._b64_decode_and_xor(enc_val.strip(), obfuscated_key)

            if dec_val_b64 == self._B64_NET_BOOLEAN_TRUE:
                item_map[dec_key] = True
            elif dec_val_b64 == self._B64_NET_BOOLEAN_FALSE:
                item_map[dec_key] = False
            else:
                item_map[dec_key] = dec_val_b64
        return item_map

    def _modify(self, data_object: dict[str, bool | str]) -> dict[str, bool | str]:
        """Sets all boolean false values to true."""
        for key, value in data_object.items():
            if value is False:
                data_object[key] = True
        return data_object

    def _encrypt(self, data_object: dict[str, bool | str], obfuscated_key: str) -> str:
        """Re-encrypts the modified data object back into the file format."""
        output_lines = []
        for key, value in data_object.items():
            encrypted_key = self._xor_and_b64_encode(key, obfuscated_key)
            if value is True:
                value_to_serialize = self._B64_NET_BOOLEAN_TRUE
            elif value is False:
                value_to_serialize = self._B64_NET_BOOLEAN_FALSE
            else:
                value_to_serialize = str(value)
            encrypted_value = self._xor_and_b64_encode(value_to_serialize, obfuscated_key)
            output_lines.append(f"{encrypted_key}:{encrypted_value}")
        return "\n".join(output_lines)
