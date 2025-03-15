from fastapi import FastAPI
from api.api import router as api_router
from app.middleware import RequestLoggingMiddleware


app = FastAPI()

app.include_router(api_router)
app.add_middleware(RequestLoggingMiddleware)
