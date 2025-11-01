#!/usr/bin/env python3
"""Validation coverage checker for CI - fails if coverage below threshold."""

import ast
import sys
from pathlib import Path


def analyze_file(filepath: Path) -> tuple[int, int]:
    """Return (total_functions, validated_functions)."""
    with open(filepath) as f:
        tree = ast.parse(f.read(), filename=str(filepath))

    total = validated = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
            total += 1
            has_validation = any(
                "deal" in ast.unparse(d) or "beartype" in ast.unparse(d)
                for d in node.decorator_list
            )
            if has_validation:
                validated += 1

    return total, validated


def main() -> None:
    """Check validation coverage meets threshold."""
    threshold = float(sys.argv[1]) if len(sys.argv) > 1 else 90.0

    src_dir = Path("src")
    total = validated = 0

    for filepath in src_dir.rglob("*.py"):
        if filepath.name == "__init__.py":
            continue
        t, v = analyze_file(filepath)
        total += t
        validated += v

    coverage = (validated / total * 100) if total > 0 else 0

    print(f"Validation Coverage: {validated}/{total} ({coverage:.1f}%)")
    print(f"Threshold: {threshold}%")

    if coverage < threshold:
        print(f"❌ FAILED: Coverage {coverage:.1f}% below threshold {threshold}%")
        sys.exit(1)

    print("✅ PASSED: Coverage meets threshold")


if __name__ == "__main__":
    main()
