#!/usr/bin/env python3
"""
Simple code duplication detector.
Measures duplicated code by finding similar code blocks.
Returns a score from 0-100 where higher means more duplication.
"""

import sys
import re
from collections import defaultdict


def normalize_line(line):
    """Normalize a line by removing whitespace and comments."""
    # Remove inline comments
    line = re.sub(r'#.*$', '', line)
    # Remove all whitespace
    line = re.sub(r'\s+', '', line)
    return line


def extract_code_blocks(filename, min_lines=3):
    """
    Extract all code blocks of minimum length.
    Returns list of normalized code blocks.
    """
    with open(filename, 'r') as f:
        lines = f.readlines()

    # Normalize all lines
    normalized = []
    for line in lines:
        norm = normalize_line(line)
        if norm:  # Skip empty lines
            normalized.append(norm)

    # Extract all blocks of min_lines length
    blocks = []
    for i in range(len(normalized) - min_lines + 1):
        block = tuple(normalized[i:i + min_lines])
        blocks.append(block)

    return blocks


def find_duplicates(blocks):
    """
    Find duplicated blocks.
    Returns count of duplicate block instances.
    """
    block_counts = defaultdict(int)

    for block in blocks:
        block_counts[block] += 1

    # Count how many blocks appear more than once
    duplicates = sum(count - 1 for count in block_counts.values() if count > 1)

    return duplicates


def measure_duplication(filename):
    """
    Measure code duplication in a file.
    Returns a score from 0-100 where higher means more duplication.
    """
    try:
        # Extract blocks of 3, 4, and 5 lines
        blocks_3 = extract_code_blocks(filename, min_lines=3)
        blocks_4 = extract_code_blocks(filename, min_lines=4)
        blocks_5 = extract_code_blocks(filename, min_lines=5)

        # Find duplicates
        dup_3 = find_duplicates(blocks_3)
        dup_4 = find_duplicates(blocks_4)
        dup_5 = find_duplicates(blocks_5)

        # Weight longer blocks more heavily
        total_dup = dup_3 + (dup_4 * 2) + (dup_5 * 3)
        total_blocks = len(blocks_3)

        if total_blocks == 0:
            return 0

        # Calculate percentage (capped at 100)
        duplication_percent = min(100, (total_dup / total_blocks) * 100)

        return round(duplication_percent, 2)

    except Exception as e:
        print(f"Error measuring duplication: {e}", file=sys.stderr)
        return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: measure_duplication.py <filename>", file=sys.stderr)
        sys.exit(1)

    filename = sys.argv[1]
    score = measure_duplication(filename)
    print(score)
