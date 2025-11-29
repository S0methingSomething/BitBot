"""BitBot Core Processor: Decrypts, Modifies, and Re-encrypts a target asset file."""

from pathlib import Path

from beartype import beartype

from bitbot.core.result import Err, Ok, Result
from bitbot.crypto.cipher import decrypt, encrypt
from bitbot.crypto.constants import DEFAULT_CIPHER_KEY
from bitbot.crypto.modifier import modify
from bitbot.crypto.obfuscation import get_obfuscated_key


@beartype
def process_file(input_path: Path, output_path: Path) -> Result[None, str]:
    """Process file with encryption/decryption."""
    if not input_path.exists():
        return Err(f"Input file not found: {input_path}")

    try:
        encrypted_content = input_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        return Err(f"Failed to read input file: {e}")

    try:
        obfuscated_key = get_obfuscated_key(DEFAULT_CIPHER_KEY)
        decrypted_data = decrypt(encrypted_content, obfuscated_key)
        modified_data = modify(decrypted_data)
        encrypted_output = encrypt(modified_data, obfuscated_key)
    except (ValueError, KeyError) as e:
        return Err(f"Processing failed: {e}")

    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(encrypted_output, encoding="utf-8")
    except OSError as e:
        return Err(f"Failed to write output file: {e}")

    return Ok(None)
