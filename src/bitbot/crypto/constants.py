"""Cryptographic constants for game asset file patching.

WARNING: DEFAULT_CIPHER_KEY is hardcoded for the specific game being patched.
If key rotation is needed, this must be updated.
"""

# Default cipher key for game asset encryption
DEFAULT_CIPHER_KEY: str = "com.wtfapps.apollo16"

# Base64-encoded .NET serialized boolean values
B64_NET_BOOLEAN_TRUE: str = (
    "AAEAAAD/////AQAAAAAAAAAEAQAAAA5TeXN0ZW0uQm9vbGVhbgEAAAAHbV92YWx1ZQABAQs="
)
B64_NET_BOOLEAN_FALSE: str = (
    "AAEAAAD/////AQAAAAAAAAAEAQAAAA5TeXN0ZW0uQm9vbGVhbgEAAAAHbV92YWx1ZQABAAw="
)

# Character obfuscation map (lowercase a-z only)
# Maps ASCII codes: a→z, b→m, c→y, etc.
# NOTE: Only handles lowercase letters. Uppercase and numbers pass through unchanged.
OBF_CHAR_MAP: dict[int, int] = {
    0x61: 0x7A,  # a → z
    0x62: 0x6D,  # b → m
    0x63: 0x79,  # c → y
    0x64: 0x6C,  # d → l
    0x65: 0x78,  # e → x
    0x66: 0x6B,  # f → k
    0x67: 0x77,  # g → w
    0x68: 0x6A,  # h → j
    0x69: 0x76,  # i → v
    0x6A: 0x69,  # j → i
    0x6B: 0x75,  # k → u
    0x6C: 0x68,  # l → h
    0x6D: 0x74,  # m → t
    0x6E: 0x67,  # n → g
    0x6F: 0x73,  # o → s
    0x70: 0x66,  # p → f
    0x71: 0x72,  # q → r
    0x72: 0x65,  # r → e
    0x73: 0x71,  # s → q
    0x74: 0x64,  # t → d
    0x75: 0x70,  # u → p
    0x76: 0x63,  # v → c
    0x77: 0x6F,  # w → o
    0x78: 0x62,  # x → b
    0x79: 0x6E,  # y → n
    0x7A: 0x61,  # z → a
}
