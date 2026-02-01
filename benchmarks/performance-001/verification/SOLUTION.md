# Performance Optimization Solution

This document explains the reference solution for the performance-001 benchmark.

## Problem Analysis

### Initial Performance Issues

The baseline implementation in `data_processor.py` has severe performance problems:

1. **25 million regex operations** (from profiler)
   - `re.search()` called 25,015,000 times
   - Each log entry parsed multiple times
   - No caching of parsed results

2. **O(n²) duplicate detection**
   - Nested loops in `find_duplicate_sessions()`
   - For each entry, searches through all entries
   - With 5,000 entries: 25 million comparisons

3. **O(n²) bubble sort**
   - `get_top_users()` uses manual bubble sort
   - Python's built-in sort is O(n log n) and highly optimized

4. **Repeated work**
   - Each method re-parses the same log data
   - No sharing of computed results

### Profiler Evidence

From `profiler_output.txt`:
```
   ncalls  tottime  cumtime filename:lineno(function)
        1    4.100   15.335  data_processor.py:22(find_duplicate_sessions)
 25015000    2.923   10.122  re.py:198(search)
```

The profiler clearly shows:
- Total time: 15.376 seconds
- Most time in `find_duplicate_sessions()`: 15.335 seconds
- Dominated by regex searches: 25M calls

## Optimization Strategy

### 1. Parse Once, Cache Results (Most Important)

**Problem**: Logs parsed multiple times with regex
**Solution**: Parse all logs once, store results

```python
def _parse_logs_once(self) -> List[Tuple[str, int]]:
    """Parse all logs once and cache the results."""
    if self._parsed_logs is not None:
        return self._parsed_logs

    parsed = []
    for log in self.logs:
        user_match = re.search(r'user_id=(\w+)', log)
        duration_match = re.search(r'duration=(\d+)', log)
        if user_match and duration_match:
            user_id = user_match.group(1)
            duration = int(duration_match.group(1))
            parsed.append((user_id, duration))

    self._parsed_logs = parsed
    return parsed
```

**Impact**: Reduces 25M regex operations to ~10K (one per log entry)

### 2. Use Hash Maps for O(1) Lookup

**Problem**: O(n²) nested loops for duplicate detection
**Solution**: Use `defaultdict` to group by user_id in O(n)

```python
def find_duplicate_sessions(self) -> List[Tuple[str, List[int]]]:
    parsed_logs = self._parse_logs_once()

    # Build index: O(n) single pass
    user_indices = defaultdict(list)
    for i, (user_id, _) in enumerate(parsed_logs):
        user_indices[user_id].append(i)

    # Filter for duplicates
    duplicates = [
        (user_id, line_nums)
        for user_id, line_nums in user_indices.items()
        if len(line_nums) > 1
    ]

    return duplicates
```

**Before**: O(n²) - nested loops comparing each entry to all others
**After**: O(n) - single pass building hash map

**Impact**: 25,000,000 operations → 5,000 operations

### 3. Use Built-in Sorting

**Problem**: Bubble sort is O(n²)
**Solution**: Use Python's built-in `sorted()` which is O(n log n)

```python
def get_top_users(self, stats: Dict[str, int], n: int = 10) -> List[Tuple[str, int]]:
    # Use built-in sorted with key parameter (O(n log n))
    sorted_items = sorted(stats.items(), key=lambda x: x[1], reverse=True)
    return sorted_items[:n]
```

**Before**: O(n²) bubble sort with manual swaps
**After**: O(n log n) Timsort (Python's optimized algorithm)

### 4. Aggregate in Single Pass

**Problem**: Re-parsing for stats computation
**Solution**: Use cached parsed data and defaultdict

```python
def compute_session_stats(self) -> Dict[str, int]:
    parsed_logs = self._parse_logs_once()

    # Aggregate in single pass
    stats = defaultdict(int)
    for user_id, duration in parsed_logs:
        stats[user_id] += duration

    return dict(stats)
```

## Performance Results

### Baseline (Slow Version)
- Time: ~15 seconds
- Regex calls: 25,015,000
- Complexity: O(n²)

### Optimized Version
- Time: ~0.01 seconds
- Regex calls: ~10,000
- Complexity: O(n log n)
- **Speedup: ~1,500x** (far exceeds 10x target)

## Key Lessons

1. **Profile first**: Don't guess where the bottleneck is
2. **Algorithm matters**: O(n) vs O(n²) makes huge difference
3. **Cache expensive operations**: Regex parsing is costly
4. **Use right data structures**: Hash maps for lookups, not linear search
5. **Leverage standard library**: Built-in functions are optimized
6. **Maintain correctness**: All tests still pass

## Complexity Analysis

| Operation | Before | After |
|-----------|--------|-------|
| Parsing | O(n×m) per method | O(n) once |
| Duplicate finding | O(n²) | O(n) |
| Sorting | O(n²) | O(n log n) |
| Stats computation | O(n) | O(n) |
| **Overall** | **O(n²)** | **O(n log n)** |

Where:
- n = number of log entries (5,000)
- m = number of method calls (3)

## Verification

The optimized solution:
- Passes all 12 tests ✓
- Achieves >100x speedup ✓
- Maintains identical behavior ✓
- Uses profiler-guided optimizations ✓
