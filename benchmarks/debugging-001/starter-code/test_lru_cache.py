"""
Tests for LRU Cache implementation
"""

import pytest
from lru_cache import LRUCache


class TestLRUCacheBasic:
    """Basic functionality tests"""

    def test_put_and_get(self):
        """Test basic put and get operations"""
        cache = LRUCache(3)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)

        assert cache.get("a") == 1
        assert cache.get("b") == 2
        assert cache.get("c") == 3

    def test_get_nonexistent(self):
        """Test getting a key that doesn't exist"""
        cache = LRUCache(3)
        assert cache.get("missing") is None

    def test_update_existing_key(self):
        """Test updating an existing key"""
        cache = LRUCache(3)
        cache.put("a", 1)
        cache.put("a", 100)
        assert cache.get("a") == 100

    def test_size(self):
        """Test size tracking"""
        cache = LRUCache(5)
        assert cache.size() == 0

        cache.put("a", 1)
        assert cache.size() == 1

        cache.put("b", 2)
        cache.put("c", 3)
        assert cache.size() == 3

    def test_contains(self):
        """Test membership checking"""
        cache = LRUCache(3)
        cache.put("a", 1)

        assert "a" in cache
        assert "b" not in cache


class TestLRUEviction:
    """Tests for LRU eviction behavior"""

    def test_eviction_at_capacity(self):
        """Test that items are evicted when capacity is reached"""
        cache = LRUCache(3)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)

        # Cache is now full. Adding a new item should evict "a"
        cache.put("d", 4)

        assert cache.get("a") is None  # "a" should be evicted
        assert cache.get("b") == 2
        assert cache.get("c") == 3
        assert cache.get("d") == 4
        assert cache.size() == 3

    def test_get_updates_recency(self):
        """Test that getting an item marks it as recently used"""
        cache = LRUCache(3)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)

        # Access "a" to mark it as recently used
        cache.get("a")

        # Add new item - "b" should be evicted (least recently used)
        cache.put("d", 4)

        assert cache.get("a") == 1  # "a" should still be there
        assert cache.get("b") is None  # "b" should be evicted
        assert cache.get("c") == 3
        assert cache.get("d") == 4

    def test_put_updates_recency(self):
        """Test that updating an existing key marks it as recently used"""
        cache = LRUCache(3)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)

        # Update "a" to mark it as recently used
        cache.put("a", 100)

        # Add new item - "b" should be evicted
        cache.put("d", 4)

        assert cache.get("a") == 100  # "a" should still be there
        assert cache.get("b") is None  # "b" should be evicted
        assert cache.get("c") == 3
        assert cache.get("d") == 4


class TestLRUEdgeCases:
    """Edge case tests"""

    def test_single_capacity_cache(self):
        """Test cache with capacity of 1"""
        cache = LRUCache(1)
        cache.put("a", 1)
        assert cache.get("a") == 1

        cache.put("b", 2)
        assert cache.get("a") is None
        assert cache.get("b") == 2

    def test_evict_and_readd_same_key(self):
        """
        FAILING TEST - This test demonstrates the bug.

        When we evict the LRU item and then immediately add a new item
        with the SAME key that was just evicted, the behavior is incorrect.
        """
        cache = LRUCache(2)
        cache.put("a", 1)
        cache.put("b", 2)

        # Cache is full with ["a", "b"]
        # Now we want to add "a" again with a new value
        # This should:
        # 1. Recognize "a" is the LRU item
        # 2. Remove it properly
        # 3. Add the new "a" with value 100

        cache.put("a", 100)

        # After this, cache should contain ["b", "a"] with a=100
        # Check the keys FIRST before calling get() (which has side effects)
        keys_list = list(cache.keys())
        assert keys_list == ["b", "a"], f"Expected ['b', 'a'], got {keys_list}"

        # Now verify the values
        assert cache.get("a") == 100
        assert cache.get("b") == 2
        assert cache.size() == 2

    def test_clear(self):
        """Test clearing the cache"""
        cache = LRUCache(3)
        cache.put("a", 1)
        cache.put("b", 2)

        cache.clear()
        assert cache.size() == 0
        assert cache.get("a") is None

    def test_invalid_capacity(self):
        """Test that invalid capacity raises error"""
        with pytest.raises(ValueError):
            LRUCache(0)

        with pytest.raises(ValueError):
            LRUCache(-1)
