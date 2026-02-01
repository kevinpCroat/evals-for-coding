#!/usr/bin/env python3
import ast
import re
import sys
from pathlib import Path
from typing import List, Dict


def extract_docstring(node):
    """Extract docstring from an AST node."""
    return ast.get_docstring(node)


def extract_code_examples(docstring):
    """Extract code examples from a docstring.

    Looks for code blocks in various formats:
    - Example: or Examples: sections
    - >>> interactive examples
    - ```python code blocks
    """
    if not docstring:
        return []

    examples = []

    # Pattern 1: Example: or Examples: sections with indented code
    example_pattern = r'(?:Example|Examples):\s*\n((?:[ \t]+.+\n)+)'
    for match in re.finditer(example_pattern, docstring, re.MULTILINE):
        code_block = match.group(1)
        # Remove common indentation
        lines = code_block.split('\n')
        min_indent = min(len(line) - len(line.lstrip())
                        for line in lines if line.strip())
        dedented = '\n'.join(line[min_indent:] for line in lines)
        examples.append(dedented.strip())

    # Pattern 2: >>> interactive examples
    doctest_pattern = r'((?:>>>.*\n(?:\.\.\..*\n)*)+)'
    for match in re.finditer(doctest_pattern, docstring):
        doctest_code = match.group(1)
        # Convert doctest format to regular Python
        code_lines = []
        for line in doctest_code.split('\n'):
            if line.strip().startswith('>>>'):
                code_lines.append(line.strip()[4:])
            elif line.strip().startswith('...'):
                code_lines.append(line.strip()[4:])
        if code_lines:
            examples.append('\n'.join(code_lines))

    # Pattern 3: ```python code blocks
    code_block_pattern = r'```(?:python)?\s*\n(.*?)\n```'
    for match in re.finditer(code_block_pattern, docstring, re.DOTALL):
        examples.append(match.group(1).strip())

    return examples


def extract_all_examples(filepath):
    """Extract all code examples from all docstrings in a file."""
    with open(filepath, 'r') as f:
        content = f.read()
        tree = ast.parse(content)

    all_examples = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
            docstring = extract_docstring(node)
            if docstring:
                examples = extract_code_examples(docstring)
                for example in examples:
                    all_examples.append({
                        'location': f"{node.name}",
                        'code': example
                    })

    return all_examples


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: extract_examples.py <filepath>", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]
    if not Path(filepath).exists():
        print(f"Error: File {filepath} not found", file=sys.stderr)
        sys.exit(1)

    examples = extract_all_examples(filepath)

    import json
    print(json.dumps(examples, indent=2))
