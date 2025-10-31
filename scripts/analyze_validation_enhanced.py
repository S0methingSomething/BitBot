#!/usr/bin/env python3
"""Enhanced AST-based validation analyzer with Pydantic model detection."""

import ast
from pathlib import Path
from typing import Any


def get_pydantic_models(filepath: Path) -> set[str]:
    """Extract Pydantic model class names from a file."""
    with open(filepath) as f:
        tree = ast.parse(f.read(), filename=str(filepath))
    
    models = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            # Check if class inherits from BaseModel
            for base in node.bases:
                if isinstance(base, ast.Name) and base.id == "BaseModel":
                    models.add(node.name)
    return models


def analyze_function(node: ast.FunctionDef, pydantic_models: set[str]) -> dict[str, Any]:
    """Analyze a function for validation decorators and Pydantic usage."""
    # Check decorators
    has_deal = any('deal' in ast.unparse(d) for d in node.decorator_list)
    has_beartype = any('beartype' in ast.unparse(d) for d in node.decorator_list)
    
    # Check for Pydantic model arguments
    uses_pydantic = False
    pydantic_args = []
    
    for arg in node.args.args:
        if arg.annotation:
            annotation_str = ast.unparse(arg.annotation)
            # Check if annotation matches any Pydantic model
            for model in pydantic_models:
                if model in annotation_str:
                    uses_pydantic = True
                    pydantic_args.append(f"{arg.arg}: {annotation_str}")
    
    # Extract signature
    args = [arg.arg for arg in node.args.args]
    returns = ast.unparse(node.returns) if node.returns else 'None'
    
    return {
        'name': node.name,
        'args': args,
        'returns': returns,
        'deal': has_deal,
        'beartype': has_beartype,
        'validated': has_deal or has_beartype,
        'uses_pydantic': uses_pydantic,
        'pydantic_args': pydantic_args,
        'lineno': node.lineno,
    }


def analyze_file(filepath: Path, all_pydantic_models: set[str]) -> list[dict]:
    """Parse file and extract function validation status."""
    with open(filepath) as f:
        tree = ast.parse(f.read(), filename=str(filepath))
    
    functions = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef):
            continue
        if node.name.startswith('_'):  # Skip private
            continue
        
        func_info = analyze_function(node, all_pydantic_models)
        functions.append(func_info)
    
    return functions


def main() -> None:
    """Run enhanced AST-based validation analysis."""
    src_dir = Path('src')
    
    # First pass: collect all Pydantic models
    print('=== SCANNING FOR PYDANTIC MODELS ===\n')
    all_pydantic_models = set()
    for filepath in src_dir.glob('*.py'):
        models = get_pydantic_models(filepath)
        if models:
            print(f'{filepath.name}: {", ".join(sorted(models))}')
            all_pydantic_models.update(models)
    
    print(f'\nTotal Pydantic models found: {len(all_pydantic_models)}\n')
    
    # Second pass: analyze functions
    print('=== ENHANCED VALIDATION COVERAGE ===\n')
    
    all_functions = {}
    for filepath in sorted(src_dir.glob('*.py')):
        if filepath.name == '__init__.py':
            continue
        funcs = analyze_file(filepath, all_pydantic_models)
        if funcs:
            all_functions[filepath.name] = funcs
    
    # Report
    total = validated = deal_count = beartype_count = pydantic_count = 0
    pydantic_unvalidated = []
    
    for filename, funcs in all_functions.items():
        print(f'{filename}:')
        for func in funcs:
            total += 1
            status = '✅' if func['validated'] else '❌'
            decorators = []
            
            if func['deal']:
                decorators.append('deal')
                deal_count += 1
            if func['beartype']:
                decorators.append('beartype')
                beartype_count += 1
            if func['uses_pydantic']:
                decorators.append('pydantic-args')
                pydantic_count += 1
                if not func['validated']:
                    pydantic_unvalidated.append((filename, func['name'], func['pydantic_args']))
            
            if func['validated']:
                validated += 1
            
            dec_str = f" ({', '.join(decorators)})" if decorators else ''
            sig = f"{func['name']}({', '.join(func['args'])}) -> {func['returns']}"
            print(f'  {status} {sig}{dec_str}')
        print()
    
    print('=== SUMMARY ===')
    print(f'Total: {total} | Validated: {validated} | Coverage: {validated/total*100:.1f}%')
    print(f'@deal: {deal_count} | @beartype: {beartype_count} | Missing: {total - validated}')
    print(f'Functions using Pydantic models: {pydantic_count}')
    
    if pydantic_unvalidated:
        print(f'\n=== UNVALIDATED FUNCTIONS WITH PYDANTIC ARGS ({len(pydantic_unvalidated)}) ===')
        for filename, funcname, args in pydantic_unvalidated:
            print(f'\n❌ {filename}::{funcname}')
            for arg in args:
                print(f'   - {arg}')


if __name__ == '__main__':
    main()
