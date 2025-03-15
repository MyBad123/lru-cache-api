import aioredis
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi import FastAPI


from fastapi import APIRouter, Depends, HTTPException
from aioredis import Redis
from fastapi import Request
from app.cache import lry_cache
from app.models import StateItem

router = APIRouter()


def get_redis(request: Request) -> Redis:
    return request.app.state.redis


@router.get("/cache/{key}")
async def get_item_route(key: str, redis: Redis = Depends(get_redis)):
    """Получение элемента по ID"""
    
    # Получаем значение по ключу
    value = await lry_cache.get(redis, key)
    if value is None:
        raise HTTPException(status_code=404, detail="Cache not found or TTL expired")
    return {"key": key, "value": value}


@router.delete("/cache/{key}")
async def delete_item(key: str, redis: Redis = Depends(get_redis)):
    value = await lry_cache.get(redis, key)
    if value is None:
        raise HTTPException(status_code=404, detail="Cache not found or TTL expired")
    
    await lry_cache.delete(redis, key)
    
    return status.HTTP_204_NO_CONTENT


@router.get("/cache/stats/")
async def get_cache_stats(redis: Redis = Depends(get_redis)) -> StateItem:
    data = await lry_cache.get_keys_sorted_by_ttl(redis)
    return StateItem(**data)

