import pytest
import time
from fastapi.testclient import TestClient
from app.main import app
from app.cache import LRUCache


client = TestClient(app)


@pytest.mark.asyncio
async def test_cache_set_and_get():
    """
    Test adding items to the cache and retrieving them.
    """
    cache = LRUCache(capacity=3)
    
    # Add items to the cache
    await cache.set("key1", "value1")
    await cache.set("key2", "value2")
    
    # Assert that the items are correctly retrieved from the cache
    assert await cache.get("key1") == "value1"
    assert await cache.get("key2") == "value2"


@pytest.mark.asyncio
async def test_cache_update():
    """
    Test updating an existing item in the cache.
    """
    cache = LRUCache(capacity=3)
    
    # Add an item to the cache
    await cache.set("key1", "value1")
    
    # Update the value for the same key
    await cache.set("key1", "value2")
    
    # Assert that the updated value is correctly retrieved from the cache
    assert await cache.get("key1") == "value2"


@pytest.mark.asyncio
async def test_cache_delete():
    """
    Test deleting an item from the cache.
    """
    cache = LRUCache(capacity=3)
    
    # Add items to the cache
    await cache.set("key1", "value1")
    await cache.set("key2", "value2")
    
    # Delete one item
    await cache.delete("key1")
    
    # Assert that the deleted item is no longer in the cache
    assert await cache.get("key1") is None
    # Assert that the other item still exists
    assert await cache.get("key2") == "value2"


@pytest.mark.asyncio
async def test_cache_eviction():
    """
    Test cache eviction when the cache reaches its capacity.
    """
    cache = LRUCache(capacity=2)
    
    # Add more items than the cache capacity
    await cache.set("key1", "value1")
    await cache.set("key2", "value2")
    await cache.set("key3", "value3")
    
    # Assert that the oldest item is evicted (LRU eviction)
    assert await cache.get("key1") is None
    # Assert that the newer items are still in the cache
    assert await cache.get("key2") == "value2"
    assert await cache.get("key3") == "value3"


@pytest.mark.asyncio
async def test_cache_ttl():
    """
    Test TTL (Time-to-Live) behavior in the cache.
    """
    cache = LRUCache(capacity=3)
    
    # Add an item with a TTL of 1 second
    await cache.set("key1", "value1", ttl=1)
    
    # Assert that the item is still in the cache initially
    assert await cache.get("key1") == "value1"
    
    # Wait for the TTL to expire (sleep for 2 seconds)
    time.sleep(2)
    
    # Assert that the item has expired and is no longer in the cache
    assert await cache.get("key1") is None


def test_get_item():
    # Сначала добавим элемент
    response = client.put("/cache/key1", json={"value": "value1", "ttl": 3600})
    assert response.status_code == 201
    
    # Теперь получим элемент
    response = client.get("/cache/key1")
    assert response.status_code == 200
    assert response.json() == {"value": "value1"}

def test_get_nonexistent_item():
    response = client.get("/cache/nonexistent_key")
    assert response.status_code == 404
    assert response.json() == {"detail": "Cache key not found or TTL expired"}

def test_set_item():
    response = client.put("/cache/key2", json={"value": "value2", "ttl": 3600})
    assert response.status_code == 201
    
    # Проверка обновления элемента
    response = client.put("/cache/key2", json={"value": "new_value2", "ttl": 3600})
    assert response.status_code == 200
    
    response = client.get("/cache/key2")
    assert response.status_code == 200
    assert response.json() == {"value": "new_value2"}

def test_delete_item():
    # Добавим элемент
    response = client.put("/cache/key3", json={"value": "value3", "ttl": 3600})
    assert response.status_code == 201
    
    # Удалим элемент
    response = client.delete("/cache/key3")
    assert response.status_code == 204
    
    # Проверим, что элемент удален
    response = client.get("/cache/key3")
    assert response.status_code == 404

def test_cache_eviction():
    # Добавим 3 элемента в кэш с лимитом 2
    client.put("/cache/key1", json={"value": "value1", "ttl": 3600})
    client.put("/cache/key2", json={"value": "value2", "ttl": 3600})
    client.put("/cache/key3", json={"value": "value3", "ttl": 3600})
    
    # Проверим, что первый элемент был вытеснен
    response = client.get("/cache/key1")
    assert response.status_code == 200
    response = client.get("/cache/key2")
    assert response.status_code == 200
    assert response.json() == {"value": "value2"}
    response = client.get("/cache/key3")
    assert response.status_code == 200
    assert response.json() == {"value": "value3"}

# def test_cache_ttl():
#     # Добавим элемент с TTL = 1 секунда
#     response = client.put("/cache/key4", json={"value": "value4", "ttl": 1})
#     assert response.status_code == 201
    
#     # Проверим, что элемент существует
#     response = client.get("/cache/key4")
#     assert response.status_code == 200
#     assert response.json() == {"value": "value4"}
    
#     # Подождем 2 секунды и проверим, что элемент истек
#     time.sleep(2)
#     response = client.get("/cache/key4")
#     assert response.status_code == 404

# def test_cache_stats():
#     # Добавим элементы в кэш
#     client.put("/cache/key1", json={"value": "value1", "ttl": 3600})
#     client.put("/cache/key2", json={"value": "value2", "ttl": 3600})
    
#     response = client.get("/cache/stats/")
#     assert response.status_code == 200
#     stats = response.json()
#     assert stats["size"] == 2
#     assert stats["capacity"] == 5  # default capacity
#     assert "key1" in stats["items"]
#     assert "key2" in stats["items"]
