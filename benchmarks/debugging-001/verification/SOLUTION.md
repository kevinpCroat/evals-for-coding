# Solution: LRU Cache Bug Root Cause

## Root Cause

The bug is in the `put()` method when the cache is at capacity. When adding a new key-value pair at capacity, the code:

1. Gets the least recently used (LRU) key: `lru_key = next(iter(self._cache))`
2. **Overwrites the value** of that LRU key instead of deleting it: `self._cache[lru_key] = value`
3. Moves that key to the end: `self._cache.move_to_end(lru_key)`

The critical flaw is in step 2: **the code reuses the old key instead of creating a new entry with the intended key**.

### Why This Causes the Bug

In the failing test case `test_evict_and_readd_same_key`:
- Cache has capacity 2 and contains: `{"a": 1, "b": 2}` (in that order)
- When we call `cache.put("a", 100)`:
  - The code sees the cache is at capacity
  - It gets `lru_key = "a"` (the first/oldest key)
  - It sets `self._cache["a"] = 100` (reusing the "a" key)
  - It moves "a" to the end
  - **BUT it never adds the new "a" entry - it just modified the existing one**

The problem is more general: when evicting at capacity, the code **replaces the LRU key's value instead of deleting the LRU entry and adding the new key**. This means:
- The new key is never actually added (if different from LRU key)
- The LRU key gets the new value instead
- The cache ends up with the wrong key-value mapping

### The Specific Lines

In `lru_cache.py`, lines ~47-50:
```python
if len(self._cache) >= self.capacity:
    lru_key = next(iter(self._cache))
    self._cache[lru_key] = value      # BUG: assigns to wrong key
    self._cache.move_to_end(lru_key)
```

This should DELETE the LRU key, then ADD the new key:
```python
if len(self._cache) >= self.capacity:
    lru_key = next(iter(self._cache))
    del self._cache[lru_key]
    self._cache[key] = value
```

Or use `popitem(last=False)` to remove and add in one step.

## Minimal Reproduction

```python
cache = LRUCache(2)
cache.put("a", 1)
cache.put("b", 2)
cache.put("c", 3)  # Should evict "a", add "c"

# Bug: "a" still exists with value 3, "c" is missing
print(cache.get("a"))  # Should be None, but returns 3
print(cache.get("c"))  # Should be 3, but returns None
```

Or even simpler:
```python
cache = LRUCache(1)
cache.put("x", 1)
cache.put("y", 2)  # Should evict "x", add "y"

print(cache.get("x"))  # Should be None, but returns 2
print(cache.get("y"))  # Should be 2, but returns None
```

## The Fix

Replace the buggy eviction logic:

```python
# Before (buggy):
if len(self._cache) >= self.capacity:
    lru_key = next(iter(self._cache))
    self._cache[lru_key] = value
    self._cache.move_to_end(lru_key)
else:
    self._cache[key] = value

# After (fixed):
if len(self._cache) >= self.capacity:
    self._cache.popitem(last=False)  # Remove LRU item
self._cache[key] = value  # Add new item
```

Or alternatively:
```python
if len(self._cache) >= self.capacity:
    lru_key = next(iter(self._cache))
    del self._cache[lru_key]
self._cache[key] = value
```

The key insight is that we must DELETE the old entry and ADD the new one with the correct key, not reuse the old key.
