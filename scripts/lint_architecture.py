"""
An AST-based linter to enforce architectural rules.

This script ensures that only specific modules are allowed to import
libraries that we want to keep isolated (e.g., `praw`, `asyncpraw`).
This helps maintain a clean, decoupled architecture.
"""

import ast
import os
import sys
from pathlib import Path
from typing import List

from bitbot.logging import get_logger

# --- Configuration ---
# A dictionary where the key is the restricted module and the value is the
# path of the ONLY module allowed to import it.
RESTRICTED_IMPORTS = {
    "praw": "src/bitbot/services/praw_manager.py",
    "asyncpraw": "src/bitbot/services/praw_manager.py",
}

# The directory to scan.
SRC_DIRECTORY = "src/bitbot"

logger = get_logger(__name__)


class ImportVisitor(ast.NodeVisitor):
    """An AST visitor that finds all import statements in a file."""

    def __init__(self, file_path: Path) -> None:
        """Initializes the ImportVisitor."""
        self.file_path = file_path
        self.violations: List[str] = []

    def check_import(self, module_name: str, line_number: int) -> None:
        """Checks if an import is a violation of our architectural rules."""
        if module_name in RESTRICTED_IMPORTS:
            allowed_path_str = RESTRICTED_IMPORTS[module_name]
            allowed_path = Path(allowed_path_str).resolve()

            if self.file_path.resolve() != allowed_path:
                violation = (
                    f"{self.file_path}:{line_number}: Architectural violation: "
                    f"Import of restricted module '{module_name}' is only allowed in "
                    f"'{allowed_path_str}'."
                )
                self.violations.append(violation)

    def visit_Import(self, node: ast.Import) -> None:
        """Visits `import <module>` statements."""
        for alias in node.names:
            self.check_import(alias.name, node.lineno)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Visits `from <module> import ...` statements."""
        if node.module:
            self.check_import(node.module, node.lineno)
        self.generic_visit(node)


def main() -> int:
    """
    Main function to run the architectural linter.

    Returns:
        The exit code.
    """
    all_violations: List[str] = []
    root_path = Path(SRC_DIRECTORY)

    for dirpath, _, filenames in os.walk(root_path):
        for filename in filenames:
            if filename.endswith(".py"):
                file_path = Path(dirpath) / filename
                try:
                    with file_path.open("r", encoding="utf-8") as f:
                        content = f.read()
                        tree = ast.parse(content, filename=str(file_path))
                        visitor = ImportVisitor(file_path)
                        visitor.visit(tree)
                        all_violations.extend(visitor.violations)
                except Exception as e:
                    logger.error(f"Error parsing {file_path}: {e}")
                    return 1

    if all_violations:
        logger.error("Architectural violations found:")
        for violation in all_violations:
            logger.error(f" - {violation}")
        return 1

    logger.info("Architectural checks passed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
