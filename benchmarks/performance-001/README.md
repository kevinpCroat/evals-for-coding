# Performance Optimization Benchmark (performance-001)

Tests AI's ability to optimize slow code using profiler data to identify and fix performance bottlenecks.

## Overview

This benchmark evaluates an AI's capability to:
1. Analyze profiler output to identify performance bottlenecks
2. Recognize algorithmic inefficiencies (O(n²) vs O(n log n))
3. Apply appropriate data structures for performance
4. Optimize code while preserving correctness

## Task Summary

Optimize a log processing system that finds duplicate user sessions and computes statistics. The code is functionally correct but extremely slow due to:
- O(n²) nested loops for duplicate detection
- Repeated regex parsing (25 million operations)
- Bubble sort instead of efficient sorting
- Inefficient data structures

**Target**: Achieve 10x+ speedup (baseline ~15s → <1.5s) while maintaining all test behavior.

## Files

```
performance-001/
├── README.md                              # This file
├── spec.md                               # Task specification
├── prompts.txt                           # Task prompt for AI
├── starter-code/
│   ├── data_processor.py                 # Slow implementation to optimize
│   ├── test_data_processor.py            # Test suite (must pass)
│   ├── profiler_output.txt               # cProfile output showing bottlenecks
│   ├── benchmark.py                      # Performance measurement script
│   └── generate_profile.py               # Script to regenerate profiler output
└── verification/
    ├── verify.sh                         # Scoring script
    └── data_processor_optimized.py       # Reference optimized solution
```

## Quick Start

1. Review the slow implementation:
   ```bash
   cd starter-code
   cat data_processor.py
   ```

2. Examine profiler output to identify bottlenecks:
   ```bash
   cat profiler_output.txt
   ```

3. Run tests to understand expected behavior:
   ```bash
   pytest test_data_processor.py -v
   ```

4. Measure baseline performance:
   ```bash
   python benchmark.py
   ```

5. Optimize `data_processor.py` to achieve 10x speedup

6. Verify your solution:
   ```bash
   ../verification/verify.sh
   ```

## Scoring

Total: 100 points

- **Performance (50%)**: Speedup achieved
  - 10x+ speedup: 50 points
  - 5-10x speedup: 25-50 points (linear)
  - 2-5x speedup: 10-25 points
  - <2x speedup: 0-10 points

- **Correctness (30%)**: All tests pass
  - All tests pass: 30 points
  - Any test fails: 0 points

- **Optimization Quality (20%)**: Code analysis
  - Used caching/parsing once: 5 points
  - Used appropriate data structures: 4 points
  - Used built-in sort: 4 points
  - Removed nested loops: 4 points
  - Improved algorithms: 3 points
  - Bonus for exceptional speedup (20x+): +5 points

## Key Performance Issues

The profiler reveals:

1. **25M regex operations**: `re.search()` called repeatedly on same data
2. **O(n²) duplicate finding**: Nested loops comparing every entry
3. **O(n²) bubble sort**: Custom sort instead of built-in O(n log n)
4. **No caching**: Same log entries parsed multiple times

## Expected Optimizations

Successful solutions typically:
- Parse logs once and cache results
- Use `defaultdict` for O(1) lookups
- Replace nested loops with hash-based grouping
- Use `sorted()` instead of bubble sort
- Combine operations to reduce passes over data

## Validation

The verification script:
1. Runs all tests - must pass for any points
2. Benchmarks performance with 5,000 log entries
3. Calculates speedup vs baseline
4. Analyzes code for optimization patterns
5. Outputs JSON score with detailed feedback

## Reference Solution

An optimized reference implementation is provided in `verification/data_processor_optimized.py` that achieves 50-100x speedup using:
- Single-pass parsing with caching
- Dictionary-based grouping (O(n) instead of O(n²))
- Built-in sorted() (O(n log n) instead of O(n²))
- Elimination of redundant regex operations

## Design Notes

This benchmark tests "real-world" optimization skills:
- Profiler-guided optimization (not premature optimization)
- Algorithmic thinking (time complexity matters)
- Maintaining correctness under optimization
- Using appropriate data structures

The bottlenecks are intentionally obvious from profiling to make this accessible while still requiring understanding of algorithms and data structures.
