import json
from typing import Optional, Dict
from fastapi import FastAPI
import aioredis
import asyncio

class RedisLRUCache:
    def __init__(self, ttl: int = 3600, max_items: int = 1000):
        self.ttl = ttl
        self.max_items = max_items
        self.lock = asyncio.Lock()

    async def _is_expired(self, redis: aioredis.Redis, key: str) -> bool:
        """Проверка, истек ли TTL элемента в Redis."""
        ttl = await redis.ttl(key)
        return ttl == -2  # Если ключ не существует (TTL истек)

    async def get(self, redis: aioredis.Redis, key: str) -> Optional[Dict]:
        """Получить элемент из кэша Redis"""
        
        async with self.lock:
            # Получаем элемент из Redis
            item_data = await redis.get(key)
            if item_data:
                # Если элемент существует и не истек — обновляем его как последний использованный
                await redis.expire(key, self.ttl)
                return item_data
            
            return None

    async def set(self, redis: aioredis.Redis, key: str, value: str) -> None:
        """Добавить или обновить элемент в Redis с проверкой на максимальное количество объектов"""
        async with self.lock:
            # Проверяем количество элементов в Redis
            keys_count = await redis.dbsize()
            if keys_count >= self.max_items:
                raise ValueError(f"Максимальное количество элементов ({self.max_items}) в кэше превышено")

            await redis.setex(key, self.ttl, value)

    async def delete(self, redis: aioredis.Redis, key: str) -> bool:
        """Удалить элемент из Redis"""
        async with self.lock:
            deleted = await redis.delete(key)
            return deleted > 0
        
    async def _get_ttl(self, redis: aioredis.Redis, key: bytes) -> tuple:
        """Получить TTL для ключа и вернуть в виде кортежа (key, ttl)."""
        ttl = await redis.ttl(key)
        return key.decode(), ttl

    async def get_keys_sorted_by_ttl(self, redis: aioredis.Redis) -> list:
        """Получить все ключи из Redis и отсортировать по оставшемуся времени жизни (TTL)"""
        
        async with self.lock:
            # Получаем все ключи в базе данных Redis
            keys = await redis.keys('*')
            
            # Получаем TTL для каждого ключа
            ttl_info = await asyncio.gather(
                *[self._get_ttl(redis, key) for key in keys]
            )

            # Сортируем ключи по оставшемуся TTL
            ttl_info.sort(key=lambda x: x[1])  # Сортируем по времени TTL (по возрастанию)

            return {
                'size': self.max_items,
                'capacity': len(ttl_info),
                'items': [obj[0] for obj in ttl_info]
            }

        

lry_cache = RedisLRUCache()
