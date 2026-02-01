#!/usr/bin/env python3
import ast
import re
import sys
from pathlib import Path
from typing import List, Dict, Set


def extract_docstring(node):
    """Extract docstring from an AST node."""
    return ast.get_docstring(node)


def extract_function_signature(node):
    """Extract parameter names and types from a function definition."""
    params = []
    for arg in node.args.args:
        param_info = {
            'name': arg.arg,
            'annotation': ast.unparse(arg.annotation) if arg.annotation else None
        }
        params.append(param_info)
    return params


def extract_documented_params(docstring):
    """Extract parameter names from Args section of docstring."""
    if not docstring:
        return set()

    # Look for Args: section
    args_pattern = r'Args:\s*\n((?:[ \t]+\w+.*\n)+)'
    match = re.search(args_pattern, docstring, re.MULTILINE)

    if not match:
        return set()

    args_section = match.group(1)

    # Extract parameter names (format: "param_name: description" or "param_name (type): description")
    param_pattern = r'^\s*(\w+)(?:\s*\([^)]+\))?\s*:'
    params = set()
    for line in args_section.split('\n'):
        match = re.match(param_pattern, line)
        if match:
            params.add(match.group(1))

    return params


def check_return_documented(docstring):
    """Check if Returns section exists in docstring."""
    if not docstring:
        return False
    return bool(re.search(r'Returns:\s*\n', docstring, re.MULTILINE))


def check_raises_documented(docstring):
    """Check if Raises section exists in docstring."""
    if not docstring:
        return False
    return bool(re.search(r'Raises:\s*\n', docstring, re.MULTILINE))


def check_consistency(filepath):
    """Check if docstrings are consistent with actual function signatures."""
    with open(filepath, 'r') as f:
        tree = ast.parse(f.read())

    issues = []
    total_checks = 0
    passed_checks = 0

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name.startswith('_'):  # Skip private methods
                continue

            docstring = extract_docstring(node)
            if not docstring:
                continue

            # Extract actual parameters
            actual_params = extract_function_signature(node)
            actual_param_names = {p['name'] for p in actual_params if p['name'] != 'self'}

            # Extract documented parameters
            documented_params = extract_documented_params(docstring)

            # Check if all actual params are documented
            undocumented = actual_param_names - documented_params
            extra_documented = documented_params - actual_param_names

            total_checks += 1

            if undocumented or extra_documented:
                issues.append({
                    'function': node.name,
                    'type': 'parameter_mismatch',
                    'undocumented_params': list(undocumented),
                    'extra_documented_params': list(extra_documented)
                })
            else:
                passed_checks += 1

            # Check if function has return statement and Returns is documented
            has_return = any(isinstance(n, ast.Return) and n.value is not None
                           for n in ast.walk(node))
            has_return_doc = check_return_documented(docstring)

            total_checks += 1
            if has_return and not has_return_doc:
                issues.append({
                    'function': node.name,
                    'type': 'missing_return_doc',
                    'message': 'Function returns a value but has no Returns section'
                })
            else:
                passed_checks += 1

    consistency_percentage = (passed_checks / total_checks * 100) if total_checks > 0 else 100

    return {
        'total_checks': total_checks,
        'passed_checks': passed_checks,
        'consistency_percentage': consistency_percentage,
        'issues': issues
    }


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: check_consistency.py <filepath>", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]
    if not Path(filepath).exists():
        print(f"Error: File {filepath} not found", file=sys.stderr)
        sys.exit(1)

    result = check_consistency(filepath)

    import json
    print(json.dumps(result, indent=2))
