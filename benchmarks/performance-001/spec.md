# Performance Optimization Benchmark: Log Processor

## Objective

Optimize a slow log processing system using profiler data to identify and fix performance bottlenecks. This benchmark tests your ability to analyze profiling output, identify algorithmic inefficiencies, and implement effective optimizations while maintaining correctness.

## Background

The `LogProcessor` class in `starter-code/data_processor.py` processes log files to find duplicate user sessions and compute session statistics. While the code is functionally correct, it has severe performance problems that make it unusable with large datasets.

Profiler output in `profiler_output.txt` shows the performance bottlenecks.

## Requirements

### Performance Requirements
1. Achieve at least **10x speedup** from baseline performance
2. Baseline (slow version) runs in ~15 seconds with 5,000 log entries
3. Target: Complete processing in under 1.5 seconds

### Functional Requirements
1. **All existing tests must continue to pass** - behavior must be preserved
2. Maintain the same API (class and method signatures)
3. Results must be identical to the original implementation
4. Handle edge cases correctly (empty logs, single entries, etc.)

### Optimization Requirements
1. **Use profiler data** to identify bottlenecks
2. Address **algorithmic inefficiencies** (not just micro-optimizations)
3. Improve **time complexity** of slow operations
4. Use appropriate **data structures** for better performance

## Getting Started

1. Review the current implementation in `starter-code/data_processor.py`
2. Examine `profiler_output.txt` to understand where time is spent
3. Run the tests to understand expected behavior:
   ```bash
   pytest test_data_processor.py -v
   ```
4. Run the benchmark to measure baseline performance:
   ```bash
   python benchmark.py
   ```
5. Optimize `data_processor.py` to meet performance targets
6. Verify tests still pass and measure new performance

## Performance Bottlenecks

The profiler reveals several issues:

1. **Excessive regex operations**: ~25 million regex searches
2. **O(n²) nested loops**: Linear search for each log entry
3. **Inefficient sorting**: Bubble sort instead of optimal algorithm
4. **Repeated parsing**: Same log entries parsed multiple times

Your task is to fix these issues systematically.

## Success Criteria

Your optimization will be considered successful when:

1. **Performance (50%)**: Achieve 10x+ speedup (baseline ~15s → target <1.5s)
2. **Correctness (30%)**: All tests pass with identical results
3. **Optimization Quality (20%)**: Used profiling data, addressed root causes with proper algorithms/data structures

## Deliverables

Optimized version of `starter-code/data_processor.py` that:
- Passes all tests in `test_data_processor.py`
- Meets or exceeds the 10x performance target
- Uses better algorithms and data structures

## Optimization Hints

Consider these approaches:

1. **Parse once, use many times**: Cache parsed data instead of re-parsing
2. **Use appropriate data structures**: Dictionaries for O(1) lookup instead of O(n) search
3. **Improve time complexity**: O(n log n) sorting instead of O(n²) bubble sort
4. **Reduce redundant work**: Combine operations, eliminate duplicate processing
5. **Leverage standard library**: Built-in functions are often optimized

## Important Notes

- Focus on **algorithmic improvements**, not micro-optimizations
- Use the **profiler output** to guide your optimization efforts
- **Don't break functionality** - all tests must pass
- Document significant changes if creating an explanation file

## Evaluation

Run `./verification/verify.sh` to check your solution. The script will:
- Run the test suite to verify correctness
- Benchmark performance and calculate speedup
- Verify profiling was used appropriately
- Output a JSON score with detailed feedback

Scoring breakdown:
- **Performance Improvement (50%)**: Based on actual speedup achieved
- **Tests Passing (30%)**: All tests must pass for full credit
- **Optimization Approach (20%)**: Quality of algorithmic improvements
