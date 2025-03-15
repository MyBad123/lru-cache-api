import asyncio
import time
from collections import OrderedDict
from typing import Optional, Dict, Any


class LRUCache:
    def __init__(self, capacity: int = 5):
        self.capacity = capacity
        self.cache = OrderedDict()
        self.lock = asyncio.Lock()
        self.timestamps = {}
        self.ttls = {}

    def _is_expired(self, key: str) -> bool:
        if key not in self.timestamps:
            return True
        
        ttl = self.ttls.get(key, 3360)
        
        if ttl is None:
            ttl = 3360
        
        return time.time() - self.timestamps[key] > ttl


    async def get(self, key: str) -> Optional[Any]:
        async with self.lock:
            if key not in self.cache or self._is_expired(key):
                self.cache.pop(key, None)
                self.timestamps.pop(key, None)
                self.ttls.pop(key, None)
                return None
            
            self.cache.move_to_end(key)
            self.timestamps[key] = time.time()
            return self.cache[key]

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
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
        async with self.lock:
            if key in self.cache:
                self.cache.pop(key)
                self.timestamps.pop(key, None)
                self.ttls.pop(key, None)
                return True
            return False

    async def get_stats(self) -> Dict[str, int]:
        async with self.lock:
            return {
                "size": len(self.cache),
                "capacity": self.capacity,
                "items": list(self.cache.keys())[::-1]
            }

        
lry_cache = LRUCache()
