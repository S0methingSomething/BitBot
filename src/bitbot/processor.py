# -*- coding: utf-8 -*-
"""This module orchestrates the file processing by calling the crypto module.
"""
import sys

from . import crypto
from .logging import get_logger

logger = get_logger(__name__)


def process_file(input_file: str, output_file: str) -> None:
    """Uses the crypto module to decrypt, modify, and re-encrypt a file."""
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            encrypted_content = f.read()

        obfuscated_key = crypto.get_obfuscated_key(crypto.DEFAULT_CIPHER_KEY)
        decrypted_data = crypto.decrypt(encrypted_content, obfuscated_key)
        modified_data = crypto.modify(decrypted_data)
        re_encrypted_content = crypto.encrypt(modified_data, obfuscated_key)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(re_encrypted_content)

    except FileNotFoundError:
        logger.error(f"Input file not found at {input_file}", exc_info=True)
        sys.exit(1)
    except Exception as e:
        logger.error(f"Failed to process file with crypto module: {e}", exc_info=True)
        sys.exit(1)
