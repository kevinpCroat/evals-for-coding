"""
Thread-unsafe cache implementation with race conditions.

This cache has multiple concurrency issues:
1. Check-then-act race condition in get()
2. Non-atomic updates to shared dictionary
3. Race conditions in size tracking
"""

import time
from typing import Any, Optional


class SimpleCache:
    """A simple in-memory cache with race conditions."""

    def __init__(self, max_size: int = 100):
        self.cache = {}
        self.max_size = max_size
        self.hits = 0
        self.misses = 0

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache. Returns None if not found."""
        if key in self.cache:
            # Race condition: cache might be modified between check and access
            self.hits += 1  # Non-atomic increment
            return self.cache[key]
        else:
            self.misses += 1  # Non-atomic increment
            return None

    def put(self, key: str, value: Any) -> None:
        """Put value in cache."""
        # Race condition: size check and insertion are not atomic
        if len(self.cache) >= self.max_size:
            # Simple eviction: remove first item
            # Race condition: multiple threads might try to evict simultaneously
            if self.cache:
                first_key = next(iter(self.cache))
                del self.cache[first_key]

        self.cache[key] = value

    def get_stats(self) -> dict:
        """Get cache statistics."""
        total = self.hits + self.misses
        hit_rate = self.hits / total if total > 0 else 0.0
        return {
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': hit_rate,
            'size': len(self.cache)
        }

    def clear(self) -> None:
        """Clear the cache."""
        self.cache = {}
        self.hits = 0
        self.misses = 0
