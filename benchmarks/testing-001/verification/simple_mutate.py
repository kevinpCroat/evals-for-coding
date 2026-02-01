#!/usr/bin/env python3
"""
Simple mutation testing script for shopping_cart.py
This creates basic mutations and runs tests to see if they're caught.
"""

import sys
import subprocess
import re
import tempfile
import shutil
from pathlib import Path


def create_mutations(source_file):
    """Create simple mutations of the source code."""
    with open(source_file, 'r') as f:
        original_code = f.read()

    mutations = []

    # Mutation 1: Change < to <=
    for match in re.finditer(r'(\s+)(if .* < )', original_code):
        mutated = original_code.replace(match.group(0), match.group(1) + match.group(2).replace(' < ', ' <= '), 1)
        mutations.append(("< to <=", mutated))

    # Mutation 2: Change <= to <
    for match in re.finditer(r'(\s+)(if .* <= )', original_code):
        mutated = original_code.replace(match.group(0), match.group(1) + match.group(2).replace(' <= ', ' < '), 1)
        mutations.append(("<= to <", mutated))

    # Mutation 3: Change > to >=
    for match in re.finditer(r'(\s+)(if .* > )', original_code):
        mutated = original_code.replace(match.group(0), match.group(1) + match.group(2).replace(' > ', ' >= '), 1)
        mutations.append(("> to >=", mutated))

    # Mutation 4: Change + to -
    for match in re.finditer(r'(total_discount \+= )', original_code):
        mutated = original_code.replace(match.group(0), match.group(0).replace('+=', '-='), 1)
        mutations.append(("'+=' to '-='", mutated))

    # Mutation 5: Change * to /
    for match in re.finditer(r'(self\.price \* self\.quantity)', original_code):
        mutated = original_code.replace(match.group(0), match.group(0).replace('*', '/'), 1)
        mutations.append(("'*' to '/'", mutated))

    # Mutation 6: Change - to +
    for match in re.finditer(r'(subtotal - discount)', original_code):
        mutated = original_code.replace(match.group(0), match.group(0).replace('-', '+'), 1)
        mutations.append(("'-' to '+'", mutated))

    # Mutation 7: Change return values
    for match in re.finditer(r'return (True|False)', original_code):
        value = match.group(1)
        opposite = 'False' if value == 'True' else 'True'
        mutated = original_code.replace(match.group(0), f'return {opposite}', 1)
        mutations.append((f"return {value} to {opposite}", mutated))

    # Mutation 8: Change 0 to 1
    for match in re.finditer(r'(self\.loyalty_points = )0', original_code):
        mutated = original_code.replace(match.group(0), match.group(1) + '1', 1)
        mutations.append(("'= 0' to '= 1'", mutated))

    # Mutation 9: Change min to max
    for match in re.finditer(r'min\(total_discount, subtotal\)', original_code):
        mutated = original_code.replace(match.group(0), match.group(0).replace('min', 'max'), 1)
        mutations.append(("'min' to 'max'", mutated))

    # Mutation 10: Change sum to len
    for match in re.finditer(r'sum\(item\.quantity for item in self\.items\.values\(\)\)', original_code):
        mutated = original_code.replace(match.group(0), match.group(0).replace('sum', 'len'), 1)
        mutations.append(("'sum' to 'len'", mutated))

    return mutations[:50]  # Limit to first 50 mutations


def run_tests(source_file_path):
    """Run the test suite."""
    result = subprocess.run(
        ['python3', '-m', 'pytest', 'test_shopping_cart.py', '-x', '-q'],
        cwd=source_file_path.parent,
        capture_output=True,
        timeout=30
    )
    return result.returncode == 0


def main():
    source_file = Path('shopping_cart.py')
    if not source_file.exists():
        print("Error: shopping_cart.py not found")
        sys.exit(1)

    # Create backup
    backup_file = Path('shopping_cart.py.bak')
    shutil.copy(source_file, backup_file)

    try:
        mutations = create_mutations(source_file)
        print(f"Generated {len(mutations)} mutations", file=sys.stderr)

        killed = 0
        survived = 0

        for i, (mutation_type, mutated_code) in enumerate(mutations):
            # Write mutated code
            with open(source_file, 'w') as f:
                f.write(mutated_code)

            # Run tests
            try:
                tests_pass = run_tests(source_file)
                if not tests_pass:
                    killed += 1
                else:
                    survived += 1
                    print(f"Mutation {i+1} survived: {mutation_type}", file=sys.stderr)
            except Exception as e:
                # Treat errors as killed
                killed += 1

            # Restore original
            shutil.copy(backup_file, source_file)

        total = killed + survived
        if total > 0:
            percent = (killed / total) * 100
            print(f"\nMutation Testing Results:", file=sys.stderr)
            print(f"Killed: {killed}/{total} ({percent:.1f}%)", file=sys.stderr)
            print(f"Survived: {survived}/{total}", file=sys.stderr)

        # Output in format for script to parse
        print(f"{killed},{survived},0,0")

    finally:
        # Restore original file
        if backup_file.exists():
            shutil.copy(backup_file, source_file)
            backup_file.unlink()


if __name__ == '__main__':
    main()
