"""BitBot Core Processor: Decrypts, Modifies, and Re-encrypts a target asset file."""

import sys
from pathlib import Path

import deal
from beartype import beartype

from crypto.cipher import decrypt, encrypt
from crypto.constants import DEFAULT_CIPHER_KEY
from crypto.modifier import modify
from crypto.obfuscation import get_obfuscated_key


@deal.post(lambda result: result is None)  # type: ignore[misc]
@beartype  # type: ignore[misc]
def main() -> None:
    """Main function to orchestrate the file processing."""
    if len(sys.argv) != 3:  # noqa: PLR2004
        sys.exit(1)

    input_file_path = Path(sys.argv[1])
    output_file_path = Path(sys.argv[2])

    if not input_file_path.exists():
        sys.exit(1)

    try:
        encrypted_content = input_file_path.read_text(encoding="utf-8")
    except Exception:  # noqa: BLE001
        sys.exit(1)

    obfuscated_key = get_obfuscated_key(DEFAULT_CIPHER_KEY)
    decrypted_data = decrypt(encrypted_content, obfuscated_key)
    modified_data = modify(decrypted_data)
    encrypted_output = encrypt(modified_data, obfuscated_key)

    try:
        output_file_path.write_text(encrypted_output, encoding="utf-8")
    except Exception:  # noqa: BLE001
        sys.exit(1)


if __name__ == "__main__":
    main()
