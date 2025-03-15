from fastapi import FastAPI
from api.api import router as api_router
import aioredis
import asyncio
from contextlib import asynccontextmanager

# Используем asynccontextmanager для управления подключением Redis
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создаем подключение к Redis при старте
    redis = await aioredis.from_url("redis://localhost:6379", db=0)
    app.state.redis = redis  # Сохраняем Redis в состоянии приложения
    yield
    # Закрытие соединения с Redis при остановке
    redis.close()
    await redis.wait_closed()

app = FastAPI(lifespan=lifespan)
app.include_router(api_router)
