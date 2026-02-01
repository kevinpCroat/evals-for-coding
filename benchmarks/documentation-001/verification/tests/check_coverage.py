#!/usr/bin/env python3
import ast
import sys
from pathlib import Path


def has_docstring(node):
    """Check if an AST node has a docstring."""
    return (ast.get_docstring(node) is not None and
            len(ast.get_docstring(node).strip()) > 0)


def is_public(name):
    """Check if a name is public (doesn't start with underscore)."""
    return not name.startswith('_')


def count_documented_apis(filepath):
    """Count how many public APIs are documented vs total public APIs."""
    with open(filepath, 'r') as f:
        tree = ast.parse(f.read())

    total_apis = 0
    documented_apis = 0
    details = {
        'classes': {'total': 0, 'documented': 0, 'missing': []},
        'methods': {'total': 0, 'documented': 0, 'missing': []},
        'functions': {'total': 0, 'documented': 0, 'missing': []}
    }

    for node in ast.walk(tree):
        # Check classes
        if isinstance(node, ast.ClassDef) and is_public(node.name):
            total_apis += 1
            details['classes']['total'] += 1
            if has_docstring(node):
                documented_apis += 1
                details['classes']['documented'] += 1
            else:
                details['classes']['missing'].append(node.name)

            # Check methods within the class
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and is_public(item.name):
                    total_apis += 1
                    details['methods']['total'] += 1
                    method_name = f"{node.name}.{item.name}"
                    if has_docstring(item):
                        documented_apis += 1
                        details['methods']['documented'] += 1
                    else:
                        details['methods']['missing'].append(method_name)

        # Check module-level functions
        elif isinstance(node, ast.FunctionDef) and is_public(node.name):
            # Only count if it's a module-level function
            if any(isinstance(parent, ast.Module) for parent in ast.walk(tree)):
                total_apis += 1
                details['functions']['total'] += 1
                if has_docstring(node):
                    documented_apis += 1
                    details['functions']['documented'] += 1
                else:
                    details['functions']['missing'].append(node.name)

    coverage_percentage = (documented_apis / total_apis * 100) if total_apis > 0 else 0

    return {
        'total_apis': total_apis,
        'documented_apis': documented_apis,
        'coverage_percentage': coverage_percentage,
        'details': details
    }


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: check_coverage.py <filepath>", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]
    if not Path(filepath).exists():
        print(f"Error: File {filepath} not found", file=sys.stderr)
        sys.exit(1)

    result = count_documented_apis(filepath)

    import json
    print(json.dumps(result, indent=2))
