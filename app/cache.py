import asyncio
import time
from collections import OrderedDict
from typing import Any, Dict, Optional


class LRUCache:
    def __init__(self, capacity: int = 5):
        """
        Initialize the LRU Cache.

        :param capacity: Maximum capacity of the cache.
        :raises ValueError: If the capacity is less than or equal to 0.
        """
        if capacity <= 0:
            raise ValueError("Capacity must be greater than 0")

        self.capacity = capacity
        self.cache = OrderedDict()
        self.lock = asyncio.Lock()
        self.timestamps = {}
        self.ttls = {}

    def _is_expired(self, key: str) -> bool:
        """Check if the cache item has expired."""

        ttl = self.ttls.get(key)
        if ttl is None:
            return False
        
        # Return True if the TTL has expired for the item
        return time.time() - self.timestamps[key] > ttl

    async def get(self, key: str) -> Optional[Any]:
        """Retrieve the value for the key from the cache, if it's not expired."""

        async with self.lock:
            if key not in self.cache or self._is_expired(key):
                self.cache.pop(key, None)
                self.timestamps.pop(key, None)
                self.ttls.pop(key, None)
                return None

            # Move the key to the end (it was recently accessed) and update the timestamp
            self.cache.move_to_end(key)
            self.timestamps[key] = time.time()
            return self.cache[key]

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set a value for a key in the cache, with an optional TTL."""

        async with self.lock:
            is_create = key not in self.cache
            
            if len(self.cache) >= self.capacity:
                self.cache.popitem(last=False)
            
            self.cache[key] = value
            self.cache.move_to_end(key)
            self.timestamps[key] = time.time()
            self.ttls[key] = ttl

            return is_create

    async def delete(self, key: str) -> bool:
        """Delete an item from the cache by its key."""

        async with self.lock:
            if key in self.cache:
                self.cache.pop(key)
                self.timestamps.pop(key, None)
                self.ttls.pop(key, None)
                return True
            return False

    async def get_stats(self) -> Dict[str, int]:
        """Get statistics about the cache."""

        async with self.lock:
            return {
                "size": len(self.cache),
                "capacity": self.capacity,
                "items": list(self.cache.keys())[::-1]
            }

        
lry_cache = LRUCache()
