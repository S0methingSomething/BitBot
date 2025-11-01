#!/usr/bin/env python3
"""Generate comprehensive validation coverage report."""

import ast
from collections import defaultdict
from pathlib import Path


def get_pydantic_models(tree: ast.AST) -> set[str]:
    """Extract Pydantic model names."""
    models = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            if any(isinstance(b, ast.Name) and b.id == "BaseModel" for b in node.bases):
                models.add(node.name)
    return models


def analyze_function(node: ast.FunctionDef, pydantic_models: set[str]) -> dict:
    """Analyze function validation and Pydantic usage."""
    has_deal = any("deal" in ast.unparse(d) for d in node.decorator_list)
    has_beartype = any("beartype" in ast.unparse(d) for d in node.decorator_list)

    uses_pydantic = any(
        arg.annotation and any(m in ast.unparse(arg.annotation) for m in pydantic_models)
        for arg in node.args.args
    )

    return {
        "name": node.name,
        "line": node.lineno,
        "deal": has_deal,
        "beartype": has_beartype,
        "validated": has_deal or has_beartype,
        "uses_pydantic": uses_pydantic,
    }


def main() -> None:
    """Generate validation report."""
    src_dir = Path("src")

    # Collect all Pydantic models
    all_models = set()
    for filepath in src_dir.rglob("*.py"):
        with open(filepath) as f:
            tree = ast.parse(f.read())
            all_models.update(get_pydantic_models(tree))

    # Analyze files
    stats = defaultdict(
        lambda: {"total": 0, "validated": 0, "deal": 0, "beartype": 0, "pydantic": 0}
    )

    for filepath in sorted(src_dir.rglob("*.py")):
        if filepath.name == "__init__.py":
            continue

        with open(filepath) as f:
            tree = ast.parse(f.read())

        rel_path = filepath.relative_to(src_dir)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
                info = analyze_function(node, all_models)
                stats[str(rel_path)]["total"] += 1
                if info["validated"]:
                    stats[str(rel_path)]["validated"] += 1
                if info["deal"]:
                    stats[str(rel_path)]["deal"] += 1
                if info["beartype"]:
                    stats[str(rel_path)]["beartype"] += 1
                if info["uses_pydantic"]:
                    stats[str(rel_path)]["pydantic"] += 1

    # Report
    print("=== VALIDATION COVERAGE REPORT ===\n")
    print(f"Pydantic Models: {len(all_models)}\n")

    total_funcs = total_validated = total_deal = total_beartype = total_pydantic = 0

    for filepath in sorted(stats.keys()):
        s = stats[filepath]
        coverage = (s["validated"] / s["total"] * 100) if s["total"] > 0 else 0
        status = "✅" if coverage == 100 else "⚠️" if coverage >= 80 else "❌"

        print(f"{status} {filepath}")
        print(f'   Coverage: {s["validated"]}/{s["total"]} ({coverage:.0f}%)')
        print(f'   @deal: {s["deal"]} | @beartype: {s["beartype"]} | Pydantic: {s["pydantic"]}')

        total_funcs += s["total"]
        total_validated += s["validated"]
        total_deal += s["deal"]
        total_beartype += s["beartype"]
        total_pydantic += s["pydantic"]

    overall = (total_validated / total_funcs * 100) if total_funcs > 0 else 0

    print("\n=== OVERALL ===")
    print(f"Coverage: {total_validated}/{total_funcs} ({overall:.1f}%)")
    print(f"@deal: {total_deal} | @beartype: {total_beartype}")
    print(f"Functions with Pydantic args: {total_pydantic}")


if __name__ == "__main__":
    main()
