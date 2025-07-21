"""Protocol for cryptographic operations."""

from typing import Protocol


class CryptoManagerProtocol(Protocol):
    """Defines the interface for an encryption/decryption manager."""

    def encrypt(self, data: bytes) -> bytes:
        """
        Encrypts the given data.

        Args:
            data: The data to encrypt.

        Returns:
            The encrypted data.
        """
        ...

    def decrypt(self, data: bytes) -> bytes:
        """
        Decrypts the given data.

        Args:
            data: The data to decrypt.

        Returns:
            The decrypted data.
        """
        ...
