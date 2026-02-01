# Rewriting-001: Recursive to Iterative Tree Traversal

## Overview

This benchmark evaluates an AI's ability to rewrite recursive algorithms as iterative implementations while preserving exact behavior and maintaining performance. The task focuses on binary tree traversal and analysis operations.

## Challenge

Transform 6 recursive tree operation functions into iterative implementations using explicit stack data structures:

1. **inorder_traversal** - In-order tree traversal (left, root, right)
2. **postorder_traversal** - Post-order tree traversal (left, right, root)
3. **max_depth** - Calculate maximum tree depth
4. **find_path_sum** - Find if a root-to-leaf path with target sum exists
5. **collect_leaves** - Collect all leaf node values in order
6. **tree_map** - Apply a function to all node values, creating a new tree

## Key Requirements

- Must preserve exact behavior (all 39 tests pass)
- Must use explicit stacks (lists/deques) instead of recursion
- Cannot modify function signatures or TreeNode class
- Performance must remain within 120% of recursive baseline
- Must handle deep trees (100+ levels) without stack overflow

## Structure

```
rewriting-001/
├── README.md           # This file
├── spec.md            # Detailed specification
├── prompts.txt        # Task prompts for AI
├── starter-code/
│   ├── tree_traversal.py      # Functions to rewrite (recursive)
│   └── test_tree_traversal.py # Comprehensive test suite (39 tests)
└── verification/
    └── verify.sh      # Automated scoring script
```

## Test Coverage

The test suite includes:

- **Normal cases** (24 tests): Balanced trees, skewed trees, various structures
- **Edge cases** (15 tests): Empty trees, single nodes, deep recursion, special values
- **Performance tests**: 100-iteration runs on balanced and deep trees

### Edge Case Tests

Explicitly defined edge cases for scoring:

1. **Deep recursion inorder** (10 points): 100-level deep tree traversal
2. **Deep recursion max_depth** (5 points): 100-level depth calculation
3. **Path sum with zero** (5 points): Handling zero values in path sums
4. **Large tree leaves** (extra): Complete binary tree of depth 5
5. **Tree map identity** (extra): Identity function transformation

## Scoring

Total: 100 points

### Components

1. **Tests Passing (60%)**: Percentage of tests that pass
   - 100%: All 39 tests pass = 60 points
   - Proportional scoring down to 50% pass rate
   - Below 50%: 0 points

2. **Performance (20%)**: Execution time vs recursive baseline
   - Within 110%: 20 points
   - Within 120%: 15 points
   - Within 150%: 10 points
   - Slower than 150%: 0 points

3. **Edge Cases (20%)**: Specific edge case handling
   - Deep recursion inorder: 10 points
   - Deep recursion max_depth: 5 points
   - Path sum with zero: 5 points

**Passing score**: 70/100

## Running the Benchmark

### Run Tests
```bash
cd starter-code
pytest test_tree_traversal.py -v
```

### Run Verification
```bash
./verification/verify.sh
```

The verification script outputs JSON with detailed scoring:
```json
{
  "benchmark": "rewriting-001",
  "components": {
    "tests_passing": {"score": 100, "weight": 0.6},
    "performance": {"score": 100, "weight": 0.2},
    "edge_cases": {"score": 100, "weight": 0.2}
  },
  "final_score": 100,
  "passed": true
}
```

## Example Solution Approach

For iterative traversal:
1. Use a list or deque as an explicit stack
2. Push nodes onto stack in appropriate order
3. Process nodes as you pop from stack
4. Track state (visited/unvisited) as needed

For tree_map:
- Use two parallel stacks: one for original tree, one for new tree
- Build new tree nodes as you traverse

## Learning Outcomes

This benchmark tests:
- Understanding of recursion vs iteration tradeoffs
- Stack-based algorithm design
- Preserving algorithmic behavior during transformation
- Performance optimization
- Edge case handling (deep recursion, special values)

## Realistic Context

This pattern of rewriting recursive code to iterative is common when:
- Dealing with deep data structures that may exceed recursion limits
- Needing explicit control over execution (pause/resume)
- Optimizing for languages/environments with expensive function calls
- Converting functional code to imperative styles
