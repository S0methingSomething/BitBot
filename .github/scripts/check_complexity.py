#!/usr/bin/env python3
"""Cyclomatic complexity checker for CI - fails if functions exceed threshold."""

import ast
import sys
from pathlib import Path


def calculate_complexity(node: ast.AST) -> int:
    """Calculate cyclomatic complexity of a function."""
    complexity = 1
    for child in ast.walk(node):
        if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
            complexity += 1
        elif isinstance(child, ast.BoolOp):
            complexity += len(child.values) - 1
    return complexity


def analyze_file(filepath: Path, max_complexity: int) -> list[tuple[str, int]]:
    """Return list of (function_name, complexity) exceeding threshold."""
    with open(filepath) as f:
        tree = ast.parse(f.read(), filename=str(filepath))
    
    violations = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            complexity = calculate_complexity(node)
            if complexity > max_complexity:
                violations.append((f"{filepath.relative_to('src')}::{node.name}", complexity))
    
    return violations


def main() -> None:
    """Check complexity doesn't exceed threshold."""
    max_complexity = int(sys.argv[1]) if len(sys.argv) > 1 else 15
    
    src_dir = Path('src')
    all_violations = []
    
    for filepath in src_dir.rglob('*.py'):
        violations = analyze_file(filepath, max_complexity)
        all_violations.extend(violations)
    
    if all_violations:
        print(f'❌ FAILED: {len(all_violations)} functions exceed complexity {max_complexity}')
        for func, complexity in sorted(all_violations, key=lambda x: x[1], reverse=True):
            print(f'  {func}: {complexity}')
        sys.exit(1)
    
    print(f'✅ PASSED: All functions below complexity threshold {max_complexity}')


if __name__ == '__main__':
    main()
