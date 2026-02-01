# Concurrency-001: Thread Safety and Race Condition Fixes

## Overview

This benchmark tests an AI's ability to identify and fix race conditions in concurrent Python code. The challenge involves making thread-unsafe code reliable by adding proper synchronization primitives.

## The Challenge

The provided code contains three modules with realistic concurrency bugs:

1. **cache.py** - In-memory cache with check-then-act bugs, non-atomic statistics, and unsafe eviction
2. **counter.py** - Metrics counter with lost updates, inconsistent state, and classic read-modify-write races
3. **worker_pool.py** - Worker pool with unsafe queue operations and non-atomic state transitions

These bugs cause intermittent test failures that only appear under concurrent load, making them challenging to debug but critical to fix.

## Structure

```
concurrency-001/
├── starter-code/           # Buggy code to fix
│   ├── cache.py           # Cache with race conditions
│   ├── counter.py         # Counter with race conditions
│   ├── worker_pool.py     # Worker pool with race conditions
│   └── test_concurrency.py # Tests that expose the bugs
├── verification/
│   └── verify.sh          # Automated scoring script
├── spec.md                # Detailed specification
├── prompts.txt            # Example prompts
└── README.md              # This file
```

## Key Race Conditions

### Cache Module
- Check-then-act pattern in `get()` method
- Non-atomic dictionary updates and evictions
- Race conditions in hit/miss statistics tracking
- Concurrent modification during size checks

### Counter Module
- Non-atomic increment operations (`+=` is not atomic!)
- Lost updates when multiple threads increment simultaneously
- Inconsistent state between related counters
- Classic read-modify-write race conditions

### Worker Pool Module
- Unsafe task queue operations (should use `queue.Queue`)
- Non-atomic state transitions for workers
- Concurrent access to shared results list
- Inconsistent statistics updates

## Testing

The test suite in `test_concurrency.py` exposes the race conditions by:
- Running operations from many threads simultaneously
- Performing thousands of concurrent operations
- Verifying that counts and statistics are correct
- Checking for consistency between related variables

With the buggy starter code, tests fail intermittently. A correct solution passes 100 consecutive runs.

## Verification

Run the verification script to score a solution:

```bash
cd starter-code
../verification/verify.sh
```

Or verify a specific submission directory:

```bash
./verification/verify.sh /path/to/submission
```

### Scoring Breakdown

- **Race Condition Tests (40%)** - Tests must pass 100/100 consecutive runs
- **Deadlock Freedom (30%)** - No deadlocks or infinite waits
- **Synchronization Correctness (20%)** - Proper use of locks and thread-safe primitives
- **Performance (10%)** - Reasonable execution time (no over-locking)

## Expected Solution Approach

A correct solution should:

1. Add `threading.Lock()` to protect critical sections in cache and counter
2. Use `queue.Queue` for thread-safe task queue in worker pool
3. Make all related updates atomic (happen together under the same lock)
4. Eliminate check-then-act patterns
5. Use `with lock:` context managers for clean, safe code

## Common Pitfalls

- Insufficient locking (protecting only part of a critical section)
- Over-locking (holding locks too long, reducing concurrency)
- Check-then-act bugs (checking condition without holding lock)
- Non-atomic operations on related state
- Forgetting that `+=` is not atomic in Python

## Example Fix

Before (buggy):
```python
if key in self.cache:
    self.hits += 1
    return self.cache[key]
```

After (fixed):
```python
with self.lock:
    if key in self.cache:
        self.hits += 1
        return self.cache[key]
```

## Requirements

- Python 3.7+
- Standard library only (threading, queue)
- Tests must pass consistently (100/100 runs)
- No deadlocks
- Reasonable performance (< 60s for 100 test runs)

## Difficulty

**Medium-Hard** - Requires understanding of:
- Race conditions and concurrent programming concepts
- Python's threading primitives (Lock, Queue)
- Check-then-act anti-patterns
- Atomic operations and critical sections
- Proper lock granularity

## Learning Outcomes

This benchmark helps evaluate:
- Ability to identify race conditions in real code
- Understanding of thread synchronization primitives
- Knowledge of common concurrency anti-patterns
- Skill in balancing correctness with performance
- Testing concurrent code for reliability
