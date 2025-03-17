from fastapi import APIRouter, HTTPException, Response, status

from app.cache import lry_cache
from app.models import ChangeKey, GetKeyModel, StateItem


router = APIRouter(prefix='/cache')


@router.get("/stats")
async def get_cache_stats() -> StateItem:
    """
    Retrieve the current statistics of the cache.

    Returns:
        StateItem: The cache statistics.
    """
    data = await lry_cache.get_stats()
    return StateItem(**data)


@router.get("/{key}")
async def get_item_route(key: str) -> GetKeyModel:
    """
    Retrieve a cached item by its key.

    Args:
        key (str): The key of the item to fetch from the cache.

    Raises:
        HTTPException: If the cache key is not found or has expired.

    Returns:
        GetKeyModel: The cache value associated with the key.
    """
    value = await lry_cache.get(key)
    if value is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Cache key not found or TTL expired"
        )
    return GetKeyModel(value=value)


@router.put("/{key}")
async def set_item_route(key: str, value: ChangeKey):
    """
    Set or update a cache item.

    Args:
        key (str): The key of the item to cache.
        value (ChangeKeyRequest): The value and TTL for the cache entry.

    Returns:
        Response: The status of the cache update.
    """
    is_created = await lry_cache.set(key, value.value, value.ttl)
    return Response(
        status_code=status.HTTP_201_CREATED if is_created else status.HTTP_200_OK
    )


@router.delete("/{key}", status_code=204)
async def delete_item(key: str):
    """
    Delete a cached item by its key.

    Args:
        key (str): The key of the item to delete from the cache.

    Raises:
        HTTPException: If the cache key is not found.
    """
    deleted = await lry_cache.delete(key)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cache key '{key}' not found."
        )
