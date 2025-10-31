"""BitBot Core Processor: Decrypts, Modifies, and Re-encrypts a target asset file."""

import sys
from pathlib import Path

import deal
from beartype import beartype

from core.result import Err, Ok, Result
from crypto.cipher import decrypt, encrypt
from crypto.constants import DEFAULT_CIPHER_KEY
from crypto.modifier import modify
from crypto.obfuscation import get_obfuscated_key


@beartype  # type: ignore[misc]
def process_file(input_path: Path, output_path: Path) -> Result[None, str]:
    """Process file with encryption/decryption."""
    if not input_path.exists():
        return Err(f"Input file not found: {input_path}")
    
    try:
        encrypted_content = input_path.read_text(encoding="utf-8")
    except Exception as e:
        return Err(f"Failed to read input file: {e}")
    
    try:
        obfuscated_key = get_obfuscated_key(DEFAULT_CIPHER_KEY)
        decrypted_data = decrypt(encrypted_content, obfuscated_key)
        modified_data = modify(decrypted_data)
        encrypted_output = encrypt(modified_data, obfuscated_key)
    except Exception as e:
        return Err(f"Processing failed: {e}")
    
    try:
        output_path.write_text(encrypted_output, encoding="utf-8")
    except Exception as e:
        return Err(f"Failed to write output file: {e}")
    
    return Ok(None)


@deal.post(lambda result: result is None)  # type: ignore[misc]
@beartype  # type: ignore[misc]
def main() -> None:
    """Main function to orchestrate the file processing."""
    if len(sys.argv) != 3:  # noqa: PLR2004
        print("Usage: patch_file.py <input_file> <output_file>", file=sys.stderr)
        sys.exit(1)

    input_file_path = Path(sys.argv[1])
    output_file_path = Path(sys.argv[2])

    result = process_file(input_file_path, output_file_path)
    
    if result.is_err():
        print(f"Error: {result.error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
