#!/usr/bin/env python3
import ast
import re
import sys
from pathlib import Path


def extract_docstring(node):
    """Extract docstring from an AST node."""
    return ast.get_docstring(node)


def is_public(name):
    """Check if a name is public."""
    return not name.startswith('_')


def check_google_style(docstring):
    """Check if docstring follows Google style format.

    Returns:
        dict with 'score' (0-100) and 'issues' (list of strings)
    """
    if not docstring:
        return {'score': 0, 'issues': ['No docstring']}

    score = 100
    issues = []

    # Check for summary line (first line should be brief, one-line)
    lines = docstring.split('\n')
    first_line = lines[0].strip()

    if not first_line:
        score -= 20
        issues.append('Missing summary line')
    elif len(first_line) > 120:
        score -= 10
        issues.append('Summary line too long (>120 chars)')

    # Check for proper sections with correct format
    sections = ['Args:', 'Returns:', 'Raises:', 'Example:', 'Examples:', 'Attributes:']
    found_sections = []

    for section in sections:
        if section in docstring:
            found_sections.append(section)

    # Check section formatting (should be "Section:\n" followed by indented content)
    for section in found_sections:
        section_pattern = f'{re.escape(section)}\\s*\\n((?:[ \\t]+.+\\n)*)'
        if not re.search(section_pattern, docstring, re.MULTILINE):
            score -= 5
            issues.append(f'{section} section not properly formatted')

    # Bonus points for having examples
    if 'Example:' in docstring or 'Examples:' in docstring:
        score = min(100, score + 10)

    return {'score': max(0, score), 'issues': issues}


def analyze_format_quality(filepath):
    """Analyze overall documentation format quality."""
    with open(filepath, 'r') as f:
        tree = ast.parse(f.read())

    total_docstrings = 0
    total_score = 0
    all_issues = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
            if is_public(node.name):
                docstring = extract_docstring(node)
                if docstring:
                    total_docstrings += 1
                    result = check_google_style(docstring)
                    total_score += result['score']
                    if result['issues']:
                        all_issues.append({
                            'location': node.name,
                            'issues': result['issues']
                        })

    average_score = (total_score / total_docstrings) if total_docstrings > 0 else 0

    return {
        'total_docstrings': total_docstrings,
        'average_format_score': average_score,
        'issues': all_issues
    }


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: check_format.py <filepath>", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]
    if not Path(filepath).exists():
        print(f"Error: File {filepath} not found", file=sys.stderr)
        sys.exit(1)

    result = analyze_format_quality(filepath)

    import json
    print(json.dumps(result, indent=2))
