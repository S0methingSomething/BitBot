"""Service for cryptographic operations using Fernet."""

import base64

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from bitbot.interfaces.crypto_manager import CryptoManagerProtocol


class FernetCryptoManager(CryptoManagerProtocol):
    """Manages encryption and decryption using Fernet."""

    def __init__(self, encryption_key: str) -> None:
        """
        Initializes the FernetCryptoManager.

        Args:
            encryption_key: The key to use for encryption.
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b"salt",  # In a real app, use a unique salt per user
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(encryption_key.encode()))
        self._fernet = Fernet(key)

    def encrypt(self, data: bytes) -> bytes:
        """Encrypts the given data."""
        return self._fernet.encrypt(data)

    def decrypt(self, data: bytes) -> bytes:
        """Decrypts the given data."""
        return self._fernet.decrypt(data)
