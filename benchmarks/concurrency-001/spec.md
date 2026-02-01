# Concurrency-001: Thread Safety and Race Condition Fixes

## Objective

Fix all race conditions in the provided Python code to make it thread-safe and ensure tests pass consistently across 100 consecutive runs.

## Background

Concurrent programming is essential for modern applications, but introduces challenges like race conditions, where multiple threads access shared state without proper synchronization. This benchmark tests your ability to identify and fix common concurrency bugs in Python code.

The provided code contains three modules with realistic race conditions:
- A cache with check-then-act bugs and non-atomic statistics
- A metrics counter with lost updates and inconsistent state
- A worker pool with unsafe queue operations and state transitions

These bugs cause intermittent test failures that only appear under concurrent load, making them difficult to debug but critical to fix.

## Requirements

### Functional Requirements
1. Fix all race conditions in cache.py, counter.py, and worker_pool.py
2. All tests in test_concurrency.py must pass consistently (100/100 runs)
3. Preserve the original API and functionality - do not change function signatures
4. Use appropriate Python synchronization primitives (threading.Lock, queue.Queue, etc.)

### Technical Constraints
- Only modify cache.py, counter.py, and worker_pool.py
- Do NOT modify test_concurrency.py
- Use only Python standard library (no external dependencies)
- Maintain backward compatibility with existing API
- No deadlocks or infinite waits allowed

### Quality Requirements
- All race conditions must be eliminated
- Critical sections properly protected with locks
- No check-then-act anti-patterns
- Atomic operations for related state updates
- Efficient synchronization (no over-locking)
- Code must complete within reasonable time (< 60 seconds for 100 test runs)

## Success Criteria

The implementation will be considered successful when:
1. All tests pass 100 consecutive runs without failures
2. No deadlocks occur during execution
3. Proper synchronization primitives are used correctly
4. Performance remains reasonable (< 3x slowdown from over-locking)
5. All original functionality is preserved

## Common Race Conditions to Fix

### In cache.py
- Check-then-act pattern in get() method
- Non-atomic dictionary updates and evictions
- Race conditions in hit/miss statistics tracking
- Concurrent modification during size checks

### In counter.py
- Non-atomic increment operations (+=)
- Lost updates when multiple threads increment
- Inconsistent state between related counters
- Classic read-modify-write race conditions

### In worker_pool.py
- Unsafe task queue operations (use queue.Queue)
- Non-atomic state transitions for workers
- Concurrent access to shared results list
- Inconsistent statistics updates

## Deliverables

1. Fixed cache.py with proper synchronization
2. Fixed counter.py with atomic operations
3. Fixed worker_pool.py with thread-safe queue and locks

## Evaluation

Your submission will be scored on:
- **Race Condition Tests (40%)** - All tests pass 100/100 consecutive runs with no failures
- **Deadlock Freedom (30%)** - Code completes without deadlocks, proper lock usage patterns
- **Synchronization Correctness (20%)** - Proper use of locks, no anti-patterns, atomic critical sections
- **Performance (10%)** - Reasonable execution time, not excessively slow from over-locking

See verification/verify.sh for automated scoring implementation.

## Tips

- Start by identifying all shared mutable state
- Look for check-then-act patterns (almost always bugs in concurrent code)
- Remember that `+=` and similar operations are NOT atomic
- Use `with lock:` context managers for cleaner, safer code
- Consider what operations need to happen atomically (together)
- Test your solution multiple times to ensure consistency

## Example Fix Pattern

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
