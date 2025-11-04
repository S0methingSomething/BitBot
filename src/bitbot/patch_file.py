"""BitBot Core Processor: Decrypts, Modifies, and Re-encrypts a target asset file."""

import sys
from pathlib import Path

from beartype import beartype

from bitbot.core.error_logger import get_logger
from bitbot.core.result import Err, Ok, Result
from bitbot.crypto.cipher import decrypt, encrypt
from bitbot.crypto.constants import DEFAULT_CIPHER_KEY
from bitbot.crypto.modifier import modify
from bitbot.crypto.obfuscation import get_obfuscated_key

logger = get_logger()


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


@beartype
def main() -> None:
    """Main function to orchestrate the file processing."""
    if len(sys.argv) != 3:
        logger.error("Usage: bitbot patch <input_file> <output_file>")
        sys.exit(1)

    input_file_path = Path(sys.argv[1])
    output_file_path = Path(sys.argv[2])

    result = process_file(input_file_path, output_file_path)

    if result.is_err():
        logger.error("Error: %s", result.unwrap_err())
        sys.exit(1)


if __name__ == "__main__":
    main()
