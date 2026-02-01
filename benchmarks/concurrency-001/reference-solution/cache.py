"""
Thread-safe cache implementation with proper synchronization.

Fixed issues:
1. Added lock to protect all critical sections
2. Made get() atomic with proper synchronization
3. Protected statistics updates
4. Made eviction logic thread-safe
"""

import time
import threading
from typing import Any, Optional


class SimpleCache:
    """A simple in-memory cache with proper thread safety."""

    def __init__(self, max_size: int = 100):
        self.cache = {}
        self.max_size = max_size
        self.hits = 0
        self.misses = 0
        self.lock = threading.Lock()

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache. Returns None if not found."""
        with self.lock:
            if key in self.cache:
                self.hits += 1
                return self.cache[key]
            else:
                self.misses += 1
                return None

    def put(self, key: str, value: Any) -> None:
        """Put value in cache."""
        with self.lock:
            # Eviction logic is now atomic with insertion
            if len(self.cache) >= self.max_size and key not in self.cache:
                # Simple eviction: remove first item
                if self.cache:
                    first_key = next(iter(self.cache))
                    del self.cache[first_key]

            self.cache[key] = value

    def get_stats(self) -> dict:
        """Get cache statistics."""
        with self.lock:
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
        with self.lock:
            self.cache = {}
            self.hits = 0
            self.misses = 0
