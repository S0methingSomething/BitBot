#!/usr/bin/env python3
"""AST-based validation coverage analyzer."""

import ast
from pathlib import Path


def analyze_file(filepath: Path) -> list[dict]:
    """Parse file and extract function validation status."""
    with open(filepath) as f:
        tree = ast.parse(f.read(), filename=str(filepath))
    
    functions = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef):
            continue
        if node.name.startswith('_'):  # Skip private
            continue
        
        # AST analysis of decorators
        has_deal = any('deal' in ast.unparse(d) for d in node.decorator_list)
        has_beartype = any('beartype' in ast.unparse(d) for d in node.decorator_list)
        
        # Extract signature
        args = [arg.arg for arg in node.args.args]
        returns = ast.unparse(node.returns) if node.returns else 'None'
        
        functions.append({
            'name': node.name,
            'args': args,
            'returns': returns,
            'deal': has_deal,
            'beartype': has_beartype,
            'validated': has_deal or has_beartype,
            'lineno': node.lineno,
        })
    
    return functions


def main() -> None:
    """Run AST-based validation analysis."""
    src_dir = Path('src')
    all_functions = {}
    
    for filepath in sorted(src_dir.glob('*.py')):
        if filepath.name == '__init__.py':
            continue
        funcs = analyze_file(filepath)
        if funcs:
            all_functions[filepath.name] = funcs
    
    # Report
    print('=== AST-BASED VALIDATION COVERAGE ===\n')
    
    total = validated = deal_count = beartype_count = 0
    
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
            if func['validated']:
                validated += 1
            
            dec_str = f" ({', '.join(decorators)})" if decorators else ''
            sig = f"{func['name']}({', '.join(func['args'])}) -> {func['returns']}"
            print(f'  {status} {sig}{dec_str}')
        print()
    
    print('=== SUMMARY ===')
    print(f'Total: {total} | Validated: {validated} | Coverage: {validated/total*100:.1f}%')
    print(f'@deal: {deal_count} | @beartype: {beartype_count} | Missing: {total - validated}')


if __name__ == '__main__':
    main()
