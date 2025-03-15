from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import logging

# Настроим логгер
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LogRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info(f"Request: {request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"Response: {response.status_code}")
        return response
