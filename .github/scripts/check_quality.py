#!/usr/bin/env python3
"""Comprehensive code quality checker - runs full validation stack."""

import subprocess
import sys


def run_check(name: str, cmd: list[str], allow_fail: bool = False) -> bool:
    """Run a check and return success status."""
    print(f'\n{"="*60}')
    print(f"{name}")
    print(f'{"="*60}')

    result = subprocess.run(cmd, check=False)

    if result.returncode != 0 and not allow_fail:
        print(f"\n❌ {name} FAILED (exit code: {result.returncode})")
        return False

    print(f"\n✅ {name} PASSED")
    return True


def main() -> None:
    """Run all quality checks."""
    checks = [
        ("Type Checking (mypy)", ["uv", "run", "mypy", "src/"]),
        ("Linting (ruff)", ["uv", "run", "ruff", "check", "src/", "tests/"]),
        (
            "Runtime Type Checking (beartype)",
            ["uv", "run", "python", ".github/scripts/check_validation.py", "90"],
        ),
        (
            "Contract Validation (deal)",
            ["uv", "run", "python", ".github/scripts/check_validation.py", "90"],
        ),
        (
            "Data Validation (pydantic)",
            [
                "uv",
                "run",
                "python",
                "-c",
                'from src.models import *; print("✅ Pydantic models valid")',
            ],
        ),
        ("Complexity Check", ["uv", "run", "python", ".github/scripts/check_complexity.py", "15"]),
        (
            "Docstring Coverage (interrogate)",
            ["uv", "run", "interrogate", "-v", "src/", "--fail-under=80"],
        ),
        ("Dead Code (vulture)", ["uv", "run", "vulture", "src/", "--min-confidence=80"]),
        ("Dependency Check (deptry)", ["uv", "run", "deptry", "src/"]),
    ]

    results = []
    for name, cmd in checks:
        success = run_check(name, cmd)
        results.append((name, success))

    # Summary
    print(f'\n{"="*60}')
    print("SUMMARY")
    print(f'{"="*60}')

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for name, success in results:
        status = "✅" if success else "❌"
        print(f"{status} {name}")

    print(f"\nPassed: {passed}/{total}")

    if passed < total:
        print("\n❌ Quality checks FAILED")
        sys.exit(1)

    print("\n✅ All quality checks PASSED")


if __name__ == "__main__":
    main()
